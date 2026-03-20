import streamlit as st
import swisseph as swe
from datetime import datetime, time, timedelta

# --- 1. カラーパレット ---
C_BG = "#F2EAE0"
C_MAIN = "#BDA6CE"
C_ACCENT = "#9B8EC7"

# --- 2. デザイン (CSS) ---
st.set_page_config(page_title="Lagna Blueprint", page_icon="✨")

st.markdown(f"""
    <style>
    header[data-testid="stHeader"], footer, #MainMenu {{ display: none !important; }}
    .stAppToolbar {{ display: none !important; }}
    .block-container {{ padding-top: 2rem !important; }}
    .stApp {{ background-color: {C_BG}; }}
    h1, h2, h3, label {{ color: {C_ACCENT} !important; font-weight: bold; }}

    input, .stSelectbox div[data-baseweb="select"] {{
        color: {C_ACCENT} !important;
        -webkit-text-fill-color: {C_ACCENT} !important;
        background-color: white !important;
    }}
    div[data-baseweb="input"], div[data-baseweb="select"] {{
        background-color: white !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {C_MAIN}, {C_ACCENT});
        color: white !important; border-radius: 25px; border: none;
        height: 3.5em; width: 100%; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ヘッダー画像 ---
try:
    st.image("LagnaTOP.png", use_container_width=True)
except:
    st.title("✨ Lagna Blueprint")

# --- 4. 都道府県データ ---
PREFECTURES = {
    "北海道": [43.0641, 141.3469], "青森県": [40.8244, 140.7400], "岩手県": [39.7036, 141.1527],
    "宮城県": [38.2682, 140.8694], "秋田県": [39.7186, 140.1024], "山形県": [38.2554, 140.3396],
    "福島県": [37.7503, 140.4675], "茨城県": [36.3418, 140.4468], "栃木県": [36.5657, 139.8835],
    "群馬県": [36.3912, 139.0602], "埼玉県": [35.8570, 139.6490], "千葉県": [35.6051, 140.1232],
    "東京都": [35.6895, 139.6917], "神奈川県": [35.4478, 139.6425], "新潟県": [37.9022, 139.0236],
    "富山県": [36.6953, 137.2113], "石川県": [36.5947, 136.6256], "福井県": [36.0652, 136.2216],
    "山梨県": [35.6640, 138.5683], "長野県": [36.6513, 138.1810], "岐阜県": [35.3912, 136.7222],
    "静岡県": [34.9769, 138.3831], "愛知県": [35.1802, 136.9066], "三重県": [34.7303, 136.5086],
    "滋賀県": [35.0045, 135.8686], "京都府": [35.0210, 135.7556], "大阪府": [34.6864, 135.5199],
    "兵庫県": [34.6913, 135.1830], "奈良県": [34.6853, 135.8328], "和歌山県": [34.2260, 135.1675],
    "鳥取県": [35.5036, 134.2383], "島根県": [35.4722, 133.0505], "岡山県": [34.6618, 133.9344],
    "広島県": [34.3963, 132.4594], "山口県": [34.1858, 131.4706], "徳島県": [34.0657, 134.5593],
    "香川県": [34.3401, 134.0433], "愛媛県": [33.8416, 132.7657], "高知県": [33.5597, 133.5311],
    "福岡県": [33.6064, 130.4182], "佐賀県": [33.2635, 130.2998], "長崎県": [32.7448, 129.8737],
    "熊本県": [32.7898, 130.7417], "大分県": [33.2382, 131.6126], "宮崎県": [31.9111, 131.4239],
    "鹿児島県": [31.5967, 130.5571], "沖縄県": [26.2124, 127.6809]
}

# --- 5. 入力フォーム ---
today = datetime.now()
birth_date = st.date_input(
    "1. 誕生日を選択", 
    value=datetime(1980, 1, 1),
    min_value=datetime(1950, 1, 1),
    max_value=today
)
# step=60 を入れることで1分単位の選択になります
birth_time = st.time_input("2. 出生時刻", value=time(10, 58), step=60)
pref_name = st.selectbox("3. 出生地", list(PREFECTURES.keys()))

# --- 6. 鑑定ロジック ---
if st.button("鑑定結果を表示する"):
    try:
        # 時差の計算 (日本は +9時間)
        dt_local = datetime.combine(birth_date, birth_time)
        dt_ut = dt_local - timedelta(hours=9)
        
        # ユリウス日の算出 (ET/UT)
        jd_ut = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, dt_ut.hour + dt_ut.minute/60.0)
        
        # 緯度経度の取得
        lat, lon = PREFECTURES[pref_name]
        
        # 1. まず西洋式(Tropical)のアセンダントを算出
        # flag = 0 (西洋式) を明示
        res_houses = swe.houses(jd_ut, lat, lon, b'P')
        tropical_asc = res_houses[0][0] # アセンダント
        
        # 2. Lahiriアヤナムシャの値を強制的に引き出す
        # sid_modeをセットしてから get_ayanamsa で数値を取得
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        ayanamsa_val = swe.get_ayanamsa(jd_ut)
        
        # 3. インド式角度 ＝ 西洋式角度 － アヤナムシャ
        lagna_deg = (tropical_asc - ayanamsa_val) % 360

        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        
        all_msgs = [
            "情熱的で、新しい一歩を踏み出す勇気を持っています。",
            "穏やかで、心地よい豊かさを育む才能があります。",
            "知的好奇心が旺盛で、軽やかに情報を繋ぐ力があります。",
            "共感力が高く、大切な居場所を守り育てる愛を持っています。",
            "堂々とした華やかさと、周囲を照らすリーダーシップがあります。",
            "緻密で分析力に優れ、物事を完璧に整える力を持っています。",
            "調和を重んじ、洗練された美意識とバランス感覚があります。",
            "深い洞察力と、一つのことを極める強い精神力があります。",
            "自由を愛し、高い理想を求めて冒険する精神を持っています。",
            "責任感が強く、地道な努力で大きな成果を成し遂げる力があります。",
            "独創的で、未来を見据えた新しい視点を持っています。",
            "感受性が豊かな、全てを包み込む優しさがあります。"
        ]

        sign_index = int(lagna_deg / 30)
        deg_in_sign = lagna_deg % 30
        sign_name = zodiac_signs[sign_index]
        advice = all_msgs[sign_index]

        st.markdown("---")
        st.balloons()
        
        shop_url = "https://lagnablue.base.shop/"

        st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 20px; 
                        border: 3px solid {C_MAIN}; text-align: center; margin-bottom: 20px;">
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
                        color: {C_BG} !important; 
                        padding: 12px 30px; 
                        border-radius: 50px;
                        font-weight: 800; 
                        font-size: 16px; 
                        display: inline-block;
                        box-shadow: 0 4px 12px rgba(155, 142, 199, 0.4);
                        text-decoration: none !important;
                        -webkit-text-fill-color: {C_BG} !important;
                    ">
                        個人鑑定を申し込む
                    </span>
                </a>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"鑑定中にエラーが発生しました。時間を空けて再度お試しください。")
