import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- 1. 구글 시트 및 데이터 기본 설정 ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_bongi_data():
    try:
        df = conn.read()
        user_row = df[df['name'] == "봉이"]
        if not user_row.empty:
            return user_row.iloc[0]['date'], int(user_row.iloc[0]['cycle'])
    except:
        pass
    return str(datetime.date.today()), 30 # 봉이 기본 주기 30일

def save_bongi_data(date_str, cycle):
    df = conn.read()
    if "봉이" in df['name'].values:
        df.loc[df['name'] == "봉이", ['date', 'cycle']] = [date_str, cycle]
    else:
        new_row = pd.DataFrame([{"name": "봉이", "date": date_str, "cycle": cycle}])
        df = pd.concat([df, new_row], ignore_index=True)
    conn.update(data=df)
    st.cache_data.clear()

def calculate_cycle_day(start_date_str, cycle_len):
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = today - start_date
        return (delta.days % cycle_len) + 1
    except:
        return None

# --- 2. 루틴 박스 디자인 함수 ---
def show_routine_box(time, title, items):
    if time == "아침":
        st.success(f"**☀️ 아침: {title}**")
    elif time == "저녁":
        st.info(f"**🌙 저녁: {title}**")
    elif time == "스페셜":
        st.warning(f"**🌋 스페셜: {title}**")
    
    st.markdown(items)

# --- 3. ⭐️ 핵심: 내 몸 주식회사 가이드 (봉이 대본 적용) ---
def display_hormone_guide(day, cycle_len):
    progress_val = min(day / cycle_len, 1.0)
    st.progress(progress_val, text=f"현재 {day}일차 / {cycle_len}일 주기 ({int(progress_val*100)}%) 진행 중")

    st.markdown(f"""
        <h3 style='text-align: center; margin-bottom: -10px;'>🧸 봉이의 뷰티 보고서: Day {day}</h3>
        <hr style='margin-top: 15px; margin-bottom: 20px;'>
        """, unsafe_allow_html=True)

    # 구간 계산 (봉이 주기에 맞춰 자동 조절)
    phase1_end = 5
    phase2_end = cycle_len - 15
    phase3_end = cycle_len - 11

    # 🩸 1단계: 생리 중
    if 1 <= day <= phase1_end:
        st.markdown("#### 🩸 1단계: 생리 중 (피부 휴식 & 수분 올인!)")
        st.caption("🚨 피부 장벽이 제일 약하고 민감한 시기야. 무조건 자극을 줄이고 푹 쉬게 해줘야 해! (기기, 리들샷, 효소, 바하 전부 ❌)")
        
        col1, col2 = st.columns(2)
        with col1:
            show_routine_box("아침", "수분 방어", "라로슈포제 로션 ➡️ 매트릭실 ➡️ 구달 아이크림 ➡️ 에스트라 크림 ➡️ 선크림")
        with col2:
            show_routine_box("저녁", "장벽 진정", "더랩 토너(여러 번 촵촵) ➡️ 히알루로닉 앰플 ➡️ 보르피린(눈밑/팔자 콕콕) ➡️ 라로슈포제 시카플라스트 밤 (듬뿍!)")

    # ✨ 2단계: 황금기
    elif phase1_end < day <= phase2_end:
        st.markdown("#### ✨ 2단계: 생리 후 ~ 배란기 전 (영양 쫙쫙! 깐달걀 황금기)")
        st.caption("🏆 피부 컨디션 최상! **'리들샷'**과 **'기기 관리'**를 쏟아부어서 안티에이징과 미백을 확 끌어올려야 해.")
        
        show_routine_box("아침", "비타민 활력 (고정)", "아로마티카 에센스 ➡️ 코스알엑스 비타민C 23 (얼굴 전체 톤업) ➡️ 선크림 무조건 듬뿍!")
        
        st.markdown("##### 👇 저녁 루틴 (선택)")
        tab1, tab2, tab3 = st.tabs(["A. 리들샷 데이(주3회)", "B. 기기 흡수(매일)", "C. 초음파 스페셜(주1회)"])
        with tab1:
            show_routine_box("저녁", "리들샷", "비플레인 LHA 토너(닦토) ➡️ VT 리들샷 300 ➡️ 알파 아르부틴 ➡️ 센텔리안24 마데카크림 타임리버스")
        with tab2:
            show_routine_box("저녁", "기기 흡수 모드", "더랩 토너 ➡️ 매트릭실 ➡️ 나이아신아마이드 ➡️ **마데카 프라임(흡수/브라이트닝 모드 윙윙~)** ➡️ 에스트라 크림\n\n*(🚨주의: 리들샷 쓴 날은 기기 금지!)*")
        with tab3:
            show_routine_box("저녁", "초음파 스페셜", "수분 마스크팩(또는 히알루로닉 앰플 듬뿍) ➡️ **마데카 프라임(초음파 모드)** ➡️ 보르피린 콕콕 ➡️ 마데카크림 마무리")

    # 🥚 3단계: 배란기
    elif phase2_end < day <= phase3_end:
        st.markdown("#### 🥚 3단계: 배란기 (모공 청소 & 피지 조절)")
        st.caption("🧹 슬슬 피지량이 늘어나기 시작하는 타이밍! 모공이 막히지 않게 새로 산 효소 파우더로 부드럽게 청소해 줄 때야.")
        
        show_routine_box("아침", "피지/다크닝 방어", "AHC 위치하젤 토너 (나비존/T존 닦토) ➡️ 코스알엑스 비타민C 23 ➡️ 구달 비타C 아이크림 ➡️ 에스트라 아토베리어 크림 (얇게!) ➡️ 선크림 필수!☀️")
        st.info("💡 **포인트:** 고농축 비타민C가 모공에서 나오는 피지가 산화돼서 다크닝 오는 걸 싹 방어해 줄 거야!")
        
        show_routine_box("저녁", "효소 세안 데이", "수이사이 효소 파우더 워시(딥클렌징!) ➡️ AHC 위치하젤 토너(모공 수렴 닦토) ➡️ 나이아신아마이드(피지 조절) ➡️ 매트릭실 ➡️ 에스트라 크림")

    # 🌋 4단계: 생리 직전
    else:
        st.markdown("#### 🌋 4단계: 생리 직전 (트러블 방어 & 모공 순삭!)")
        st.caption("🚨 피지 폭발, 요철 대환장 파티 시기! 봉이의 필살기 조합으로 요철을 잠재워야 해.")
        
        show_routine_box("아침", "피지 조절 핵집중", "라로슈포제 토너(흡수) or AHC 토너(닦토) ➡️ 매트릭실 ➡️ **나이아신아마이드 (★핵심! 뿜어져 나오는 피지 조절)** ➡️ 구달 비타C 아이크림 ➡️ 에스트라 크림 (아주 얇게 코팅만) ➡️ 선크림!☀️")
        
        show_routine_box("스페셜", "바하 & 모델링팩 데이", "반신욕(스팀 팍팍 쐬며 모공 열기 🛁) ➡️ 애크린겔(바하) 요철 부위에만 얇게 톡톡! ➡️ 히알루로닉 앰플 듬뿍 ➡️ **시원하게 녹두 모델링팩 (피지 흡착 & 수분 진정 🌿)** ➡️ 시카플라스트 밤 마무리!")

