import streamlit as st
import swisseph as swe
from datetime import datetime, time, timedelta

# --- 1. カラーパレットの設定 ---
C_BG = "#F2EAE0"     # 背景
C_SUB = "#B4D3D9"    # 枠線・アクセント
C_MAIN = "#BDA6CE"   # ボタン・装飾
C_ACCENT = "#9B8EC7" # タイトル・強調

# --- 2. ページ設定とデザイン (CSS) ---
st.set_page_config(page_title="ジョーティッシュ鑑定所", page_icon="✨")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {C_BG}; }}
    h1, h2, h3, label {{ color: {C_ACCENT} !important; font-weight: bold; }}
    
    /* 入力フィールドのデザイン */
    .stDateInput div, .stTimeInput div, .stSelectbox div {{
        background-color: white !important;
        border-radius: 10px !important;
    }}
    
    /* ボタンのデザイン */
    .stButton>button {{
        background: linear-gradient(135deg, {C_MAIN}, {C_ACCENT});
        color: white !important;
        border-radius: 25px;
        height: 3.5em;
        width: 100%;
        border: none;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(155, 142, 199, 0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# ロゴの表示
try:
    st.image("Lagna blueprint.png", use_container_width=True)
except:
    st.title("✨ ジョーティッシュ鑑定所")

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
# --- 4. 入力フォーム ---
# 日付が入らない問題を解決するため、valueを指定し明示的にカレンダーを表示させます
birth_date = st.date_input("1. 誕生日を選択してください", value=datetime(1990, 1, 1), min_value=datetime(1900, 1, 1))
birth_time = st.time_input("2. 出生時刻 (1分単位)", value=time(12, 0), step=60)
pref_name = st.selectbox("3. 出生地", list(PREFECTURES.keys()), index=0)

if st.button("鑑定（ラグナ算出）を実行する"):
    try:
        # 1. 時間の精密変換 (JST -> UT)
        # 日本時間は世界時より9時間進んでいるため、正確に9時間を引きます
        dt_local = datetime.combine(birth_date, birth_time)
        dt_ut = dt_local - timedelta(hours=9)
        
        # 2. ユリウス日の計算
        # 小数点以下の時間まで精密に反映させます
        decimal_hour = dt_ut.hour + dt_ut.minute/60.0 + dt_ut.second/3600.0
        jd = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, decimal_hour)

        # 3. アヤナムシャの厳密設定 (1: Lahiri)
        swe.set_sid_mode(1, 0, 0)
        
        # 4. ラグナ（アセンダント）の計算
        # flags=64 (SIDEREAL) でインド式計算を確定させます
        lat, lon = PREFECTURES[pref_name]
        res = swe.houses_ex(jd, lat, lon, b'W', flags=64)
        lagna_deg = res[1][0] # 0-360度の生データ

        # 12星座の定義
        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        sign_index = int(lagna_deg / 30)
        deg_in_sign = lagna_deg % 30
        minutes = int((deg_in_sign - int(deg_in_sign)) * 60)

        # --- 5. 結果表示（指定カラー） ---
        st.markdown("---")
        st.balloons()
        
        st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 20px; 
                        border: 3px solid {C_MAIN}; text-align: center;
                        box-shadow: 0 10px 25px rgba(155, 142, 199, 0.2);">
                <p style="color: {C_MAIN}; margin: 0;">あなたのラグナは</p>
                <h1 style="color: {C_ACCENT}; font-size: 42px; margin: 10px 0;">【{zodiac_signs[sign_index]}】</h1>
                <p style="color: {C_ACCENT}; font-size: 18px; margin: 0;">
                    {int(deg_in_sign)}度 {minutes}分
                </p>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"計算エラーが発生しました: {e}")
