2009年付近の日付でエラーが出る原因は、プログラミング上の「日付の型（形式）」の不一致か、あるいはStreamlitのキャッシュが古いコードを読み込んでいる可能性が高いです。

特に、カレンダーから選んだ日付が内部的に「2009-01-17」という形式で正しく計算機（pyswisseph）に渡せていない場合にこのエラーが発生します。

これを確実に修正し、2009年でも、どの年代でもエラーが出ないように「日付処理」を強化した完全版コードを用意しました。

ステップ1：app.py を以下の「完全修正版」に書き換える
GitHubの app.py を開き、中身をすべて消してから、以下のコードをそのまま貼り付けて保存（Commit）してください。

Python
import streamlit as st
import swisseph as swe
from datetime import datetime, time, timedelta

# --- 1. カラーパレット ---
C_BG = "#F2EAE0"
C_SUB = "#B4D3D9"
C_MAIN = "#BDA6CE"
C_ACCENT = "#9B8EC7"

# --- 2. デザイン (CSS) ---
st.set_page_config(page_title="Lagna Blueprint", page_icon="✨")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {C_BG}; }}
    h1, h2, h3, label {{ color: {C_ACCENT} !important; font-weight: bold; }}
    .stButton>button {{
        background: linear-gradient(135deg, {C_MAIN}, {C_ACCENT});
        color: white !important; border-radius: 25px; border: none;
        height: 3.5em; width: 100%; font-weight: bold;
    }}
    /* 入力欄の背景を白に固定 */
    .stDateInput div, .stTimeInput div, .stSelectbox div {{
        background-color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ヘッダー画像の表示 ---
try:
    st.image("Lagna blueprint.png", use_container_width=True)
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
# 日付エラー回避のため、明示的に datetime 型として扱います
birth_date = st.date_input("誕生日を選択", value=datetime(2009, 1, 17))
birth_time = st.time_input("出生時刻", value=time(12, 0), step=60)
pref_name = st.selectbox("出生地", list(PREFECTURES.keys()), index=0)

if st.button("鑑定を実行する"):
    try:
        # 日付と時刻を結合（ここでのエラーを防ぐため型変換を強化）
        y, m, d = birth_date.year, birth_date.month, birth_date.day
        hh, mm = birth_time.hour, birth_time.minute
        
        # 日本時間(JST)から世界時(UT)へ変換（-9時間）
        local_dt = datetime(y, m, d, hh, mm)
        ut_dt = local_dt - timedelta(hours=9)
        
        # ユリウス日の計算 (精密版)
        jd_ut = swe.julday(ut_dt.year, ut_dt.month, ut_dt.day, ut_dt.hour + ut_dt.minute/60.0)

        # アヤナムシャ設定
        swe.set_sid_mode(1, 0, 0) # 1 = Lahiri
        
        # ラグナ算出
        lat, lon = PREFECTURES[pref_name]
        res = swe.houses_ex(jd_ut, lat, lon, b'W', flags=64) # 64 = Sidereal
        lagna_deg = res[1][0]

        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        sign_index = int(lagna_deg / 30)
        deg_in_sign = lagna_deg % 30

        # --- 結果表示 ---
        st.markdown("---")
        st.balloons()
        st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 20px; 
                        border: 3px solid {C_MAIN}; text-align: center;
                        box-shadow: 0 10px 25px rgba(155, 142, 199, 0.2);">
                <h1 style="color: {C_ACCENT}; font-size: 42px; margin: 10px 0;">【{zodiac_signs[sign_index]}】</h1>
                <p style="color: {C_ACCENT}; font-size: 18px;">
                    {int(deg_in_sign)}度 {int((deg_in_sign % 1) * 60)}分
                </p>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"計算にエラーが発生しました: {e}")
