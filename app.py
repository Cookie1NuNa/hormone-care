import streamlit as st
import datetime
import os

# --- 1. 기본 설정 및 함수 ---
DB_FILE = "last_period.txt"

def save_date(date_str):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        f.write(date_str)

def load_date():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def calculate_cycle_day(start_date_str):
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = today - start_date
        return (delta.days % 28) + 1
    except:
        return None

# [핵심 수정] 루틴을 보여주는 함수 (더 안전하게 변경)
def show_routine_list(title, color_style, routine_items):
    """
    루틴을 박스 안에 예쁘게 출력해주는 함수
    """
    # 색상 스타일 적용 (success=초록, info=파랑, warning=노랑, error=빨강)
    if color_style == "success":
        container = st.success(title)
    elif color_style == "info":
        container = st.info(title)
    elif color_style == "warning":
        container = st.warning(title)
    else:
        container = st.error(title)
    
    # 박스 바로 아래에 루틴 내용을 출력 (호환성 문제 해결)
    for step, product in routine_items.items():
        st.markdown(f"**▪ {step}:** {product}")

# --- 2. 내 몸 주식회사 가이드 ---
def display_hormone_guide(day):
    # 0. 진행률 표시
    progress_val = min(day / 28, 1.0)
    st.progress(progress_val, text=f"현재 {day}일차 ({int(progress_val*100)}%) 진행 중")

    st.divider()
    st.markdown(f"#### 🧸 오늘의 보고서: **Day {day}**")
    
    # -----------------------------------------------------------
    # [1] 아침 세안법 결정
    # -----------------------------------------------------------
    skin_condition = st.selectbox(
        "👇 오늘 아침 피부 상태는 어떤가요? (세안법 결정)",
        ["CASE 1. 평소/건조함 (당김)", "CASE 2. T존 번들거림 (생리전/배란기)", "CASE 3. 어제 무거운 팩 함 (잔여물)"]
    )

    # 세안제 변수 설정
    if "CASE 1" in skin_condition:
        cleanser = "💦물세안(가볍게)"
    else:
        cleanser = "☁️약산성 폼(소량)"

    # [공통] 아침 루틴 정의
    morning_routine = {
        "세안": cleanser,
        "앰플": "💧디오디너리 히알루론산",
        "보습": "🧴프리메이 수분크림",
        "방어": "☀️선크림(꼼꼼히!)"
    }

    # ===========================================================
    # [2] 주기별 루틴 출력
    # ===========================================================

    # -------------------------------
    # 🩸 1. 생리기 (Day 1 ~ 5)
    # -------------------------------
    if 1 <= day <= 5:
        st.error(f"### 🩸 1. 생리기: 대청소 & 휴식 기간 (Day {day})")
        
        # Day 1 ~ 2
        if day <= 2:
            st.markdown("#### 🚨 1단계: 폭풍의 시작 (Day 1~2)")
            st.caption("⚠️ 피부 장벽이 가장 약할 때입니다. 문지르지 말고 '지그시 눌러서' 흡수시키세요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "결정돈": "☁️ 토너",
                    "수분": "💧디오디너리 히알루론산",
                    "진정": "🌿 마데카/시카밤 (듬뿍)"
                }
                show_routine_list("🌙 저녁 (진정)", "info", night_routine)
            
        # Day 3 ~ 4
        elif day <= 4:
            st.markdown("#### 🧹 2단계: 조금씩 살아나는 중 (Day 3~4)")
            st.caption("⚠️ 마스크팩은 15분 넘기지 마세요! 오히려 수분을 뺏어갑니다.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "결정돈": "☁️ 토너",
                    "스페셜": "🧖‍♀️수분 마스크팩",
                    "수분": "💧디오디너리 히알루론산",
                    "잠금": "🛡️마데카/시카밤"
                }
                show_routine_list("🌙 저녁 (수분충전)", "info", night_routine)

        # Day 5
        else: 
            st.markdown("#### 🌱 3단계: 황금기 준비 (Day 5)")
            st.caption("묵은 각질을 살살 청소하고, 미백 앰플을 꺼내두세요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "딥클렌징": "📍효소파우더",
                    "결정돈": "☁️ 토너",
                    "수분": "💧디오디너리 히알루론산",
                    "진정": "🛡️마데카/시카밤"
                }
                show_routine_list("🌙 저녁 (각질제거)", "info", night_routine)

    # -------------------------------
    # 📈 2. 난포기 (Day 6 ~ 13)
    # -------------------------------
    elif 6 <= day <= 13:
        st.success(f"### 📈 2. 난포기: 황금기 & 리즈 갱신 (Day {day})")

        # Day 6
        if day == 6:
            st.markdown("#### 🚀 Day 6: 비타민C (잡티 완화)")
            st.caption("⚠️ 비타민C는 따가울 수 있습니다. 바른 직후 강한 자외선은 피하세요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "결정돈": "☁️ 토너",
                    "미백": "🍋코스알엑스 비타민C",
                    "진정팩": "🧖‍♀️토리든 마스크팩",
                    "마무리": "🛡️마데카/시카밤"
                }
                show_routine_list("🌙 저녁 (미백)", "warning", night_routine)

        # Day 7
        elif day == 7:
            st.markdown("#### 🚀 Day 7: 알부틴 + 기기 (톤 정리)")
            st.caption("⚠️ 기기 사용 시 앰플을 1.5배 듬뿍 발라 마찰을 줄이세요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "결정돈": "☁️ 토너",
                    "수분": "💧히알루론산(듬뿍!)",
                    "기기": "💡알부틴 + 디바이스",
                    "마무리": "🛡️마데카/시카밤"
                }
                show_routine_list("🌙 저녁 (기기관리)", "warning", night_routine)

        # Day 8
        elif day == 8:
            st.markdown("#### 🚀 Day 8: 리들샷 300 (길 뚫기)")
            st.caption("회복력이 좋을 때라 따가운 니들샷 쓰기 좋습니다. (비타민C와 동시 사용 금지)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "부스팅": "⚡VT 리들샷(맨얼굴)",
                    "결정돈": "☁️ 토너",
                    "수분": "💧히알루론산",
                    "진정": "🛡️시카밤(보습폭탄!)"
                }
                show_routine_list("🌙 저녁 (모공)", "warning", night_routine)

        # Day 9
        elif day == 9:
            st.markdown("#### 🚀 Day 9: 나이아신아마이드 (모공 쫀쫀)")
            st.caption("건조하지 않게 모공 관리하기. (크림에 섞어서 바르세요!)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "결정돈": "☁️ 토너",
                    "수분": "💧히알루론산",
                    "모공": "🧴크림 + 나이아신 믹스",
                    "보습막": "크림 한겹 더"
                }
                show_routine_list("🌙 저녁 (모공)", "warning", night_routine)

        # Day 10~13
        else:
            st.markdown("#### ✨ 2단계: 물광 코팅 (Day 10~13)")
            st.caption("곧 다가올 배란기(개기름) 대비, 유수분 밸런스를 맞춰두세요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "결정돈": "☁️ 토너",
                    "수분": "💧히알루론산",
                    "수분팩": "🧖‍♀️수분 마스크팩",
                    "마무리": "🛡️마데카 크림"
                }
                show_routine_list("🌙 저녁 (물광)", "warning", night_routine)

    # -------------------------------
    # 🎉 3. 배란기 (Day 14 ~ 16)
    # -------------------------------
    elif 14 <= day <= 16:
        st.warning(f"### 🎉 3. 배란기: 화려한 파티 & 피지 주의보 (Day {day})")
        
        # Day 14
        if day == 14:
            st.markdown("#### 🚨 오늘 미션: 개기름 청소 & 열 내리기")
            st.caption("난자 출시 파티 중! 폭죽(피지) 터지고 난리 났어요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "딥클렌징": "오일클렌징(코 집중)",
                    "결정돈": "☁️ 토너",
                    "쿨링팩": "🧊토리든 팩(차갑게!)",
                    "마무리": "프리메이 수분크림"
                }
                show_routine_list("🌙 저녁 (피지조절)", "warning", night_routine)

        # Day 15~16
        else:
            st.caption("파티 끝! 알로에 젤이나 차가운 토너로 얼굴 온도를 낮추세요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "쿨링": "🧊차가운 토너(닥토)",
                    "수분": "💧히알루론산",
                    "진정": "알로에/프리메이",
                    "마무리": "🛡️시카밤(얇게)"
                }
                show_routine_list("🌙 저녁 (쿨링)", "warning", night_routine)

    # -------------------------------
    # 🛡️ 4. 황체기 (Day 17 ~ 28)
    # -------------------------------
    else:
        st.info(f"### 🛡️ 4. 황체기: 방어 모드 & 존버 (Day {day})")
        st.caption("트러블 잠복기입니다. 유수분 밸런스에 집중하세요.")

        # Day 17~22
        if day <= 22:
            st.markdown("#### 🧱 1단계: 햇빛 & 건조 방어 (Day 17~22)")
            st.caption("속은 건조하고 겉은 번들거립니다. 크림보다는 수분 앰플을 2번 바르세요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "결정돈": "☁️ 토너",
                    "집중케어": "💧히알루론산(2겹)",
                    "고보습": "🛡️마데카/세타필"
                }
                show_routine_list("🌙 저녁 (보습저장)", "info", night_routine)

        # Day 23~28
        else:
            st.markdown("#### 🚨 2단계: 폭동 전야 (생리 전) (Day 23~28)")
            st.markdown("**[긴급 지침]** 화장품 다이어트! 트러블 나면 패치만 붙이세요.")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("☀️ 아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {
                    "세안": "☁️ 약산성 세안",
                    "결정돈": "☁️ 토너",
                    "진정": "🛡️시카밤(두껍게)",
                    "SOS": "트러블패치"
                }
                show_routine_list("🌙 저녁 (최소화)", "error", night_routine)

    st.divider()
    st.caption("💪 딱 10분 투자, 10년 유지. 정성스럽게 관리하세요.")

