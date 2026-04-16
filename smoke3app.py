import streamlit as st
from datetime import datetime, date, timedelta
import random
import pandas as pd

# ====================== 頁面高級設定 ======================
st.set_page_config(
    page_title="戒得掂",
    page_icon="🚭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 高級自訂CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
h1, h2, h3 {
    color: white !important;
    font-weight: 800 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}
.stButton>button {
    background: linear-gradient(45deg, #FF6B6B, #FF8E53) !important;
    color: white !important;
    border-radius: 25px !important;
    font-weight: bold !important;
    border: none !important;
    padding: 12px 24px !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
}
.stButton>button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
}
.card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    border: 1px solid rgba(255, 255, 255, 0.18);
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.1);
    border-radius: 15px 15px 0 0;
    color: white !important;
    font-weight: bold;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.3) !important;
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
    st.session_state.price_per_pack = 0
if 'craving_count' not in st.session_state:
    st.session_state.craving_count = 0
if 'friends' not in st.session_state:
    st.session_state.friends = [
        {"name": "小明", "points": 250, "quit_days": 15},
        {"name": "阿詩", "points": 320, "quit_days": 20},
        {"name": "阿強", "points": 180, "quit_days": 10},
        {"name": "你自己", "points": st.session_state.points, "quit_days": (date.today() - st.session_state.quit_start_date).days}
    ]
if 'achievements' not in st.session_state:
    st.session_state.achievements = {
        "7日堅持": False,
        "30日王者": False,
        "積分達人": False,
        "拒煙大師": False
    }

# ====================== 更新好友排行榜數據 ======================
def update_friend_rank():
    for friend in st.session_state.friends:
        if friend["name"] == "你自己":
            friend["points"] = st.session_state.points
            friend["quit_days"] = (date.today() - st.session_state.quit_start_date).days

# ====================== 首頁標題 ======================
st.title("🚭 戒得掂 · 青少年拒煙大作戰")
st.markdown("### 玩住戒煙，型到爆！同朋友一齊挑戰！")

# ====================== 分頁設定 ======================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 戒煙日誌",
    "🚬 吸煙危害圖集",
    "🎮 拒煙闖關遊戲",
    "💪 煙癮對抗",
    "🏆 積分商城",
    "👥 好友排行榜",
    "🆘 一鍵求助"
])

