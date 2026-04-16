import streamlit as st
from datetime import date, timedelta
import random
import pandas as pd

# ====================== 頁面設定 ======================
st.set_page_config(
    page_title="戒得掂",
    page_icon="🚭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 樣式
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
h1, h2, h3 {
    color: white !important;
}
.stButton>button {
    background: linear-gradient(45deg, #FF6B6B, #FF8E53);
    color: white;
    border-radius: 20px;
    font-weight: bold;
    padding: 10px 20px;
}
.card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ====================== 初始化狀態 ======================
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'check_in' not in st.session_state:
    st.session_state.check_in = False
if 'check_in_streak' not in st.session_state:
    st.session_state.check_in_streak = 0
if 'last_check_in' not in st.session_state:
    st.session_state.last_check_in = date.today() - timedelta(days=1)
if 'game_level' not in st.session_state:
    st.session_state.game_level = 1
if 'challenge_done' not in st.session_state:
    st.session_state.challenge_done = False
if 'quit_start_date' not in st.session_state:
    st.session_state.quit_start_date = date.today()
if 'cigs_per_day' not in st.session_state:
    st.session_state.cigs_per_day = 0
if 'price_per_pack' not in st.session_state:
    st.session_state.price_per_pack = 58  # 香港常見售價約58港幣/包

if 'craving_count' not in st.session_state:
    st.session_state.craving_count = 0

if 'friends' not in st.session_state:
    st.session_state.friends = [
        {"name": "小明", "points": 250, "quit_days": 15},
        {"name": "阿詩", "points": 320, "quit_days": 20},
        {"name": "阿強", "points": 180, "quit_days": 10},
        {"name": "你自己", "points": st.session_state.points, "quit_days": (date.today() - st.session_state.quit_start_date).days}
    ]

# ====================== 更新排行榜 ======================
def update_friend_rank():
    for friend in st.session_state.friends:
        if friend["name"] == "你自己":
            friend["points"] = st.session_state.points
            friend["quit_days"] = max(0, (date.today() - st.session_state.quit_start_date).days)

# ====================== 標題 ======================
st.title("🚭 戒得掂 · 青少年拒煙大作戰")
st.markdown("### 玩住戒煙，型到爆！同朋友一齊挑戰！")

# ====================== 分頁 ======================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 戒煙日誌",
    "🚬 吸煙危害",
    "🎮 拒煙遊戲",
    "💪 煙癮對抗",
    "🏆 積分商城",
    "👥 好友排名",
    "🆘 一鍵求助"
])

