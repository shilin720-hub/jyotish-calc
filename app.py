import streamlit as st
import swisseph as swe
from datetime import datetime, time, timedelta

# --- 1. カラーパレット ---
C_BG = "#F2EAE0"
C_SUB = "#B4D3D9"
C_MAIN = "#BDA6CE"
C_ACCENT = "#9B8EC7"

# --- 2. ページ設定とデザイン (CSS) ---
st.set_page_config(page_title="Lagna Blueprint", page_icon="✨")

# デザイン設定：アカウント名やメニューを完全に隠しつつ、指定のカラーを反映させます
st.markdown(f"""
    <style>
    /* 1. ヘッダー（GitHubアイコン等）を完全に消去 */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}

    /* 2. フッター（アカウント名等）を完全に消去 */
    footer {{
        display: none !important;
    }}

    /* 3. メニューボタンを完全に消去 */
    #MainMenu {{
        display: none !important;
    }}

    /* 4. 余白の調整（ヘッダーを消した分、上に詰めすぎないようにする） */
    .block-container {{
        padding-top: 2rem !important;
    }}

    /* 5. 全体の背景色 */
    .stApp {{
        background-color: {C_BG};
    }}
    
    /* 6. ラベルやタイトルの色 */
    h1, h2, h3, label {{
        color: {C_ACCENT} !important;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ヘッダー画像の表示 ---
# 画像ファイル名「Lagna blueprint.png」を表示させます
try:
    st.image("Lagna blueprint.png", use_container_width=True)
except:
    # 画像が読み込めない場合のバックアップタイトル
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
# --- 5. 入力フォーム（初期値1980年、範囲1950年〜） ---
birth_date = st.date_input(
    "1. 誕生日を選択", 
    value=datetime(1980, 1, 1),
    min_value=datetime(1950, 1, 1),
    max_value=datetime.now()
)
birth_time = st.time_input("2. 出生時刻", value=time(10, 58), step=60)
pref_name = st.selectbox("3. 出生地", list(PREFECTURES.keys()), index=0)

if st.button("鑑定結果を表示する"):
    try:
        # 1. 時間計算 (JST -> UT)
        dt_local = datetime.combine(birth_date, birth_time)
        dt_ut = dt_local - timedelta(hours=9)
        
        # ユリウス日の計算
        jd_ut = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, dt_ut.hour + dt_ut.minute/60.0)

        # 2. アヤナムシャ設定 (Lahiri) を強制適用
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        
        # 3. ラグナ算出
        # 都道府県データから座標取得
        lat, lon = PREFECTURES[pref_name]
        
        # 【重要】flags=swe.FLG_SIDEREAL (64) を明示的に指定してサイドリアル計算を強制
        # これにより西洋式の星座（天秤座）ではなくインド式の星座（乙女座）が算出されます
        res = swe.houses_ex(jd_ut, lat, lon, b'W', flags=swe.FLG_SIDEREAL)
        lagna_deg = res[1][0]

        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        sign_index = int(lagna_deg / 30)
        deg_in_sign = lagna_deg % 30

        # --- 4. 結果表示 ---
        st.markdown("---")
        st.balloons()
        
        # BASEショップのURL
        base_shop_url = "https://yourshop.base.shop/" 

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
                <a href="{{base_shop_url}}" target="_blank" style="text-decoration: none;">
                    <div style="
                        background: linear-gradient(135deg, {C_MAIN}, {C_ACCENT});
                        color: white; padding: 10px 24px; border-radius: 50px;
                        font-weight: bold; font-size: 15px; display: inline-block;
                        box-shadow: 0 3px 10px rgba(155, 142, 199, 0.3);
                    ">
                        個人鑑定を申し込む
                    </div>
                </a>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"エラーが発生しました: {{e}}")