# ====================== 1. 戒煙日誌（保留計算+升級） ======================
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📅 我的戒煙日誌")
    
    # 輸入資訊
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("選擇戒煙開始日期", value=st.session_state.quit_start_date)
        st.session_state.quit_start_date = start_date
    with col2:
        cigs_per_day = st.number_input("每日吸煙數量（支）", min_value=0, value=st.session_state.cigs_per_day)
        st.session_state.cigs_per_day = cigs_per_day
    with col3:
        price_per_pack = st.number_input("每包香煙價格（HK$）", min_value=0, value=st.session_state.price_per_pack)
        st.session_state.price_per_pack = price_per_pack

    # 連續打卡功能
    today = date.today()
    if st.session_state.last_check_in < today:
        if st.button("今日打卡 ✅", key="checkin_btn"):
            st.session_state.check_in = True
            st.session_state.last_check_in = today
            if (today - st.session_state.last_check_in).days == 1:
                st.session_state.check_in_streak += 1
            else:
                st.session_state.check_in_streak = 1
            # 連續打卡獎勵
            streak_bonus = st.session_state.check_in_streak * 5
            st.session_state.points += 20 + streak_bonus
            st.balloons()
            st.success(f"🎉 打卡成功！加{20 + streak_bonus}分！連續打卡{st.session_state.check_in_streak}日！")
            update_friend_rank()
    else:
        st.info(f"📌 今日已經打卡啦！連續打卡{st.session_state.check_in_streak}日！聽日再嚟！")

    # 計算數據
    if start_date <= date.today():
        delta = date.today() - start_date
        days = delta.days
        total_cigs = cigs_per_day * days
        packs = total_cigs / 20
        saved = round(packs * price_per_pack, 2)

        # 數據卡片
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("📅 戒煙天數", f"{days} 日")
        with col_b:
            st.metric("💰 節省金錢", f"HK$ {saved}")
        with col_c:
            st.metric("🏆 累積積分", f"{st.session_state.points} 分")

        # 身體改善
        st.subheader("✨ 身體升級進度")
        if days == 0:
            st.info("💪 今日開始戒煙，身體即刻回血！")
        elif 1 <= days < 7:
            st.success("🫁 血氧回升！跑樓梯唔再氣喘！味覺開始恢復！")
        elif 7 <= days < 30:
            st.success("🏃 心肺升級！打波勁到爆！精神狀態滿格！")
        elif days >= 30:
            st.success("🌟 滿級狀態！皮膚靚、記憶力好，同煙講永別！")

        # 成就解鎖
        st.subheader("🏅 我的成就")
        if days >= 7 and not st.session_state.achievements["7日堅持"]:
            st.session_state.achievements["7日堅持"] = True
            st.session_state.points += 50
            st.success("🎉 解鎖成就：7日堅持！加50分！")
        if days >= 30 and not st.session_state.achievements["30日王者"]:
            st.session_state.achievements["30日王者"] = True
            st.session_state.points += 200
            st.success("🎉 解鎖成就：30日王者！加200分！")
        if st.session_state.points >= 500 and not st.session_state.achievements["積分達人"]:
            st.session_state.achievements["積分達人"] = True
            st.success("🎉 解鎖成就：積分達人！")
        update_friend_rank()
    else:
        st.warning("⚠️ 請選擇今日或之前嘅日期")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 2. 吸煙危害圖集（穩定圖片） ======================
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚬 吸煙真樣 · 唔好呃自己")

    # 樣貌變化
    st.subheader("1. 吸煙前 vs 吸煙後 樣貌對比")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://cdn.pixabay.com/photo/2019/03/12/13/37/smoking-4050771_1280.jpg", 
                 caption="長期吸煙令皮膚暗黃、皺紋增多、樣子蒼老", use_column_width=True)
    with col2:
        st.image("https://cdn.pixabay.com/photo/2017/08/07/13/32/stop-smoking-2604636_1280.jpg", 
                 caption="牙齒變黃、口臭，影響社交同形象", use_column_width=True)

    st.divider()

    # 器官損傷
    st.subheader("2. 吸煙對身體內部嘅毀滅性破壞")
    col3, col4 = st.columns(2)
    with col3:
        st.image("https://cdn.pixabay.com/photo/2017/08/07/13/32/stop-smoking-2604637_1280.jpg", 
                 caption="正常肺 vs 吸煙者嘅肺，差天共地", use_column_width=True)
    with col4:
        st.image("https://cdn.pixabay.com/photo/2018/03/10/15/07/heart-3214361_1280.png", 
                 caption="心臟、血管、大腦全面受損", use_column_width=True)

    st.divider()

    # 青少年危害
    st.subheader("3. 青少年吸煙最慘嘅後果")
    st.warning("❌ 身高唔高、體力差，跑兩步就氣喘")
    st.warning("❌ 皮膚差、暗瘡多，樣子老幾年，靚仔靚女變路人")
    st.warning("❌ 記性差、專注力下降，讀書成績直線下滑")
    st.warning("❌ 口臭、牙黃、異味，朋友唔想靠近")
    st.warning("❌ 上癮後人生被尼古丁控制，想戒都戒唔到")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 3. 拒煙闖關遊戲（修復語法錯誤） ======================
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"🎮 拒煙闖關大挑戰 · 第 {st.session_state.game_level} 關")
    st.info("考你反應！見到煙就拒絕，見到健康就接受！通關有大獎！")

    # 正確場景列表（修復括號錯誤）
    scenes = [
        ("同學遞煙畀你：「試下啦，好爽㗎」", "拒絕"),
        ("朋友慫恿：「淨係一口唔會上癮」", "拒絕"),
        ("派對有人派煙：「唔食就唔俾面」", "拒絕"),
        ("提議去打籃球：「一齊去波樓」", "接受"),
        ("叫你去行山：「週末一齊去行山啦」", "接受"),
        ("食健康小食：「呢個水果好正」", "接受"),
        ("同學叫你一齊打機放鬆", "接受"),
        ("有人話「食煙先型，唔食係乸型」", "拒絕")
    ]
    scene, correct = random.choice(scenes)

    st.subheader(f"場景：{scene}")
    colA, colB = st.columns(2)

    with colA:
        if st.button("❌ 拒絕", key="refuse_btn"):
            if correct == "拒絕":
                st.success("✅ 答對！加10分！")
                st.session_state.points += 10
                if st.session_state.points >= st.session_state.game_level * 50:
                    st.session_state.game_level += 1
                    st.success(f"🎉 通關！進入第 {st.session_state.game_level} 關！")
                    st.balloons()
            else:
                st.error("❌ 答錯！健康活動唔好拒絕！扣5分！")
                st.session_state.points = max(0, st.session_state.points - 5)
            update_friend_rank()
    with colB:
        if st.button("✅ 接受", key="accept_btn"):
            if correct == "接受":
                st.success("✅ 答對！加10分！")
                st.session_state.points += 10
                if st.session_state.points >= st.session_state.game_level * 50:
                    st.session_state.game_level += 1
                    st.success(f"🎉 通關！進入第 {st.session_state.game_level} 關！")
                    st.balloons()
            else:
                st.error("❌ 答錯！唔好食煙！扣5分！")
                st.session_state.points = max(0, st.session_state.points - 5)
            update_friend_rank()

    st.metric("當前積分", f"{st.session_state.points} 分")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 4. 煙癮對抗挑戰 ======================
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💪 煙癮對抗挑戰 · 用健康擊退尼古丁")
    st.info("完成健康任務，賺積分，記錄每次對抗成功！")

    # 煙癮發作倒計時
    st.subheader("🔥 煙癮發作？即刻對抗！")
    if st.button("我頂住咗！✅", key="craving_btn"):
        st.session_state.craving_count += 1
        st.session_state.points += 15
        st.success(f"🎉 成功對抗第 {st.session_state.craving_count} 次煙癮！加15分！")
        st.balloons()
        update_friend_rank()
    st.metric("累積成功對抗煙癮次數", f"{st.session_state.craving_count} 次")

    # 每日任務
    st.subheader("📋 今日健康任務")
    tasks = [
        "🏃 每日運動15分鐘（快走/跳繩）",
        "💧 飲夠2L水，用清水代替煙癮",
        "😴 每晚睡足8小時，唔好捱夜",
        "🍎 多吃蔬果，補充維生素",
        "🧘 想吸煙時做10次深呼吸",
        "🚶 遠離吸煙場所，同朋友去做運動"
    ]

    completed = 0
    for i, task in enumerate(tasks):
        if st.checkbox(task, key=f"task_{i}"):
            completed += 1

    if completed > 0 and not st.session_state.challenge_done:
        reward = completed * 5
        st.session_state.points += reward
        st.session_state.challenge_done = True
        st.success(f"🎉 完成 {completed} 項任務！加 {reward} 分！")
        st.balloons()
        update_friend_rank()
    elif st.session_state.challenge_done:
        st.success("✅ 今日任務已完成！聽日再挑戰！")
        if st.button("🔄 重置任務"):
            st.session_state.challenge_done = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 5. 積分獎勵商城 ======================
