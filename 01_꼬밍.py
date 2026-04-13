import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# 1. 구글 시트 연결 설정
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 날짜 불러오기 함수
def load_user_data(user_name):
    try:
        df = conn.read() # 시트 읽어오기
        user_row = df[df['name'] == user_name]
        if not user_row.empty:
            return user_row.iloc[0]['date'], int(user_row.iloc[0]['cycle'])
    except:
        pass
    # 데이터가 없으면 기본값 (봉이 30, 동생 28)
    return str(datetime.date.today()), (30 if user_name == "봉이" else 28)

# 3. 날짜 저장하기 함수
def save_user_data(user_name, date_str, cycle):
    df = conn.read()
    
    # 기존 데이터가 있으면 업데이트, 없으면 추가
    if user_name in df['name'].values:
        df.loc[df['name'] == user_name, ['date', 'cycle']] = [date_str, cycle]
    else:
        new_data = pd.DataFrame([{"name": user_name, "date": date_str, "cycle": cycle}])
        df = pd.concat([df, new_data], ignore_index=True)
    
    # 구글 시트에 다시 쓰기
    conn.update(data=df)
    st.cache_data.clear() # 캐시 삭제해서 바로 반영되게!

def calculate_cycle_day(start_date_str, cycle_len):
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = today - start_date
        return (delta.days % cycle_len) + 1
    except:
        return None  
    
# [핵심 수정] 루틴 박스 디자인 개선
def show_routine_list(title, color_style, routine_items):
    # 색상 스타일 적용
    if color_style == "success":
        icon = "☀️"
        container = st.success(f"**{title}**", icon=icon)
    elif color_style == "info":
        icon = "🌙"
        container = st.info(f"**{title}**", icon=icon)
    elif color_style == "warning":
        icon = "🌙"
        container = st.warning(f"**{title}**", icon=icon)
    else:
        icon = "🌙"
        container = st.error(f"**{title}**", icon=icon)
    
    # 박스 내용 출력
    for step, product in routine_items.items():
        st.markdown(f"**▪ {step}:** {product}")