# --- 3. 메인 실행 화면 ---
saved_date = load_date()

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정 (My Room)")
    
    if saved_date:
        st.write(f"📅 마지막 생리일: `{saved_date}`")
    
    new_date = st.date_input("날짜 수정하기", 
                             value=datetime.datetime.strptime(saved_date, "%Y-%m-%d").date() if saved_date else datetime.date.today())
    
    if st.button("날짜 저장"):
        save_date(str(new_date))
        st.success("저장 완료!")
        st.rerun()

    st.divider()

    st.subheader("🗓️ 디바이스 결재판")
    with st.expander("📡 초음파 모드 계획표"):
        st.markdown("""
        **1. 생리기 (Day 1~5)**: ⛔ 휴식
        **2. 난포기 (Day 6~13)**: ✅ 황금기 (탄력)
        **3. 배란기 (Day 14~20)**: 💆‍♀️ 집중관리 (영양)
        **4. 생리전 (Day 21~28)**: ⚠️ 트러블 시 중단
        """)

# 메인 실행
if saved_date:
    current_day = calculate_cycle_day(saved_date)
    if current_day:
        display_hormone_guide(current_day)
    else:
        st.error("날짜 형식 오류")
else:
    st.warning("👈 왼쪽 메뉴에서 날짜를 저장해주세요!")