import streamlit as st
import swisseph as swe
from datetime import datetime, time

# ページ設定
st.set_page_config(page_title="ジョーティッシュ計算機", page_icon="✨")
st.title("✨ ジョーティッシュ・ラグナ計算機")

# 入力フォーム
col1, col2 = st.columns(2)
with col1:
    birth_date = st.date_input("誕生日", datetime(1990, 1, 1))
with col2:
    birth_time = st.time_input("出生時刻", time(12, 0))

lat = st.number_input("緯度 (東京: 35.68)", value=35.68, format="%.4f")
lon = st.number_input("経度 (東京: 139.69)", value=139.69, format="%.4f")

if st.button("ラグナを算出する"):
    # 日本時間から世界時に変換（-9時間）
    dt = datetime.combine(birth_date, birth_time)
    jd = swe.julday(dt.year, dt.month, dt.day, (dt.hour + dt.minute/60.0) - 9)
    
    # 占星術計算の基本設定
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # 計算実行（エラー回避のためフラグを最小限にしています）
    try:
        # 第4引数の 1 はサイドリアル（恒星時）計算を意味します
        res = swe.houses_ex(jd, lat, lon, b'W', flags=1)
        ascmc = res[1] # アセンダント情報
        
        zodiac_signs = ["牡羊座", "牡牛座", "双子座", "蟹座", "獅子座", "乙女座", 
                        "天秤座", "蠍座", "射手座", "山羊座", "水瓶座", "魚座"]
        sign_index = int(ascmc[0] / 30)
        
        st.success(f"あなたのラグナは 【{zodiac_signs[sign_index]}】 です")
        st.info(f"詳細度数: {ascmc[0] % 30:.2f}°")
    except Exception as e:
        st.error(f"計算に失敗しました。設定を確認してください: {e}")