with tab5:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏆 積分兌換獎勵")
    st.metric("你嘅累積積分", f"{st.session_state.points} 分")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🎮 50分兌換：遊戲禮物卡優惠券")
        if st.button("立即兌換", key="redeem1"):
            if st.session_state.points >= 50:
                st.session_state.points -= 50
                st.success("✅ 兌換成功！優惠碼：JDD2024GAME")
                update_friend_rank()
            else:
                st.error("❌ 積分唔夠！快啲去玩遊戲賺分！")
    with col2:
        st.info("☕ 30分兌換：連鎖咖啡店買一送一")
        if st.button("立即兌換", key="redeem2"):
            if st.session_state.points >= 30:
                st.session_state.points -= 30
                st.success("✅ 兌換成功！優惠碼：JDD2024COFFEE")
                update_friend_rank()
            else:
                st.error("❌ 積分唔夠！快啲去打卡賺分！")
    with col3:
        st.info("🏅 100分兌換：拒煙小勇士電子證書")
        if st.button("立即兌換", key="redeem3"):
            if st.session_state.points >= 100:
                st.session_state.points -= 100
                st.success("🎉 兌換成功！你係最型嘅拒煙小勇士！")
                st.image("https://cdn.pixabay.com/photo/2017/08/07/13/32/stop-smoking-2604638_1280.jpg", 
                         caption="拒煙小勇士榮譽證書", use_column_width=True)
                update_friend_rank()
            else:
                st.error("❌ 積分唔夠！快啲去挑戰賺分！")

    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 6. 好友排行榜（新增功能） ======================
with tab6:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👥 好友戒煙排行榜")
    st.info("同朋友一齊比賽，邊個戒煙最勁！")

    # 添加好友功能
    st.subheader("➕ 添加好友")
    new_friend_name = st.text_input("輸入好友名稱")
    if st.button("添加好友"):
        if new_friend_name and new_friend_name not in [f["name"] for f in st.session_state.friends]:
            st.session_state.friends.append({
                "name": new_friend_name,
                "points": random.randint(100, 300),
                "quit_days": random.randint(5, 25)
            })
            st.success(f"✅ 成功添加好友：{new_friend_name}！")
            st.rerun()
        else:
            st.error("❌ 名稱無效或好友已存在！")

    # 排行榜數據
    update_friend_rank()
    df = pd.DataFrame(st.session_state.friends)
    df = df.sort_values(by=["points", "quit_days"], ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    df.columns = ["好友名稱", "累積積分", "戒煙天數"]

    st.subheader("🏆 排行榜")
    st.dataframe(df, use_container_width=True)

    # 自己嘅排名
    self_rank = df[df["好友名稱"] == "你自己"].index[0]
    st.info(f"📌 你嘅排名：第 {self_rank} 名！加油衝刺第一名！")

    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 7. 一鍵求助 ======================
with tab7:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🆘 頂唔順？一鍵求助！")
    st.warning("☎ 香港衛生署戒煙熱線：*1833 183*")
    st.info("🌐 戒煙網上診所：https://www.quitnow.gov.hk/")
    if st.button("📞 一鍵複製熱線"):
        st.code("1833 183")
        st.success("✅ 熱線已複製！即刻打電話求助！")

    st.subheader("🔥 煙癮發作？即刻自救")
    st.write("1. 深呼吸10次，緩解渴望")
    st.write("2. 飲大量清水，沖淡煙癮")
    st.write("3. 搵朋友/家人傾計，尋求支持")
    st.write("4. 立即致電戒煙熱線，專人幫你")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== 頁腳 ======================
st.divider()
st.caption("戒得掂 · 香港青少年專屬拒煙APP · 玩住戒煙，健康有型")
