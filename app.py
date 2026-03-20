import streamlit as st
import swisseph as swe
from datetime import datetime, time, timedelta

# --- 1. カラーパレット ---
C_BG = "#F2EAE0"
C_SUB = "#B4D3D9"
C_MAIN = "#BDA6CE"
C_ACCENT = "#9B8EC7"

# --- 2. デザイン (CSS) & ステルス設定 ---
st.set_page_config(page_title="Lagna Blueprint", page_icon="✨")

st.markdown(f"""
    <style>
    /* 基本設定 */
    header[data-testid="stHeader"], footer, #MainMenu {{ display: none !important; }}
    .stAppToolbar {{ display: none !important; }}
    .block-container {{ padding-top: 2rem !important; }}
    .stApp {{ background-color: {C_BG}; }}
    h1, h2, h3, label {{ color: {C_ACCENT} !important; font-weight: bold; }}

    /* 【重要】スマホでの入力文字の色を強制固定（白抜き防止） */
    input, .stSelectbox div[data-baseweb="select"] {{
        color: {C_ACCENT} !important;
        -webkit-text-fill-color: {C_ACCENT} !important;
        background-color: white !important;
    }}
    div[data-baseweb="input"], div[data-baseweb="select"] {{
        background-color: white !important;
    }}

    /* ボタンの設定 */
    .stButton>button {{
        background: linear-gradient(135deg, {C_MAIN}, {C_ACCENT});
        color: white !important; border-radius: 25px; border: none;
        height: 3.5em; width: 100%; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ヘッダー画像の表示 ---
try:
    st.image("Lagna blueprint.png", use_container_width=True)
except:
    st.title("✨ Lagna Blueprint")

# --- 4. 都道府県データ ---
PREFECTURES = {
    "沖縄県": [26.2124, 127.6809], "東京都": [35.6895, 139.6917], "大阪府": [34.6864, 135.5199],
    "愛知県": [35.1802, 136.9066], "福岡県": [33.6064, 130.4182], "北海道": [43.0641, 141.3469],
    "青森県": [40.8244, 140.7400], "鹿児島県": [31.5967, 130.5571]
}

# --- 5. 入力フォーム ---
birth_date = st.date_input("1. 誕生日を選択", value=datetime(1980, 7, 20))
birth_time = st.time_input("2. 出生時刻", value=time(10, 58))
pref_name = st.selectbox("3. 出生地", list(PREFECTURES.keys()))

# --- 6. 鑑定ロジック ---
if st.button("鑑定結果を表示する"):
    try:
        dt_local = datetime.combine(birth_date, birth_time)
        dt_ut = dt_local - timedelta(hours=9)
        jd_ut = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, dt_ut.hour + dt_ut.minute/60.0)

        # サイドリアル（恒星時）計算の強制設定
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        lat, lon = PREFECTURES[pref_name]
        res = swe.houses_ex(jd_ut, lat, lon, b'W', flags=64)
        lagna_deg = res[1][0]

        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        sign_index = int(lagna_deg / 30)
        deg_in_sign = lagna_deg % 30
        sign_name = zodiac_signs[sign_index]

        # 12星座別のアドバイスメッセージ
        messages = {
            "牡羊座": "情熱的で、新しい一歩を踏み出す勇気を持っています。",
            "牡牛座": "穏やかで、心地よい豊かさを育む才能があります。",
            "双子座": "知的好奇心が旺盛で、軽やかに情報を繋ぐ力があります。",
            "蟹座": "共感力が高く、大切な居場所を守り育てる愛を持っています。",
            "獅子座": "堂々とした華やかさと、周囲を照らすリーダーシップがあります。",
            "乙女座":
