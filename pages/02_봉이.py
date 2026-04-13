import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# --- 1. 구글 시트 및 데이터 기본 설정 ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_user_data():
    try:
        df = conn.read()
        # "MyRoutine" 대신 "봉이"를 찾아라!
        user_row = df[df['name'] == "봉이"] 
        if not user_row.empty:
            return user_row.iloc[0]['date']
    except:
        pass
    return str(datetime.date.today()) 

def save_user_data(date_str):
    df = conn.read()
    # "MyRoutine" 대신 "봉이" 자리에 저장해라!
    if "봉이" in df['name'].values:
        df.loc[df['name'] == "봉이", 'date'] = date_str
    else:
        new_row = pd.DataFrame([{"name": "봉이", "date": date_str, "cycle": 28}])
        df = pd.concat([df, new_row], ignore_index=True)
    conn.update(data=df)
    st.cache_data.clear()

# 주기는 28일로 고정!
def calculate_cycle_day(start_date_str):
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = today - start_date
        return (delta.days % 28) + 1
    except:
        return None

# --- 2. 루틴 박스 세로 정렬 디자인 ---
def show_routine_box(time, title, items):
    if time == "아침":
        st.success(f"**☀️ 아침: {title}**")
    elif time == "저녁":
        st.info(f"**🌙 저녁: {title}**")
    elif time == "스페셜":
        st.warning(f"**🌋 스페셜: {title}**")
    
    # 리스트로 받은 화장품을 세로로 하나씩 출력
    for item in items:
        st.markdown(f"▪️ {item}")

# --- 3. ⭐️ 내 몸 주식회사 가이드 (효과 추가 & 세로 정렬) ---
def display_hormone_guide(day):
    progress_val = min(day / 28, 1.0)
    st.progress(progress_val, text=f"현재 {day}일차 / 28일 주기 ({int(progress_val*100)}%) 진행 중")

    st.markdown(f"""
        <h3 style='text-align: center; margin-bottom: -10px;'>🧸 오늘의 뷰티 보고서: Day {day}</h3>
        <hr style='margin-top: 15px; margin-bottom: 20px;'>
        """, unsafe_allow_html=True)

    # 28일 고정 구간
    phase1_end = 5
    phase2_end = 13
    phase3_end = 17

    # 🩸 1단계: 생리 중 (Day 1~5)
    if 1 <= day <= phase1_end:
        st.markdown("#### 🩸 1단계: 생리 중 (피부 휴식 & 수분 올인!)")
        st.caption("🚨 피부 장벽이 제일 약하고 민감한 시기. 무조건 자극을 줄이고 푹 쉬게 해줘야 해! (기기, 리들샷, 효소, 바하 전부 ❌)")
        
        col1, col2 = st.columns(2)
        with col1:
            show_routine_box("아침", "수분 방어", [
                "라로슈포제 로션 (장벽/진정)",
                "매트릭실 (탄력 베이스)",
                "구달 아이크림 (눈가 미백)",
                "에스트라 크림 (보습막)",
                "선크림 (자외선 차단)"
            ])
        with col2:
            show_routine_box("저녁", "장벽 진정", [
                "더랩 토너 (수분 여러 번 촵촵)",
                "히알루로닉 앰플 (수분/진정)",
                "보르피린 (눈밑/팔자 국소 볼륨)",
                "라로슈포제 시카플라스트 밤 (장벽 진정 듬뿍)"
            ])

    # ✨ 2단계: 황금기 (Day 6~13)
    elif phase1_end < day <= phase2_end:
        st.markdown("#### ✨ 2단계: 생리 후 ~ 배란기 전 (영양 쫙쫙! 깐달걀 황금기)")
        st.caption("🏆 피부 컨디션 최상! **'리들샷'**과 **'기기 관리'**를 쏟아부어서 안티에이징과 미백을 확 끌어올려야 해.")
        
        show_routine_box("아침", "비타민 활력 (고정)", [
            "아로마티카 에센스 (항산화/결 정돈)",
            "코스알엑스 비타민C 23 (얼굴 전체 톤업)",
            "선크림 (무조건 듬뿍!)"
        ])
        
        st.markdown("##### 👇 저녁 루틴 (선택)")
        tab1, tab2, tab3 = st.tabs(["A. 리들샷 데이(주3회)", "B. 기기 흡수(매일)", "C. 초음파 스페셜(주1회)"])
        with tab1:
            show_routine_box("저녁", "리들샷", [
                "비플레인 LHA 토너 (순한 각질/닦토)",
                "VT 리들샷 300 (턴오버/길 뚫기)",
                "알파 아르부틴 (잡티/미백 집중)",
                "마데카크림 타임리버스 (재생/속탄력)"
            ])
        with tab2:
            show_routine_box("저녁", "기기 흡수 모드", [
                "더랩 토너 (속건조 방어)",
                "매트릭실 (전체 탄력)",
                "나이아신아마이드 (피지/미백)",
                "마데카 프라임 (흡수/브라이트닝 모드)",
                "에스트라 크림 (보습 코팅)"
            ])
            st.caption("🚨 주의: 리들샷 쓴 날은 기기 금지!")
        with tab3:
            show_routine_box("저녁", "초음파 스페셜", [
                "수분 마스크팩 or 히알루로닉 앰플 (수분 듬뿍)",
                "마데카 프라임 (초음파 모드로 깊숙이!)",
                "보르피린 (눈밑/팔자 콕콕)",
                "마데카크림 (재생 마무리)"
            ])

    # 🥚 3단계: 배란기 (Day 14~17)
    elif phase2_end < day <= phase3_end:
        st.markdown("#### 🥚 3단계: 배란기 (모공 청소 & 피지 조절)")
        st.caption("🧹 슬슬 피지량이 늘어나기 시작하는 타이밍! 모공이 막히지 않게 새로 산 효소 파우더로 부드럽게 청소해 줄 때야.")
        
        col1, col2 = st.columns(2)
        with col1:
            show_routine_box("아침", "피지/다크닝 방어", [
                "AHC 위치하젤 토너 (나비존 닦토/피지조절)",
                "코스알엑스 비타민C 23 (산화 방지/톤업)",
                "구달 비타C 아이크림 (잡티 케어)",
                "에스트라 크림 (평소보다 얇게)",
                "선크림 (자외선 필수)"
            ])
        with col2:
            show_routine_box("저녁", "효소 세안 데이", [
                "수이사이 효소 파우더 워시 (딥클렌징)",
                "AHC 위치하젤 토너 (모공 수렴 닦토)",
                "나이아신아마이드 (피지 조절)",
                "매트릭실 (탄력 충전)",
                "에스트라 크림 (마무리 보습)"
            ])

    # 🌋 4단계: 생리 직전 (Day 18~28)
    else:
        st.markdown("#### 🌋 4단계: 생리 직전 (트러블 방어 & 모공 순삭!)")
        st.caption("🚨 피지 폭발, 요철 대환장 파티 시기! 필살기 조합으로 요철을 잠재워야 해.")
        
        col1, col2 = st.columns(2)
        with col1:
            show_routine_box("아침", "피지 조절 핵집중", [
                "라로슈포제 토너 or AHC 토너 (진정 or 피지닦토)",
                "매트릭실 (가벼운 수분 탄력)",
                "나이아신아마이드 (★핵심! 피지 억제)",
                "구달 비타C 아이크림 (미백)",
                "에스트라 크림 (아주 얇게 코팅)",
                "선크림 (자외선 방어)"
            ])
        with col2:
            show_routine_box("스페셜", "바하 & 모델링팩 데이", [
                "반신욕 (스팀 팍팍 쐬며 모공 열기 🛁)",
                "애크린겔 바하 (요철 부위만 얇게 톡톡)",
                "히알루로닉 앰플 (얼굴 전체 듬뿍)",
                "녹두 모델링팩 (피지 흡착 & 수분 진정 🌿)",
                "시카플라스트 밤 (장벽 마무리)"
            ])

