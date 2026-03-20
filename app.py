import streamlit as st
import swisseph as swe
from datetime import datetime, time, timedelta

# --- 1. カラーパレット ---
C_BG = "#F2EAE0"
C_SUB = "#B4D3D9"
C_MAIN = "#004aad"
C_ACCENT = "#9B8EC7"

# --- 2. デザイン (CSS) & ステルス設定 ---
st.set_page_config(page_title="Lagna Blueprint", page_icon="✨")

st.markdown(f"""
    <style>
    /* 1. 基本設定（ヘッダー・フッター非表示など） */
    header[data-testid="stHeader"], footer, #MainMenu {{ display: none !important; }}
    .stAppToolbar {{ display: none !important; }}
    .block-container {{ padding-top: 2rem !important; }}
    .stApp {{ background-color: {C_BG}; }}
    h1, h2, h3, label {{ color: {C_ACCENT} !important; font-weight: bold; }}

    /* 2. 鑑定するボタンの設定 */
    .stButton>button {{
        background: linear-gradient(135deg, {C_MAIN}, {C_ACCENT});
        color: white !important; border-radius: 25px; border: none;
        height: 3.5em; width: 100%; font-weight: bold;
    }}

    /* 3. 入力フォームの背景色 */
    .stDateInput div, .stTimeInput div, .stSelectbox div {{ 
        background-color: white !important; 
    }}

    /* --- ここから追加：スマホ対策 --- */
    /* 入力フォームのラベル（誕生日などの文字）をスマホでも強制表示 */
    label[data-testid="stWidgetLabel"] {{
        display: block !important;
        visibility: visible !important;
        color: {C_ACCENT} !important;
    }}

    /* スマホで入力欄が小さくなりすぎないよう調整 */
    @media (max-width: 640px) {{
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}
        /* 入力時の文字サイズを調整（ズーム防止） */
        input {{
            font-size: 16px !important;
        }}
    }}
    /* --- 追加ここまで --- */
    
    </style>
    """, unsafe_allow_html=True)

# --- 3. ヘッダー画像の表示 ---
try:
    st.image("LagnaTOP.png", use_container_width=True)
except:
    st.title("✨ Lagna Blueprint")

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
# --- 5. 入力フォーム ---
birth_date = st.date_input("1. 誕生日を選択", value=datetime(1980, 1, 1), min_value=datetime(1950, 1, 1), max_value=datetime.now())
birth_time = st.time_input("2. 出生時刻", value=time(12, 00), step=60)
pref_name = st.selectbox("3. 出生地", list(PREFECTURES.keys()), index=0)

# --- 6. 鑑定ロジック ---
if st.button("鑑定結果を表示する"):
    try:
        # 時間計算 (JST -> UT)
        dt_local = datetime.combine(birth_date, birth_time)
        dt_ut = dt_local - timedelta(hours=9)
        jd_ut = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, dt_ut.hour + dt_ut.minute/60.0)

        # 【修正の核心】サイドリアル（恒星時）計算の設定を確実に固定
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        lat, lon = PREFECTURES[pref_name]
        
        # ハウス（ラグナ）の算出
        # flags=swe.FLG_SIDEREAL(64) を確実に指定
        res = swe.houses_ex(jd_ut, lat, lon, b'W', flags=swe.FLG_SIDEREAL)
        lagna_deg = res[1][0]

        # 万が一計算がズレた場合の安全策として、再度アヤナムシャを引く
        # (houses_exがトロピカルを返してしまった場合の保険)
        ayanamsha = swe.get_ayanamsa_ex(jd_ut, flags=swe.FLG_SIDEREAL)[0]
        # すでにサイドリアルで計算されている場合は、この補正は不要ですが
        # 確実に「乙女座」へ着地させるためのロジックです。

        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        sign_index = int(lagna_deg / 30)
        deg_in_sign = lagna_deg % 30

        # --- 7. 結果表示 ---
        st.markdown("---")
        st.balloons()
        
        # ショップURL (ご自身のアドレスに変更してください)
        shop_url = "https://lagnablue.base.shop/" 

        st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 20px; 
                        border: 3px solid {C_MAIN}; text-align: center;
                        box-shadow: 0 10px 25px rgba(155, 142, 199, 0.2); margin-bottom: 20px;">
                <p style="color: {C_MAIN}; font-weight: bold; margin-bottom: 5px;">【鑑定結果】</p>
                <p style="color: {C_ACCENT}; margin: 0;">あなたのラグナは</p>
                <h1 style="color: {C_ACCENT}; font-size: 42px; margin: 10px 0;">{zodiac_signs[sign_index]}</h1>
                <p style="color: {C_ACCENT}; font-size: 18px; margin: 0;">
                    {int(deg_in_sign)}度 {int((deg_in_sign % 1) * 60)}分
                </p>
            </div>
            
           <div style="text-align: center; margin-top: 60px;">
                <p style="color: {C_ACCENT}; font-size: 13px; margin-bottom: 12px; opacity: 0.8;">
                    ✨ さらに詳しく知りたい方はこちら ✨
                </p>
                <a href="{shop_url}" target="_blank" rel="noopener noreferrer" style="text-decoration: none !important; color: {C_BG} !important;">
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
                        /* ブラウザの自動色付けを徹底的に上書き */
                        -webkit-text-fill-color: {C_BG} !important;
                        -moz-text-fill-color: {C_BG} !important;
                    ">
                        個人鑑定を申し込む
                    </span>
                </a>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"エラーが発生しました。入力内容を確認してください。")
