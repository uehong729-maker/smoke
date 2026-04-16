import streamlit as st
from datetime import datetime, date
import random

st.set_page_config(page_title="戒得掂", page_icon="🚭", layout="wide")

# 靚啲嘅風格
st.markdown("""
<style>
.stButton>button {
    border-radius: 16px;
    background-color: #ff4d4d;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 積分同打卡
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'check_in' not in st.session_state:
    st.session_state.check_in = False

# 分頁
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚬 吸煙真樣圖集",
    "🎮 拒煙小遊戲",
    "📅 戒煙打卡",
    "🏆 積分獎勵",
    "🆘 一鍵求助",
    "💪 健康任務"
])

# ------------------------------
# 【新頁面】吸煙樣子 + 身體影響圖片
# ------------------------------
with tab1:
    st.title("🚬 吸煙真樣 · 唔好呃自己")

    st.subheader("1. 吸煙前 vs 吸煙後 樣貌變化")
    # 皮膚、牙齒、皺紋對比
    st.image("https://i.imgur.com/8dXzHtZ.jpg", caption="吸煙令皮膚暗黃、皺紋增多、牙齒變黃")
    st.image("https://i.imgur.com/aU1dFjm.jpg", caption="長期吸煙樣貌明顯蒼老好多")

    st.divider()

    st.subheader("2. 吸煙對身體內部嘅破壞")
    st.image("https://i.imgur.com/2qNxVYF.png", caption="正常肺 🫁 vs 吸煙者嘅肺 🚬")
    st.image("https://i.imgur.com/Ct5hBCl.png", caption="心臟、血管、大腦都會受損")

    st.divider()

    st.subheader("3. 青少年最慘嘅影響（超直白）")
    st.warning("❌ 身高唔高、體力差、跑兩步就氣喘")
    st.warning("❌ 皮膚差、暗瘡多、樣子老幾年")
    st.warning("❌ 記性差、專注力下降、讀書成績受影響")
    st.warning("❌ 口臭、牙黃、異味，朋友唔想靠近")
    st.warning("❌ 上癮後人生被尼古丁控制")

# ------------------------------
# 拒煙小遊戲
# ------------------------------
with tab2:
    st.title("🎮 拒煙反應遊戲")
    st.write("見到煙就拒絕，見到健康就接受！")

    scene = random.choice([
        ("同學遞煙畀你","拒絕煙"),
        ("朋友叫你試一口","拒絕煙"),
        ("有人話食煙先型","拒絕煙"),
        ("提議去打籃球","接受健康"),
        ("叫你一齊去行山","接受健康"),
        ("食水果小食","接受健康")
    ])

    st.subheader(f"場景：{scene[0]}")
    colA, colB = st.columns(2)

    with colA:
        if st.button("❌ 拒絕"):
            if scene[1] == "拒絕煙":
                st.success("正確！+10分")
                st.session_state.points +=10
            else:
                st.error("錯咗！健康活動唔好拒絕")

    with colB:
        if st.button("✅ 接受"):
            if scene[1] == "接受健康":
                st.success("正確！+10分")
                st.session_state.points +=10
            else:
                st.error("錯咗！唔好食煙！")

# ------------------------------
# 戒煙打卡
# ------------------------------
with tab3:
    st.title("📅 戒煙打卡日記")

    if st.button("今日打卡 ✅") and not st.session_state.check_in:
        st.session_state.check_in = True
        st.session_state.points += 20
        st.success("打卡成功！+20分 🎉")
        st.balloons()

    start_date = st.date_input("戒煙開始日期")
    if start_date <= date.today():
        days = (date.today() - start_date).days
        st.metric("戒煙天數", f"{days} 日")
        st.metric("積分", st.session_state.points)

# ------------------------------
# 積分獎勵
# ------------------------------
with tab4:
    st.title("🏆 積分兌換")
    st.metric("你而家有", f"{st.session_state.points} 分")

    if st.button("30分 → 虛擬證書"):
        if st.session_state.points >=30:
            st.success("兌換成功！你係拒煙小勇士 🌟")
            st.session_state.points -=30

    if st.button("50分 → 健康頭像框"):
        if st.session_state.points >=50:
            st.success("成功獲得健康專屬頭像框！")
            st.session_state.points -=50

# ------------------------------
# 一鍵求助
# ------------------------------
with tab5:
    st.title("🆘 頂唔順就求助")
    st.warning("衛生署戒煙熱線：*1833 183*")
    st.info("網上戒煙診所：quitnow.gov.hk")

# ------------------------------
# 健康任務
# ------------------------------
with tab6:
    st.title("💪 每日健康任務")
    st.checkbox("🏃 運動15分鐘")
    st.checkbox("💧 飲夠水")
    st.checkbox("😴 早啲訓")
    st.checkbox("🍎 食蔬果")
    st.checkbox("🧘 想食煙就深呼吸")
    st.success("完成全部 → 自動獲得15分！")

st.caption("戒得掂 · 青少年拒煙APP · 玩住戒煙最型")