# --- 4. 메인 실행 & 사이드바 화면 ---
saved_date, saved_cycle = load_bongi_data()

with st.sidebar:
    st.header("⚙️ 봉이 설정")
    if saved_date:
        st.write(f"📅 시작일: `{saved_date}`")
    
    new_cycle = st.number_input("내 생리 주기 (일)", min_value=21, max_value=35, value=saved_cycle)
    new_date = st.date_input("마지막 생리 시작일", 
                             value=datetime.datetime.strptime(saved_date, "%Y-%m-%d").date() if saved_date else datetime.date.today())
    
    if st.button("설정 저장하기"):
        save_bongi_data(str(new_date), new_cycle)
        st.success("데이터 장부(시트)에 완벽하게 저장됐어!")
        st.rerun()

    st.divider()

    # 💄 봉이가 요청한 화장품 리스트 서랍!
    with st.expander("💄 봉이의 화장대 (내 무기들)", expanded=False):
        st.markdown("""
        **💧 토너 및 에센스**
        * 더랩 올리고 히알루론산 토너 (속건조)
        * 라로슈포제 톨레리앙 로션 (장벽/진정)
        * 비플레인 녹두 LHA 토너 (순한 닦토)
        * AHC 허브 솔루션 토너 (피지 조절)
        * 아로마티카 로즈마리 에센스 (결 정돈)

        **✨ 앰플 및 세럼**
        * 디오디너리 히알루로닉 (수분/진정)
        * 디오디너리 나이아신아마이드 (피지/미백)
        * 디오디너리 알파 아르부틴 (잡티/미백)
        * 디오디너리 매트릭실 (전체 탄력)
        * 보르피린 앰플 (국소 볼륨)
        * **코스알엑스 비타민C 23** (강력 톤업)

        **🛡️ 크림 및 아이케어**
        * 구달 청귤 비타C 아이크림
        * 에스트라 아토베리어 365 크림
        * 센텔리안24 마데카크림 타임리버스
        * 라로슈포제 시카플라스트 밤 B5+

        **☀️ 스페셜 케어**
        * **수이사이 효소 파우더 워시** (묵은 각질)
        * 셀리맥스 잡티미백 (선크림)
        * 원씽 로즈힙열매오일 (보습막)
        * VT 리들샷 300 (턴오버 스페셜)
        * 애크린겔 바하 (요철/피지 녹이기)
        * 녹두 모델링팩 (쿨링/피지 흡착)

        **⚡ 뷰티 디바이스**
        * 마데카 프라임 (흡수/브라이트닝/초음파)
        """)

if saved_date:
    current_day = calculate_cycle_day(saved_date, saved_cycle)
    if current_day:
        display_hormone_guide(current_day, saved_cycle)
    else:
        st.error("날짜 형식에 문제가 있어!")