# --- 2. 내 몸 주식회사 가이드 ---
def display_hormone_guide(day):
    # 0. 진행률 표시
    progress_val = min(day / 28, 1.0)
    st.progress(progress_val, text=f"현재 {day}일차 ({int(progress_val*100)}%) 진행 중")

    # [수정] 제목 가운데 정렬 (HTML 활용)
    st.markdown(f"""
        <h3 style='text-align: center; margin-bottom: -10px;'>🧸 오늘의 보고서: Day {day}</h3>
        <p style='text-align: center; font-size: 0.8em; color: gray;'>내 몸의 컨디션에 맞춘 최적의 솔루션</p>
        <hr style='margin-top: 5px; margin-bottom: 20px;'>
        """, unsafe_allow_html=True)
    
    # [NEW] 유화 과정 꿀팁 (항상 표시 - 공간 절약을 위해 expader 고려 가능하지만 중요하니 유지)
    with st.expander("💡 필독: 블랙헤드 박멸 '유화' 꿀팁 (Click)"):
        st.info("오일 후 물을 살짝 묻혀 **하얗게 변하게 하는 과정(1분)**을 꼭 지켜주세요!")

    # -----------------------------------------------------------
    # [1] 아침 세안법 결정 (제일 위로)
    # -----------------------------------------------------------
    skin_condition = st.selectbox(
        "👇 **오늘 아침 피부 상태를 선택하세요**",
        ["CASE 1. 평소/건조함 (당김)", "CASE 2. T존 번들거림 (생리전/배란기)", "CASE 3. 어제 무거운 팩 함 (잔여물)"]
    )

    # 세안제 변수 설정
    if "CASE 1" in skin_condition:
        cleanser = "💦물세안(가볍게)"
    else:
        cleanser = "☁️약산성 폼(소량)"

    # [공통] 아침 루틴
    morning_routine = {
        "세안": cleanser,
        "앰플": "💧디오디너리 히알루론산",
        "보습": "🧴프리메이 수분크림",
        "방어": "☀️선크림(꼼꼼히!)"
    }

    # ===========================================================
    # [2] 주기별 루틴 출력 (제목 축소 & 화장품 위로 배치)
    # ===========================================================

    # -------------------------------
    # 🩸 1. 생리기 (Day 1 ~ 5)
    # -------------------------------
    if 1 <= day <= 5:
        # [디자인 변경] 큰 배너 대신 깔끔한 소제목으로 변경하여 공간 확보
        st.markdown("##### 🩸 **1. 생리기: 대청소 & 휴식 기간**")
        
        # Day 1 ~ 2
        if day <= 2:
            st.caption("🚨 **1단계: 폭풍의 시작** (피부 장벽이 약해요. 자극 금지!)")
            
            # 루틴 먼저 보여주기 (User Request)
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"결정돈": "☁️ 토너", "수분": "💧히알루론산", "진정": "🌿 마데카/시카밤(듬뿍)"}
                show_routine_list("저녁 (진정)", "info", night_routine)
            
            # 긴 설명은 루틴 아래로 내리거나 작게 표시
            st.markdown("---")
            st.markdown("<small>💡 Tip: 화장품을 문지르지 말고 '지그시 눌러서' 흡수시키는 것이 핵심입니다.</small>", unsafe_allow_html=True)
            
        # Day 3 ~ 4
        elif day <= 4:
            st.caption("🧹 **2단계: 회복 중** (수분을 채워주세요)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"결정돈": "☁️ 토너", "스페셜": "🧖‍♀️:violet[수분 팩(15분)]", "수분": "💧히알루론산", "잠금": "🛡️마데카/시카밤"}
                show_routine_list("저녁 (수분충전)", "info", night_routine)
            
            st.markdown("---")
            st.markdown("<small>💡 Tip: 마스크팩은 15분을 넘기면 오히려 수분을 뺏어갑니다!</small>", unsafe_allow_html=True)

        # Day 5
        else: 
            st.caption("🌱 **3단계: 황금기 준비** (각질 정돈)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"딥클렌징": "📍violet:[효소파우더]", "결정돈": "☁️ 토너", "수분": "💧히알루론산", "진정": "🛡️마데카/시카밤"}
                show_routine_list("저녁 (각질제거)", "info", night_routine)

    # -------------------------------
    # 📈 2. 난포기 (Day 6 ~ 13)
    # -------------------------------
    elif 6 <= day <= 13:
        st.markdown("##### 📈 **2. 난포기: 황금기 & 리즈 갱신**")

        # Day 6
        if day == 6:
            st.caption("🚀 **Day 6: 비타민C 투입** (잡티 완화)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"결정돈": "☁️ 토너", "미백": "🍋:violet[비타민C]", "진정팩": "🧖‍♀️:violet[토리든 팩]", "마무리": "🛡️마데카/시카밤"}
                show_routine_list("저녁 (미백)", "warning", night_routine)
            
            st.markdown("<small>⚠️ 비타민C는 따가울 수 있습니다. 형광등도 조심하면 좋음.</small>", unsafe_allow_html=True)

        # Day 7
        elif day == 7:
            st.caption("🚀 **Day 7: 알부틴 + 기기 관리**")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"결정돈": "☁️ 토너", "수분": "💧히알루론산(듬뿍)", "기기": "💡:violet[알부틴+디바이스]", "마무리": "🛡️마데카/시카밤"}
                show_routine_list("저녁 (기기관리)", "warning", night_routine)

        # Day 8
        elif day == 8:
            st.caption("🚀 **Day 8: 리들샷 300** (길 뚫기)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"부스팅": "⚡:violet[VT 리들샷]", "결정돈": "☁️ 토너", "수분": "💧히알루론산", "진정": "🛡️:violet[시카밤(보습폭탄)]"}
                show_routine_list("저녁 (모공)", "warning", night_routine)
            
            st.markdown("<small>⚠️ 리들샷 사용 시 꾹꾹 눌러주기.</small>", unsafe_allow_html=True)

        # Day 9
        elif day == 9:
            st.caption("🚀 **Day 9: 나이아신아마이드** (모공 쫀쫀)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"결정돈": "☁️ 토너", "수분": "💧히알루론산", "모공": "🧴:violet[크림+나이아신]", "보습막": "크림 한겹 더"}
                show_routine_list("저녁 (모공)", "warning", night_routine)

        # Day 10~13
        else:
            st.caption("✨ **2단계: 물광 코팅** (유수분 밸런스)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"결정돈": "☁️ 토너", "수분": "💧히알루론산", "수분팩": "🧖‍♀️:violet[수분 마스크팩]", "마무리": "🛡️마데카 크림"}
                show_routine_list("저녁 (물광)", "warning", night_routine)

    # -------------------------------
    # 🎉 3. 배란기 (Day 14 ~ 16)
    # -------------------------------
    elif 14 <= day <= 16:
        st.markdown("##### 🎉 **3. 배란기: 피지 주의보**")
        
        # Day 14
        if day == 14:
            st.caption("🚨 **오늘 미션: 개기름 청소 & 열 내리기**")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"딥클렌징": "오일(코 집중)", "결정돈": "☁️ 토너", "쿨링팩": "🧊:violet[토리든 팩(차갑게)]", "마무리": "수분크림"}
                show_routine_list("저녁 (피지조절)", "warning", night_routine)

        # Day 15~16
        else:
            st.caption("🧹 **열 식히는 중** (쿨링 집중)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"쿨링": "🧊차가운 닥토", "수분": "💧히알루론산", "진정": "🧴프리메이", "마무리": "🛡️시카밤(얇게)"}
                show_routine_list("저녁 (쿨링)", "warning", night_routine)

    # -------------------------------
    # 🛡️ 4. 황체기 (Day 17 ~ 28)
    # -------------------------------
    else:
        st.markdown("##### 🛡️ **4. 황체기: 방어 모드**")

        # Day 17~22
        if day <= 22:
            st.caption("🧱 **1단계: 햇빛 & 건조 방어**")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"결정돈": "☁️ 토너", "집중케어": "💧:violet[히알루론산(2겹)]", "고보습": "🛡️마데카/세타필"}
                show_routine_list("저녁 (보습저장)", "info", night_routine)
            
            st.markdown("<small>⚠️ 속은 건조하고 겉은 번들거립니다. 수분을 채워주세요.</small>", unsafe_allow_html=True)

        # Day 23~28
        else:
            st.caption("🚨 **2단계: 폭동 전야 (생리 전)**")
            
            col1, col2 = st.columns(2)
            with col1:
                show_routine_list("아침 (수분)", "success", morning_routine)
            with col2:
                night_routine = {"세안": "☁️ 약산성 세안", "결정돈": "☁️ 토너", "진정": "🛡️시카밤(두껍게)", "SOS": "트러블패치"}
                show_routine_list("저녁 (최소화)", "error", night_routine)
            
            st.markdown("<small>⚠️ **긴급 지침:** 화장품 다이어트! 트러블 나면 패치만 붙이세요.</small>", unsafe_allow_html=True)

    st.divider()

# --- 3. 메인 실행 화면 ---
saved_date, saved_cycle = load_user_data("꼬밍") 

with st.sidebar:
    st.header("⚙️ My Room")
    
    if saved_date:
        st.write(f"📅 마지막 생리일: `{saved_date}`")
        st.write(f"🔄 설정된 주기: `{saved_cycle}일`")
    
    # 주기와 날짜 수정창
    new_cycle = st.number_input("내 생리 주기 (일)", min_value=21, max_value=35, value=saved_cycle)
    new_date = st.date_input("날짜 수정", 
                             value=datetime.datetime.strptime(saved_date, "%Y-%m-%d").date() if saved_date else datetime.date.today())
    
    if st.button("설정 저장"):
        # [수정된 부분] 옛날 save_date() 대신 구글 시트 저장 함수 사용!
        save_user_data("꼬밍", str(new_date), new_cycle)
        st.success("꼬밍님의 데이터가 구글 시트에 저장 완료!")
        st.rerun()

    st.divider()
    st.subheader("🗓️ 주기별 디바이스 가이드")

    # [수정] 사이드바 가독성 개선 (마크다운 리스트 활용)
    with st.expander("📡 초음파 모드 계획표", expanded=True):
        st.markdown("""
        * **1. 생리기 (Day 1~5)**
            * ⛔ **휴식** (피부 예민)
        
        * **2. 난포기 (Day 6~13)**
            * ✅ **황금기** (탄력/리프팅 추천!)
        
        * **3. 배란기 (Day 14~20)**
            * 💆‍♀️ **집중관리** (영양 공급)
        
        * **4. 생리전 (Day 21~28)**
            * ⚠️ **주의** (트러블 시 중단)
        """)
    st.info(f"현재 설정: {saved_cycle}일 주기")
    
# 메인 실행
if saved_date:
    # calculate_cycle_day 함수에 주기(saved_cycle) 변수도 같이 넘겨주기
    current_day = calculate_cycle_day(saved_date, saved_cycle) # 꼬밍 파일에서는 28일로 고정되어 있다면 이대로 둬도 됨!
    if current_day:
        display_hormone_guide(current_day) # (이전에 만든 호르몬 가이드 함수 이름이 맞는지 확인해!)
    else:
        st.error("날짜 형식 오류")
else:
    st.warning("👈 왼쪽 메뉴에서 날짜를 저장해주세요!")