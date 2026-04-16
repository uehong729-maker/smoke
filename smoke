import streamlit as st
from datetime import datetime, date

st.set_page_config(
    page_title="戒得掂",
    page_icon="🚭",
    layout="wide"
)

st.title("🚭 戒得掂 — 青少年拒煙戒煙助手")
st.markdown("### 香港專用 · 衛生署資訊 · 簡單實用")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "煙害知識庫",
    "拒煙訓練",
    "戒煙日誌",
    "一鍵求助",
    "健康挑戰"
])

# ------------------------------
# 1. 煙害知識庫
# ------------------------------
with tab1:
    st.subheader("📘 香港衛生署 · 煙害知識")
    st.info("""
    1. 香煙含有尼古丁、焦油、一氧化碳等超過7000種有害物質，尼古丁會令大腦上癮。
    2. 青少年吸煙會影響腦部發育、心肺功能、身高同記憶力，容易引起哮喘同皮膚問題。
    3. 香港法例禁止向18歲以下人士售煙，校園同室內公眾地方全面禁煙。
    4. 二手煙、三手煙同樣有害，會增加呼吸道疾病同免疫力下降風險。
    """)

# ------------------------------
# 2. 拒煙訓練
# ------------------------------
with tab2:
    st.subheader("🎯 拒煙訓練營")

    with st.expander("常見場景模擬"):
        st.write("""
        - 同學遞煙：「一齊試下啦」
        - 朋友慫恿：「淨係一口唔會上癮」
        - 聚會壓力：「人哋都食，你唔好咁孤寒」
        """)

    with st.expander("實用拒絕口訣"):
        st.success("❌ 唔使啦，我唔吸煙！")
        st.success("❌ 吸煙傷身，我唔想搞壞身體！")
        st.success("❌ 校園禁煙，犯法㗎！")
        st.success("❌ 我想健康啲，你都唔好食啦！")

    with st.expander("壓力應對技巧"):
        st.write("""
        - 即刻離開現場
        - 搵老師、家人傾計
        - 做運動、深呼吸
        - 用口香糖、水代替煙癮
        """)

# ------------------------------
# 3. 戒煙日誌
# ------------------------------
with tab3:
    st.subheader("📅 戒煙日誌")

    start_date = st.date_input("選擇戒煙開始日期")
    cigs_per_day = st.number_input("每日食幾多支煙", min_value=0, value=5)
    price_per_pack = st.number_input("每包煙價錢 (HK$)", min_value=0, value=80)

    if start_date <= date.today():
        delta = date.today() - start_date
        days = delta.days

        # 計算慳返嘅錢
        total_cigs = cigs_per_day * days
        packs = total_cigs / 20
        saved = round(packs * price_per_pack, 2)

        st.metric("戒煙天數", f"{days} 日")
        st.metric("慳返金錢", f"HK$ {saved}")

        # 身體變化
        st.subheader("身體改善狀態")
        if days == 0:
            st.info("今日開始戒煙，身體開始恢復！")
        elif 1 <= days < 7:
            st.success("血氧回升，咳嗽減少，味覺開始恢復")
        elif 7 <= days < 30:
            st.success("心肺功能提升，呼吸順暢，精神變好")
        elif days >= 30:
            st.success("戒煙成效明顯，氣喘減少，皮膚同精神全面改善")
    else:
        st.warning("請選擇今日或之前嘅日期")

# ------------------------------
# 4. 一鍵求助
# ------------------------------
with tab4:
    st.subheader("🆘 一鍵戒煙求助")
    st.warning("☎ 香港衛生署戒煙熱線：*1833 183*")
    st.info("🌐 衛生署戒煙網上診所：quitnow.gov.hk")
    st.code("戒煙求助：1833 183")

# ------------------------------
# 5. 健康挑戰
# ------------------------------
with tab5:
    st.subheader("💪 健康挑戰 · 用健康代替吸煙")
    st.checkbox("每日運動15分鐘")
    st.checkbox("每晚睡足8小時")
    st.checkbox("飲充足開水，多吃蔬果")
    st.checkbox("想吸煙時嚼無糖口香糖")
    st.checkbox("遠離吸煙朋友同場地")

    st.success("完成7日挑戰 → 獲封「拒煙小勇士」")

st.divider()
st.caption("戒得掂 · 香港青少年戒煙APP · 預防為先 · 健康至上")
