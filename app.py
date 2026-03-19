import streamlit as st
import swisseph as swe
from datetime import datetime, time, timedelta

# --- 1. カラーパレットの定義 ---
C_BG = "#F2EAE0"     # 背景（淡いベージュ）
C_SUB = "#B4D3D9"    # 入力欄・アクセント（爽やかな水色）
C_MAIN = "#BDA6CE"   # ボタン・枠線（優しい紫）
C_ACCENT = "#9B8EC7" # タイトル・強調（深い紫）

# --- 2. ページ設定とデザイン (CSS) ---
st.set_page_config(page_title="ジョーティッシュ鑑定所", page_icon="✨")

st.markdown(f"""
    <style>
    /* 全体の背景 */
    .stApp {{
        background-color: {C_BG};
    }}
    /* タイトルとサブヘッダーの文字色 */
    h1, h2, h3, label {{
        color: {C_ACCENT} !important;
        font-weight: bold;
    }}
    /* 入力エリア（セレクトボックス、数値入力、日付） */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div,
    div[data-baseweb="datepicker"] > div {{
        background-color: white !important;
        border: 2px solid {C_SUB} !important;
        border-radius: 10px !important;
    }}
    /* ボタンのデザイン */
    .stButton>button {{
        background: linear-gradient(135deg, {C_MAIN}, {C_ACCENT});
        color: white !important;
        border: none;
        border-radius: 25px;
        height: 3.5em;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    .stButton>button:hover {{
        opacity: 0.9;
        transform: translateY(-2px);
    }}
    </style>
    """, unsafe_allow_html=True)

# ロゴの表示
try:
    st.image("logo.png", use_container_width=True)
except:
    st.title("✨ ジョーティッシュ・ラグナ計算機")

# --- 1. 都道府県データの準備 ---
PREFECTURES = {
    "北海道": [43.0641, 141.3469], "青森県": [40.8244, 140.7400], "岩手県": [39.7036, 141.1527],
    "宮城県": [38.2682, 140.8694], "秋田県": [39.7186, 140.1024], "山形県": [38.2554, 140.3396],
    "福島県": [37.7503, 140.4675], "茨城県": [36.3418, 140.4468], "栃木県": [36.5657, 139.8836],
    "群馬県": [36.3895, 139.0634], "埼玉県": [35.8570, 139.6489], "千葉県": [35.6047, 140.1233],
    "東京都": [35.6895, 139.6917], "神奈川県": [35.4475, 139.6423], "新潟県": [37.9022, 139.0236],
    "富山県": [36.6953, 137.2113], "石川県": [36.5947, 136.6256], "福井県": [36.0652, 136.2219],
    "山梨県": [35.6639, 138.5683], "長野県": [36.6513, 138.1810], "岐阜県": [35.3912, 136.7223],
    "静岡県": [34.9756, 138.3828], "愛知県": [35.1802, 136.9066], "三重県": [34.7303, 136.5086],
    "滋賀県": [35.0045, 135.8686], "京都府": [35.0212, 135.7556], "大阪府": [34.6864, 135.5199],
    "兵庫県": [34.6913, 135.1831], "奈良県": [34.6851, 135.8327], "和歌山県": [34.2260, 135.1675],
    "鳥取県": [35.5039, 134.2377], "島根県": [35.4723, 133.0505], "岡山県": [34.6617, 133.9344],
    "広島県": [34.3853, 132.4553], "山口県": [34.1785, 131.4737], "徳島県": [34.0658, 134.5593],
    "香川県": [34.3401, 134.0434], "愛媛県": [33.8416, 132.7654], "高知県": [33.5597, 133.5311],
    "福岡県": [33.6064, 130.4182], "佐賀県": [33.2635, 130.3009], "長崎県": [32.7500, 129.8773],
    "熊本県": [32.7898, 130.7417], "大分県": [33.2382, 131.6126], "宮崎県": [31.9077, 131.4202],
    "鹿児島県": [31.5601, 130.5580], "沖縄県": [26.2124, 127.6809]
}
st.set_page_config(page_title="精密ジョーティッシュ計算機", page_icon="☸️")
st.title("☸️ 精密ラグナ算出ツール")

# --- 4. 入力フォーム ---
with st.container():
    birth_date = st.date_input("誕生日", datetime(1990, 1, 1))
    birth_time = st.time_input("出生時刻 (1分単位)", time(12, 0), step=60)
    pref_name = st.selectbox("出生地", list(PREFECTURES.keys()), index=0)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("鑑定（ラグナ算出）を実行する"):
    try:
        # 計算ロジック
        dt_local = datetime.combine(birth_date, birth_time)
        dt_ut = dt_local - timedelta(hours=9)
        jd = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, dt_ut.hour + dt_ut.minute/60.0)

        swe.set_sid_mode(1, 0, 0) # Lahiri
        ayan_val = swe.get_ayanamsa_ex(jd, 0)[0]

        lat, lon = PREFECTURES[pref_name]
        res = swe.houses_ex(jd, lat, lon, b'W', flags=64)
        lagna_deg = res[1][0]

        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        sign_index = int(lagna_deg / 30)
        deg = lagna_deg % 30

        # --- 5. 結果表示（指定カラーを使用） ---
        st.markdown("---")
        st.balloons()
        
        st.markdown(f"""
            <div style="
                background-color: white; 
                color: {C_ACCENT}; 
                padding: 30px; 
                border-radius: 20px; 
                border: 3px solid {C_MAIN}; 
                text-align: center;
                box-shadow: 0 10px 25px rgba(155, 142, 199, 0.2);
            ">
                <p style="margin: 0; font-size: 16px; color: {C_MAIN};">あなたのラグナは</p>
                <h1 style="color: {C_ACCENT}; font-size: 42px; margin: 10px 0;">【{zodiac_signs[sign_index]}】</h1>
                <p style="margin: 0; font-size: 18px;">{int(deg)}度 {int((deg - int(deg)) * 60)}分</p>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
