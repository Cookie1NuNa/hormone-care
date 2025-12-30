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

def make_routine(steps):
    return " ➡️ ".join(steps)

def calculate_cycle_day(start_date_str):
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        delta = today - start_date
        return (delta.days % 28) + 1
    except:
        return None


# --- 2-1. [추가] 건성(제2유형) 전용 상시 업무 지침 ---
def display_dry_skin_habit():
    st.info("### 🍂 2. 에스트로겐 부족형 (긴축 재정의 스타트업)")
    st.caption("※ 이 내용은 생리 주기와 무관하게 **매일 결재(실행)**해야 하는 기본 수칙입니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. 세안 후 '3초 룰' (골든타임)**
        * 수건으로 닦자마자 수분이 날아갑니다.
        * 물기가 살짝 남았을 때 **'디오디너리 히알루론산'**을 바로 바르세요. (욕실에 두고 쓰세요!)
        
        **2. 크림은 '이불'처럼 덮기**
        * 젤 크림만으로는 부족합니다.
        * 저녁엔 **'시카플라스트 밤'**이나 **'마데카 크림'**처럼 꾸덕한 걸로 수분이 못 도망가게 이불을 덮어주세요.
        """)
        
    with col2:
        st.markdown("""
        **3. 아침 세안은 '물'로만**
        * 밤사이에 나온 좋은 기름까지 씻어내지 마세요.
        * 아침엔 클렌징폼 대신 **미지근한 물**로만 씻는 게 피부 장벽을 지키는 비결입니다.
        
        **4. 믹스(Mix) 기술 활용**
        * 피부가 유독 당기는 날엔 크림에 **'페이스 오일'**을 1~2방울 섞으세요.
        
        **🍯 휴대용 소방관 (멀티밤)**
        * 갖고 계신 **'CNP 프로폴리스 밤'**은 건조할 때마다 수시로 바르세요.
        * 눈가, 입가, 팔자 주름, 목주름 등 건조한 부위에 즉시 수분 충전!
        * ⚠️ **주의:** 사용 후엔 티슈로 스틱을 닦아야 트러블이 안 납니다!
        """)
        

# --- 2. [핵심] 내 몸 주식회사 가이드 (친절한 버전) ---
def display_hormone_guide(day):
    st.divider()
    st.markdown(f"#### 🧸 오늘의 보고서: **Day {day}**")
    
    # -----------------------------------------------------------
    # [1] 아침 세안법 결정 (여기가 가장 먼저 실행되어야 함!)
    # -----------------------------------------------------------
    skin_condition = st.selectbox(
        "👇 오늘 아침 피부 상태는 어떤가요? (세안법 결정)",
        ["CASE 1. 평소/건조함 (당김)", "CASE 2. T존 번들거림 (생리전/배란기)", "CASE 3. 어제 무거운 팩 함 (잔여물)"]
    )

    # 선택에 따라 세안제 변수 설정
    if "CASE 1" in skin_condition:
        cleanser = "💦물세안(가볍게)"
    else:
        cleanser = "☁️약산성 폼(소량)"

    # 'common_morning' 변수 완성 (이 변수가 아래 모든 아침 루틴에 들어갑니다)
    common_morning = make_routine([cleanser, '💧디오디너리 히알루론산', '프리메이 수분크림', '🧴선크림(꼼꼼히!)'])

    # [유형파악] <여성 호르몬 수치별 3가지 유형>
    with st.expander("ℹ️ <여성 호르몬 수치별 3가지 유형> (나는 어디에 속할까?)"):
        st.caption("사람마다 회사의 '자본금(호르몬 양)'이 다릅니다. 내 유형을 알면 공략법이 보입니다!")
        
        tab1, tab2, tab3 = st.tabs(["💖 1. 부자형", "🍂 2. 부족형(나)", "🎸 3. 우세형"])
        
        with tab1:
            st.markdown("""
            ### 💖 1. 에스트로겐 부자형 (자본금 빵빵한 대기업)
            **"여성성 과다 & 드라마 퀸"**
            * **👍 장점:** 동안 피부, S라인 몸매, 애교 많은 성격.
            * **👎 단점:** 감정 기복 심함, 생리통/여성질환 주의.
            * **💡 지침:** 독소 배출(브로콜리, 양배추) & 금주.
            """)
        with tab2:
            st.markdown("""
            ### 🍂 2. 에스트로겐 부족형 (알뜰 살림형 스타트업)
            **"시크하고 쿨함 & 건조 주의보"**
            * **👍 장점:** 생리통 거의 없음(무통), 여드름/개기름 걱정 없음.
            * **👎 단점:** 온몸이 건조함(사막화), 잔주름/노화 주의.
            * **💡 지침:** 보습(페이스 오일) & 에스트로겐 식품(콩, 석류) 섭취.
            """)
        with tab3:
            st.markdown("""
            ### 🎸 3. 안드로겐 우세형 (전투적인 경쟁 기업)
            **"걸크러쉬 & 트러블 메이커"**
            * **👍 장점:** 근육 잘 붙음(근수저), 리더십/추진력 좋음.
            * **👎 단점:** 턱 여드름, 복부 비만, 생리 불규칙.
            * **💡 지침:** 당 줄이기(탄수화물 제한) & 다이어트 필수.
            """)
            
    # [친절한 안내] 세계관 설명
    with st.expander("ℹ️ '내 몸 주식회사'가 뭔가요? (처음 오셨다면 필독!)"):
        st.markdown("""
        **우리 몸을 하나의 '회사'라고 상상해 보세요!** 🏢
        매달 '임신'이라는 프로젝트를 위해 직원(호르몬)들이 열심히 일하고 있어요.
        
        * **인사팀장 (FSH):** 생리 때 잠든 난자를 깨우는 **'기상 나팔'** 🎺
        * **홍보이사 (에스트로겐):** 생리 후 피부와 기분을 좋게 만드는 **'미모 담당'** ✨
        * **이벤트팀장 (LH):** 배란일에 난자를 내보내는 **'폭죽 담당'** 🎉
        * **보안팀장 (프로게스테론):** 배란 후 몸을 붓게 하고 지키는 **'방어 담당'** 🛡️
        """)

    # [통합요약]
    with st.expander(" ⬇ 이번 달 요약 미리보기 (Click)"):
        st.markdown("""
        * **📉 생리기 (1~5일):** "파업 & 대청소 중" ➡️ 푹 쉬고 물 많이 드세요.
        * **📈 난포기 (6~13일):** "황금기 & 리즈 갱신" ➡️ 다이어트, 고기능성 화장품, 시술 OK! ✨
        * **🚩 배란기 (14~16일):** "파티 & 개기름 주의" ➡️ 매력적이지만 피지 조심하세요.
        * **🛡️ 황체기 (17~28일):** "방어 모드 & 존버" ➡️ 자외선 차단 필수, 트러블 손대지 마세요.
        """)

    # --- 구간별 스토리텔링 시작 ---

    # 1. 생리기 (Day 1 ~ 5)
    if 1 <= day <= 5:
        st.error(f"### 🩸 1. 생리기: 대청소 & 휴식 기간 (Day {day})")
        
        if day <= 2:
            st.markdown("#### 🚨 1단계: 폭풍의 시작 (Day 1~2)")
            st.markdown("**🧖‍♀️ [피부팀 보고]** 방어막이 약해져서 엄청 예민하고 건조해요. 기능성 화장품 금지!")
            
            st.write("---")
            # [수정] 박스로 통일
            st.success(f"☀️ 아침: {common_morning}")
            st.info(f"🌙 저녁: {make_routine(['토너', '💧디오디너리 히알루론산', '🛡️마데카/시카밤(듬뿍)'])}")
            
        elif day <= 4:
            st.markdown("#### 🧹 2단계: 조금씩 살아나는 중 (Day 3~4)")
            st.markdown("**🧖‍♀️ [피부팀 보고]** 트러블은 가라앉았지만 푸석푸석해요. 물을 주세요!")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.info(f"🌙 저녁: {make_routine(['토너', '🧖‍♀️수분 마스크팩', '💧디오디너리 히알루론산', '🛡️마데카/시카밤'])}")
            
        else: # Day 5
            st.markdown("#### 🌱 3단계: 황금기 준비 (Day 5)")
            st.markdown("**🧖‍♀️ [피부팀 보고]** 묵은 각질을 살살 청소하고, 미백 앰플을 꺼내두세요.")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.info(f"🌙 저녁: {make_routine(['📍효소파우더', '토너', '💧디오디너리 히알루론산', '🛡️마데카/시카밤'])}")

    # 2. 난포기 (Day 6 ~ 13)
    elif 6 <= day <= 13:
        st.success(f"### 📈 2. 난포기: 황금기 & 리즈 갱신 (Day {day})")
        st.caption("🏢 현재 상황: 에스트로겐(미모 담당)이 출근해서 지원금을 펑펑 쓰고 있어요! ✨")

        # 일자별 상세 루틴
        if day == 6:
            st.markdown("#### 🚀 Day 6: 코스알엑스 비타민C 23 (잡티 완화)")
            st.write("**목표:** 칙칙했던 얼굴에 고농도 비타민 투여! (약간 따가울 수 있음)")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.warning(f"🌙 저녁: {make_routine(['토너', '🍋코스알엑스 비타민C', '🧖‍♀️토리든 마스크팩', '🛡️마데카/시카밤'])}")
            
        elif day == 7:
            st.markdown("#### 🚀 Day 7: 디오디너리 알부틴 + 기기 (톤 정리)")
            st.write("**목표:** 뷰티 디바이스가 있다면 오늘이 기회입니다. 알부틴을 피부 깊숙이 밀어 넣으세요.")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.warning(f"🌙 저녁: {make_routine(['토너', '💧디오디너리 히알루론산', '💡디오디너리 알부틴(+기기먼저)', '🛡️마데카/시카밤'])}")
            
        elif day == 8:
            st.markdown("#### 🚀 Day 8: VT 리들샷 300 (재생, 길 뚫기)")
            st.write("**목표:** 회복력이 좋을 때라 따가운 니들샷 쓰기 딱 좋습니다. (비타민C 금지)")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.warning(f"🌙 저녁: {make_routine(['⚡VT 리들샷(맨얼굴)', '토너', '💧디오디너리 히알루론산', '🛡️시카밤(듬뿍)'])}")
            
        elif day == 9:
            st.markdown("#### 🚀 Day 9: 나이아신아마이드 (모공 쫀쫀)")
            st.write("**목표:** 건조하지 않게 모공 관리하기. (앰플 단독 사용 X, 크림에 섞어서!)")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.warning(f"🌙 저녁: {make_routine(['토너', '💧디오디너리 히알루론산', '🧴크림+나이아신 믹스', '크림 한겹 더'])}")
            
        else: # Day 10~13
            st.markdown("#### ✨ 2단계: 물광 코팅 (Day 10~13)")
            st.write("**👉 전략:** 곧 다가올 배란기(개기름)에 대비해서, **유수분 밸런스**를 맞춰두는 시기입니다.")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.warning(f"🌙 저녁: {make_routine(['토너', '💧디오디너리 히알루론산', '🧖‍♀️수분 마스크팩', '🛡️마데카 크림'])}")

    # 3. 배란기 & 체제 전환 (Day 14 ~ 16)
    elif 14 <= day <= 16:
        st.warning(f"### 🎉 3. 배란기: 화려한 파티 & 피지 주의보 (Day {day})")
        
        if day == 14:
            st.caption("🏢 현재 상황: 난자(신제품) 출시 파티 중! 폭죽 터지고 난리 났어요.")
            st.markdown("#### 🚨 오늘 미션: 개기름 청소 & 열 내리기 (머드팩 금지)")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.warning(f"🌙 저녁: {make_routine(['오일클렌징(코 집중)', '토너', '🧊토리든 마스크팩', '프리메이 수분크림'])}")
            
        else: # Day 15~16
            st.caption("🧹 파티 끝! 열 식히는 중")
            st.success("✅ **추천:** 알로에 젤이나 차가운 토너로 얼굴 온도 낮추기")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.warning(f"🌙 저녁: {make_routine(['🧊차가운 토너(닥토)', '💧디오디너리 히알루론산', '알로에/프리메이', '🛡️시카밤(얇게)'])}")

    # 4. 황체기 (Day 17 ~ 28)
    else:
        st.info(f"### 🛡️ 4. 황체기: 방어 모드 & 존버 (Day {day})")
        st.caption("👮‍♂️ 현재 상황: 보안팀장이 문 잠그고 비상식량(수분, 지방) 쟁여두는 중.")
    

        if day <= 22:
            st.markdown("#### 🧱 1단계: 햇빛 & 건조 방어 (Day 17~22)")
            st.write("기미가 생기기 쉽고 피부가 거칠어지는 시기입니다.")
            st.markdown("**🧖‍♀️ [피부팀 전략]** 선크림 꼼꼼히! 건조하면 **페이스 오일(프로폴리스 밤)** 수시로 덧바르기.")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.info(f"🌙 저녁: {make_routine(['토너', '💧디오디너리 히알루론산 / 토리든+디바이스(흡수모드)','🛡️마데카/세타필'])}")
            
        else: # Day 23~28
            st.markdown("#### 🚨 2단계: 폭동 전야 (생리 전) (Day 23~28)")
            st.markdown("**🧖‍♀️ [피부팀 긴급 지침]** 화장품 단계 최소화! 붉은 거 올라오면 패치 붙이고 끝.")
            
            st.write("---")
            st.success(f"☀️ 아침: {common_morning}")
            st.error(f"🌙 저녁: {make_routine(['약산성 세안', '토너', '🛡️시카밤(두껍게)+디바이스(초음파모드,1회)', '트러블패치'])}")

    # 공통 하단 메시지
    st.divider()
    st.caption("💪 오늘도 내 몸 주식회사의 CEO로서 파이팅하세요!")

# --- 3. 메인 실행 화면 ---

saved_date = load_date()

# 사이드바 설정 부분
# --- [수정] 사이드바 설정 부분 ---
with st.sidebar:
    st.header("⚙️ 설정 (My Room)")
    
    # 1. 날짜 설정
    if saved_date:
        st.write(f"📅 마지막 생리 시작일: `{saved_date}`")
    
    new_date = st.date_input("날짜 수정하기", 
                             value=datetime.datetime.strptime(saved_date, "%Y-%m-%d").date() if saved_date else datetime.date.today())
    
    if st.button("날짜 저장"):
        save_date(str(new_date))
        st.success("저장 완료! 새로고침됩니다.")
        st.rerun()

    st.divider() # 구분선

    # 2. [추가됨] 디바이스 스케줄 (접이식 메뉴)
    st.subheader("🗓️ 디바이스 결재판")
    
    # expanded=False로 하면 처음에 접혀있어서 깔끔합니다.
    with st.expander("📡 초음파 모드 월간 계획표 (Click)", expanded=False):
        st.markdown("""
        **1주차 (Day 1~5) : 생리기**
        > ⛔ **[휴업]** > 피부 장벽이 가장 약해요. 기기 사용을 **완전히 쉽니다.**
        
        **2주차 (Day 6~13) : 난포기**
        > ✅ **[황금기 결재]** > 회복력 최고조! **탄력 개선 효과**가 가장 좋은 시기입니다. (1회)
        
        **3주차 (Day 14~20) : 배란~황체**
        > 💆‍♀️ **[집중 관리]** > 피부가 거칠어질 때입니다. **영양 공급**을 위해 사용하세요. (1회)
        
        **4주차 (Day 21~28) : 생리 전**
        > ⚠️ **[조건부 결재]** > 트러블이 올라오면 **PASS**, 괜찮으면 가볍게 진행합니다. (0~1회)
        """)
        
    st.caption("※ 초음파는 주 1~2회 권장")

# 메인 로직 실행
if saved_date:
    current_day = calculate_cycle_day(saved_date)
    
    
    if current_day:
        display_dry_skin_habit() # 상시 지침 (건성)
        display_hormone_guide(current_day) # 오늘의 리포트
    else:
        st.error("시스템 오류: 날짜 형식을 확인하세요.")
else:
    st.warning("👈 왼쪽 메뉴에서 '마지막 생리 시작일'을 입력하고 저장을 눌러주세요!")