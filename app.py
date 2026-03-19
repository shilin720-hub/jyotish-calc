import streamlit as st
import swisseph as swe
from datetime import datetime, time, timedelta

# --- 1. ページ設定とデザイン (CSS) ---
st.set_page_config(page_title="ジョーティッシュ鑑定所", page_icon="✨")

# 背景色やボタンのデザインをアドビ風に整える設定
st.markdown("""
    <style>
    .stApp {
        background-color: #f1f1f2;
    }
    .stButton>button {
        background-color: #1995ad;
        color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ロゴ画像の読み込み ---
# GitHubに「logo.png」という名前で画像をアップロードしておくと表示されます
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
st.set_page_config(page_title="精密ジョーティッシュ計算機", page_icon="☸️")
st.title("☸️ 精密ラグナ算出ツール")

# 入力フォーム
birth_date = st.date_input("誕生日", datetime(1990, 1, 1))
birth_time = st.time_input("出生時刻 (1分単位)", time(12, 0), step=60)
pref_name = st.selectbox("出生地", list(PREFECTURES.keys()), index=0)

if st.button("計算を実行する"):
    try:
        # 1. 時間の補正 (日本時間から世界時UTへ)
        dt_local = datetime.combine(birth_date, birth_time)
        dt_ut = dt_local - timedelta(hours=9)
        jd = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, dt_ut.hour + dt_ut.minute/60.0)

        # 2. アヤナムシャの厳密な設定 (ラヒリ)
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        
        # 3. アヤナムシャの値を取得（確認用）
        ayan_value = swe.get_ayanamsa_ex(jd, flags=swe.FLG_SIDEREAL)[0]

        # 4. ハウスとアセンダント(ラグナ)の算出
        # flags=swe.FLG_SIDEREAL を明示的に指定してインド式計算を強制します
        res = swe.houses_ex(jd, PREFECTURES[pref_name][0], PREFECTURES[pref_name][1], b'W', flags=swe.FLG_SIDEREAL)
        lagna_deg_raw = res[1][0] # これがアヤナムシャ適用済みのラグナ度数

        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        sign_index = int(lagna_deg_raw / 30)

        # 結果表示
        st.markdown("---")
        st.success(f"あなたのラグナは 【{zodiac_signs[sign_index]}】 です")
        
        # ずれを確認するための詳細情報
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ラグナ度数（星座内）", f"{lagna_deg_raw % 30:.2f}°")
        with col2:
            st.metric("適用アヤナムシャ", f"{ayan_value:.2f}°")
        
        st.write("※西洋占星術（サヤナ）とは約24度異なります。")

    except Exception as e:
        st.error(f"計算エラー: {e}")
