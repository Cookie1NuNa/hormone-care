import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime


# --- 0. 세션 상태 초기화 (코드 맨 윗부분에 넣어줘!) ---
if 'menu_select' not in st.session_state:
    st.session_state.menu_select = '🗓️ 주기별 루틴'
if 'special_page' not in st.session_state:
    st.session_state.special_page = None

# --- 1. 구글 시트 및 데이터 기본 설정 ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_user_data():
    try:
        df = conn.read()
        # "꼬밍"를 찾아라!
        user_row = df[df['name'] == "꼬밍"] 
        if not user_row.empty:
            return user_row.iloc[0]['date']
    except:
        pass
    return str(datetime.date.today()) 

def save_user_data(date_str):
    df = conn.read()
    # "꼬밍" 자리에 저장해라!
    if "꼬밍" in df['name'].values:
        df.loc[df['name'] == "꼬밍", 'date'] = date_str
    else:
        new_row = pd.DataFrame([{"name": "꼬밍", "date": date_str, "cycle": 28}])
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

# --- 3. ⭐️ 내 몸 주식회사 가이드 ---
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
        
        show_routine_box("아침", "미백 광채 집중 ✨", [
            "아로마티카 에센스 (항산화/결 정돈)",
            "나이아신아마이드 + 알파 아르부틴 (잡티 싹! 전체 톤업 💡)",
            "구달 청귤 아이크림 (눈가 다크서클 환하게 톡톡 🍊)",
            "에스트라 크림 (수분 코팅)",
            "선크림 (무조건 듬뿍! 자외선 철벽 방어 🛡️)"
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
                "마데카 프라임 (흡수모드)",
                "에스트라 크림 (보습 코팅)"
            ])
            st.caption("🚨 주의: 리들샷 쓴 날은 기기 금지!")
        with tab3:
            show_routine_box("저녁", "초음파 스페셜", [
                "셀리맥스 잡티 미백 마스크팩 (황금기 미백 끌올! 팩 얹고 기기 쓰기 ⚡)", # 👈 셀리맥스 팩 추가!
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
                "나이아신아마이드 + 알파 아르부틴 (비타민C 대체! 피지/미백 콤보 💡)",
                "구달 청귤 아이크림 (눈가 다크서클/잡티 케어 🍊)",
                "에스트라 크림 (평소보다 얇게 보습막)",
                "선크림 (자외선 필수 🛡️)"
            ])
        with col2:
            show_routine_box("저녁", "효소 세안 데이", [
                "수이사이 효소 파우더 워시 (묵은 각질/피지 딥클렌징 🧼)",
                "AHC 위치하젤 토너 (모공 수렴 닦토)",
                "히알루로닉 앰플 (각질 제거 후 수분 꽉꽉 채우기 필수! 💧)",
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
            st.markdown("#### 🌟 스페셜 모공 루틴 (택 1)")
            
            # 선택해서 볼 수 있게 탭 기능을 쓰면 화면이 더 깔끔해!
            tab_a, tab_b = st.tabs(["🅰️ 애크린겔 데이", "🅱️ 딥클렌징&팩 데이"])
            
            with tab_a:
                show_routine_box("스페셜", "애크린겔 피지 관리", [
                    "반신욕 (스팀 팍팍 쐬며 모공 열기 🛁)",
                    "순한 폼 클렌징 세안 🧼 (🚨파우더워시 금지!)",
                    "애크린겔 (요철 부위만 얇게 톡톡) 🧫",
                    "히알루로닉 앰플 (수분 꽉꽉 채우기 💧)",
                    "시카플라스트 밤 (장벽 마무리)"
                ])
                
            with tab_b:
                show_routine_box("스페셜", "파우더워시 & 진정 팩", [
                    "반신욕 (스팀 팍팍 쐬며 모공 열기 🛁)",
                    "효소 파우더 워시 (부드럽게 각질 청소 🧼)",
                    "히알루로닉 앰플 (진정 베이스 깔기)",
                    "녹두 모델링팩 (피지 흡착 & 수분 진정 🌿)",
                    "시카플라스트 밤 (마무리)"
                ])

   # --- 💡 루틴 박스 바로 아래 고정되는 사용법 가이드 ---
    st.divider()
    st.markdown("### 💡 잊지 말자! 핵심 무기 사용법 & 정량")
    st.info("""
    **🧫 1. 애크린겔 (바하 - 요철/피지 컨트롤)**
    * **정량:** 고민 부위(나비존, 코 등) 1곳당 **딱 쌀알 한 톨 크기 🌾**
    * **사용법:** **🚨얼굴 전체 도포 절대 금지!** 세안 후 첫 단계나 스킨케어 마무리 쯤에, 깨끗한 손끝에 덜어서 오돌토돌한 요철 부위에만 아주 얇게 스치듯 코팅해 줘.

    **🌿 2. 녹두 모델링팩 (쿨링 & 수분 진정)**
    * **정량:** 얼굴이 안 보일 정도로 도톰하게 (너무 얇으면 수분을 뺏어가니 주의!)
    * **사용법:** 애크린겔 바른 날이나 달리기 후 열감이 있을 때 필수! 피부에 수분 앰플이나 부스팅 젤을 듬뿍 바른 뒤, 그 위에 모델링팩을 두껍게 올리고 **딱 15~20분 뒤**에 떼어내기.

    **💉 3. 보르피린 앰플 (국소 부위 볼륨 충전)**
    * **정량:** 눈밑/팔자주름 양쪽 다 합쳐서 **딱 1방울 💧**
    * **사용법:** 유분이 아주 많으니 단독 사용보다는 쫀쫀한 크림이나 아이크림에 1방울 섞어 쓰는 걸 추천! 네 번째 손가락(약지)으로 고민 부위에만 콕콕 찍어서 가볍게 두드려 흡수시켜 줘. **🚨절대 문지르기 금지 (잔주름/비립종 유발)!**
    """)

    # --- 💡 루틴 박스 바로 아래 고정되는 사용법 가이드 ---
    st.divider()
    st.markdown("### 💡 잊지 말자! 핵심 무기 사용법 & 정량")
    st.info("""
    **🍋 1. 코스알엑스 비타민C 23 & ✨ 기타 세럼류**
    * **비타민C 정량:** 양볼/이마 각 1방울 (총 2~3방울 💧)
    * **기타 세럼 정량:** 스포이드 1번 펌핑 (강낭콩 한 알 크기 🫘)
    * **사용법:** 욕심내지 말고 얇게 펴 바른 후 손바닥 온기로 꾹꾹 눌러 흡수시켜 줘! 여러 앰플을 겹쳐 바를 땐 앞 단계가 완전히 흡수되도록 약 1분 정도 간격을 두는 게 좋아.

    **🧫 2. 애크린겔 (바하 - 요철/피지 컨트롤)**
    * **정량:** 고민 부위 1곳당 **딱 쌀알 한 톨 크기 🌾**
    * **사용법:** **🚨얼굴 전체 도포 절대 금지!** 기초 케어 마지막 단계나 크림 직전에, 면봉이나 깨끗한 손끝에 덜어서 요철 부위에만 아주 얇게 스치듯 코팅해 줘.

    **💉 3. 보르피린 앰플 (국소 부위 볼륨 충전)**
    * **정량:** 눈밑/팔자주름 양쪽 다 합쳐서 **딱 1방울 💧**
    * **사용법:** 손등에 1방울 덜어낸 다음, 네 번째 손가락(약지)으로 꺼진 부위에만 콕콕 찍어서 두드려 발라줘. 전체적으로 바르면 유분 폭발하니 국소 부위만 공략하기!
    """)

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

 # --- 5. 메인 화면 출력 로직 ---
if st.session_state.menu_select == "🗓️ 주기별 루틴":
    # 👆 사이드바에서 '주기별 루틴'을 골랐을 때 나오는 원래 화면!
    if saved_date:
        current_day = calculate_cycle_day(saved_date)
        if current_day:
            display_hormone_guide(current_day)
        else:
            st.error("날짜 형식에 문제가 있어!")

else:
    # 👆 사이드바에서 '스페셜 케어 도감'을 골랐을 때 나오는 새로운 화면!
    # --- 🌋 스페셜 케어 도감 상세 페이지 ---
    selected_item = st.session_state.get('special_page', '선택하세요')
    
    if selected_item == "선택하세요":
        st.info("👈 왼쪽 사이드바에서 궁금한 무기를 선택해 봐! 🔍")
    else:
        st.subheader(f"🌋 {selected_item} 사용 설명서")
        
        # 1. 리들샷 300
        if selected_item == "💉 리들샷 300":
            st.markdown("""
            **🎯 목적:** 피부 턴오버 촉진 & 유효 성분 흡수 극대화
            * **사용법:** 세안 후 첫 단계에서 맨 얼굴에 도포. 따끔따끔한 느낌이 들어야 정상이야! 손바닥으로 꾹꾹 누르며 흡수시켜 줘.
            * **🚨 주의사항:** **마데카 프라임 기기 절대 금지!** 다음 날 선크림 필수!
            """)

        # 2. 마데카 초음파
        elif selected_item == "⚡ 마데카 초음파":
            st.markdown("""
            **🎯 목적:** 피부 속 탄력 개선 & 리프팅
            * **사용법:** 젤이나 마스크팩을 얹은 상태에서 '초음파 모드'로 천천히 롤링해 줘.
            * **꿀팁:** 황금기(2단계)에 미백 마스크팩이랑 같이 쓰면 효과가 두 배! ✨
            """)

        # 3. 효소 파우더워시
        elif selected_item == "🧼 효소 파우더워시":
            st.markdown("""
            **🎯 목적:** 자극 없는 각질 제거 & 모공 청소
            * **사용법:** 손바닥에 가루를 덜고 물을 살짝 섞어 거품을 충분히 낸 뒤, 나비존과 턱 위주로 부드럽게 굴려줘.
            * **정량:** 동전 크기만큼 1회분!
            """)

        # 4. 애크린겔(바하)
        elif selected_item == "🧫 애크린겔(바하)":
            st.markdown("""
            **🎯 목적:** 좁쌀 여드름 & 요철 박멸
            * **정량:** 고민 부위당 **딱 쌀알 한 톨 🌾**
            * **사용법:** 기초 마지막 단계에서 요철이 심한 부위에만 아주 얇게 코팅하듯 발라줘. 얼굴 전체 도포는 절대 안 돼!
            """)

        # 5. 녹두 모델링팩
        elif selected_item == "🌿 녹두 모델링팩":
            st.markdown("""
            **🎯 목적:** 피부 열감 내리기 & 수분 진정
            * **사용법:** 앰플을 듬뿍 바른 뒤, 모델링팩을 도톰하게 올려서 15~20분 뒤 떼어내기.
            * **꿀팁:** 땀 흘리고 온 날이나 생리 직전 피부 뒤집어지려 할 때 필수템! 🏃‍♀️
            """)

        # 6. 반신욕 루틴
        elif selected_item == "🛁 반신욕 루틴":
            st.markdown("""
            **🎯 목적:** 순환 촉진 & 노폐물 배출
            * **방법:** 물 온도는 38~40도, 시간은 15~20분 내외로! 땀이 살짝 나기 시작할 때가 딱 좋아.
            * **루틴 연계:** 반신욕 후 모공이 열렸을 때 효소 세안이나 모델링팩을 하면 효과가 극대화돼. 🧖‍♀️
            """)

        st.divider()
        if st.button("🗓️ 다시 주기별 루틴 보러 가기"):
            st.session_state.menu_select = "🗓️ 주기별 루틴"
            st.rerun()