# --- 4. 메인 실행 & 사이드바 화면 ---
saved_date = load_user_data()

with st.sidebar:
    st.header("⚙️ 루틴 설정")
    if saved_date:
        st.write(f"📅 마지막 생리 시작일: `{saved_date}`")
    
    new_date = st.date_input("날짜 변경", 
                             value=datetime.datetime.strptime(saved_date, "%Y-%m-%d").date() if saved_date else datetime.date.today())
    
    if st.button("날짜 저장하기"):
        save_user_data(str(new_date))
        st.success("데이터 장부(시트)에 완벽하게 저장됐어!")
        st.rerun()

    st.divider()

    # 화장대 리스트 서랍
    with st.expander("💄 내 화장대 (무기 목록)", expanded=False):
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
        * 코스알엑스 비타민C 23 (강력 톤업)

        **🛡️ 크림 및 아이케어**
        * 구달 청귤 비타C 아이크림
        * 에스트라 아토베리어 365 크림
        * 센텔리안24 마데카크림 타임리버스
        * 라로슈포제 시카플라스트 밤 B5+

        **☀️ 스페셜 케어**
        * 수이사이 효소 파우더 워시 (묵은 각질)
        * 셀리맥스 잡티미백 (선크림)
        * 원씽 로즈힙열매오일 (보습막)
        * VT 리들샷 300 (턴오버 스페셜)
        * 애크린겔 바하 (요철/피지 녹이기)
        * 녹두 모델링팩 (쿨링/피지 흡착)

        **⚡ 뷰티 디바이스**
        * 마데카 프라임 (흡수/브라이트닝/초음파)
        """)

if saved_date:
    current_day = calculate_cycle_day(saved_date)
    if current_day:
        display_hormone_guide(current_day)
    else:
        st.error("날짜 형식에 문제가 있어!")
