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
            "乙女座": "緻密で分析力に優れ、物事を完璧に整える力を持っています。",
            "天秤座": "調和を重んじ、洗練された美意識とバランス感覚があります。",
            "蠍座": "深い洞察力と、一つのことを極める強い精神力があります。",
            "射手座": "自由を愛し、高い理想を求めて冒険する精神を持っています。",
            "山羊座": "責任感が強く、地道な努力で大きな成果を成し遂げる力があります。",
            "水瓶座": "独創的で、未来を見据えた新しい視点を持っています。",
            "魚座": "感受性が豊かな、全てを包み込む優しさがあります。"
        }
        advice = messages.get(sign_name, "")

        # --- 7. 結果表示 & BASEボタン ---
        st.markdown("---")
        st.balloons()
        
        shop_url = "https://yourshop.base.shop/" # 自分のURLに書き換えてください

        st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 20px; 
                        border: 3px solid {C_MAIN}; text-align: center;
                        box-shadow: 0 10px 25px rgba(155, 142, 199, 0.2); margin-bottom: 20px;">
                <p style="color: {C_MAIN}; font-weight: bold; margin-bottom: 5px;">【鑑定結果】</p>
                <p style="color: {C_ACCENT}; margin: 0;">あなたのラグナは</p>
                <h1 style="color: {C_ACCENT}; font-size: 42px; margin: 10px 0;">{sign_name}</h1>
                <p style="color: {C_ACCENT}; font-size: 18px; margin: 0;">
                    {int(deg_in_sign)}度 {int((deg_in_sign % 1) * 60)}分
                </p>
            </div>
            
            <div style="text-align: center; margin: 30px 10px; color: {C_ACCENT};">
                <p style="font-size: 15px; margin-bottom: 8px;">🌙 <b>{sign_name}のあなたへのメッセージ</b></p>
                <p style="font-size: 14px; line-height: 1.6; opacity: 0.9;">
                    {advice}
                </p>
            </div>

            <div style="text-align: center; margin-top: 40px;">
                <p style="color: {C_ACCENT}; font-size: 13px; margin-bottom: 12px; opacity: 0.8;">
                    ✨ さらに詳しく知りたい方はこちら ✨
                </p>
                <a href="{shop_url}" target="_blank" rel="noopener noreferrer" style="text-decoration: none !important;">
                    <span style="
                        background: linear-gradient(135deg, {C_MAIN}, {C_ACCENT});
                        color: {C_BG} !important; padding: 12px 30px; border-radius: 50px;
                        font-weight: 800; font-size: 16px; display: inline-block;
                        box-shadow: 0 4px 12px rgba(155, 142, 199, 0.4); text-decoration: none !important;
                        -webkit-text-fill-color: {C_BG} !important;
                    ">
                        個人鑑定を申し込む
                    </span>
                </a>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"エラーが発生しました。入力内容を確認してください。")