# ====================== 1. 戒煙日誌 ======================
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📅 我的戒煙日誌")

    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("戒煙開始日期", value=st.session_state.quit_start_date)
        st.session_state.quit_start_date = start_date
    with col2:
        cigs_per_day = st.number_input("每日食幾多支煙", min_value=0, value=st.session_state.cigs_per_day)
        st.session_state.cigs_per_day = cigs_per_day
    with col3:
        # 香港定價，只顯示唔可修改
        st.session_state.price_per_pack = 58
        st.info(f"每包煙固定價錢：HK$ {st.session_state.price_per_pack}（香港常見售價）")

    today = date.today()
    if st.session_state.last_check_in < today:
        if st.button("今日打卡 ✅"):
            st.session_state.check_in = True
            st.session_state.last_check_in = today
            st.session_state.check_in_streak += 1
            bonus = st.session_state.check_in_streak * 5
            st.session_state.points += 20 + bonus
            st.balloons()
            st.success(f"打卡成功！加{20+bonus}分！連續{st.session_state.check_in_streak}日！")
            update_friend_rank()
    else:
        st.info(f"今日已打卡！連續{st.session_state.check_in_streak}日！")

    if start_date <= today:
        days = (today - start_date).days
        total_cigs = cigs_per_day * days
        packs = total_cigs / 20  # 20支/包
        saved = round(packs * st.session_state.price_per_pack, 2)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("戒煙天數", f"{days} 日")
        with col_b:
            st.metric("慳返金錢", f"HK$ {saved}")
        with col_c:
            st.metric("累積積分", f"{st.session_state.points}")

        st.subheader("✨ 身體變化")
        if days >= 30:
            st.success("滿級狀態！皮膚靚、精神好！")
        elif days >=7:
            st.success("心肺回升！跑跳更輕鬆！")
        elif days >=1:
            st.success("血氧回升，味覺返返嚟！")
        else:
            st.info("今日開始戒煙，身體即刻回血！")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 2. 吸煙危害 ======================
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚬 吸煙真樣 · 唔好呃自己")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ 唔食煙")
        st.markdown("""
        <div style='background:rgba(0,200,0,0.2);padding:20px;border-radius:15px'>
        <h3>皮膚白淨</h3><h3>牙齒乾淨</h3><h3>氣息清新</h3>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.subheader("❌ 食煙之後")
        st.markdown("""
        <div style='background:rgba(200,0,0,0.2);padding:20px;border-radius:15px'>
        <h3>皮膚暗黃</h3><h3>牙黃口臭</h3><h3>樣子蒼老</h3>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.subheader("🫁 肺部對比")
    st.markdown("""
    <div style='display:flex;gap:20px'>
        <div style='background:rgba(0,200,0,0.2);flex:1;padding:15px;border-radius:15px'>
        <h4>健康肺</h4><p>粉紅、乾淨、呼吸順暢</p>
        </div>
        <div style='background:rgba(200,0,0,0.2);flex:1;padding:15px;border-radius:15px'>
        <h4>吸煙肺</h4><p>黑色、焦油堆積、易咳氣喘</p>
        </div>
    </div>""", unsafe_allow_html=True)

    st.divider()
    st.subheader("青少年影響")
    st.warning("❌ 身高發育受影響")
    st.warning("❌ 體力差、容易喘氣")
    st.warning("❌ 皮膚差、暗瘡多、樣子老")
    st.warning("❌ 專注力下降、讀書受影響")
    st.warning("❌ 口臭牙黃，朋友唔想靠近")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 3. 拒煙遊戲（答案100%正確） ======================
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"🎮 拒煙闖關 · 第 {st.session_state.game_level} 關")
    st.info("見到煙就拒絕，健康就接受！")

    scenes = [
        ("同學遞煙畀你：試下啦，好爽㗎", "拒絕"),
        ("朋友叫你試一口：淨係一口唔會上癮", "拒絕"),
        ("派對有人派煙：唔食就唔俾面", "拒絕"),
        ("提議一齊去打籃球", "接受"),
        ("叫你去行山放鬆", "接受"),
        ("食健康水果小食", "接受"),
        ("同學邀請一齊打機", "接受"),
        ("有人話食煙先至型", "拒絕")
    ]

    scene, correct = random.choice(scenes)
    st.subheader(f"場景：{scene}")

    colA, colB = st.columns(2)
    with colA:
        if st.button("❌ 拒絕"):
            if correct == "拒絕":
                st.success("答對！+10分")
                st.session_state.points +=10
            else:
                st.error("答錯！健康活動唔好拒絕")
            update_friend_rank()
    with colB:
        if st.button("✅ 接受"):
            if correct == "接受":
                st.success("答對！+10分")
                st.session_state.points +=10
            else:
                st.error("答錯！唔好食煙！")
            update_friend_rank()

    st.metric("積分", st.session_state.points)
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 4. 煙癮對抗 ======================
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💪 煙癮對抗挑戰")
    if st.button("我頂住咗！成功對抗煙癮 ✅"):
        st.session_state.craving_count +=1
        st.session_state.points +=15
        st.success(f"第 {st.session_state.craving_count} 次對抗成功！+15分")
        st.balloons()
        update_friend_rank()
    st.metric("成功對抗次數", st.session_state.craving_count)

    st.subheader("今日健康任務")
    tasks = [
        "🏃 運動15分鐘",
        "💧 飲夠水",
        "😴 早啲休息",
        "🍎 食蔬果",
        "🧘 煙癮來時深呼吸"
    ]
    done = 0
    for i, t in enumerate(tasks):
        if st.checkbox(t, key=f"t{i}"):
            done +=1
    if done > 0 and not st.session_state.challenge_done:
        st.session_state.points += done*5
        st.session_state.challenge_done = True
        st.success(f"完成{done}項！+{done*5}分！")
        update_friend_rank()
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 5. 積分商城 ======================
with tab5:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏆 積分兌換")
    st.metric("你嘅積分", st.session_state.points)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("🎮 50分：遊戲優惠券")
        if st.button("兌換 50分"):
            if st.session_state.points >=50:
                st.session_state.points -=50
                st.success("兌換成功！")
    with col2:
        st.write("☕ 30分：咖啡買一送一")
        if st.button("兌換 30分"):
            if st.session_state.points >=30:
                st.session_state.points -=30
                st.success("兌換成功！")
    with col3:
        st.write("🏅 100分：拒煙小勇士證書")
        if st.button("兌換 100分"):
            if st.session_state.points >=100:
                st.session_state.points -=100
                st.success("恭喜！你係拒煙小勇士！")
    update_friend_rank()
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 6. 好友排行榜 ======================
with tab6:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👥 好友戒煙排行榜")
    update_friend_rank()
    df = pd.DataFrame(st.session_state.friends)
    df = df.sort_values(by=["points","quit_days"], ascending=False)
    df.index = range(1, len(df)+1)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 求助 ======================
with tab7:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🆘 頂唔順？即刻求助")
    st.warning("衛生署戒煙熱線：1833 183")
    st.info("戒煙網上診所：quitnow.gov.hk")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 頁腳 ======================
st.divider()
st.caption("戒得掂 · 青少年拒煙APP · 玩住戒煙最型")
