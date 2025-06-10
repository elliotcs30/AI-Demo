# Streamlit 病人健康數據異常警示判讀系統
# 經由偵測病人的收縮壓、舒張壓、脈搏、血糖等數據協助醫師快速判讀

import streamlit as st
import pandas as pd

st.set_page_config(page_title="病人健康數據異常警示判讀系統", layout="wide")
st.title("📊 健康數據異常警示判讀系統 DEMO")

# 上傳檔案
uploaded_file = st.file_uploader("請上傳病人健康紀錄 Excel 或 CSV 檔案", type=["xlsx", "csv"])

if uploaded_file:
    # 讀取資料
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # 定義異常偵測邏輯
    def check_abnormal(row):
        abnormalities = []

        if row['收縮壓'] > 140:
            abnormalities.append("收縮壓偏高")
        elif row['收縮壓'] < 90:
            abnormalities.append("收縮壓偏低")

        if row['舒張壓'] > 90:
            abnormalities.append("舒張壓偏高")
        elif row['舒張壓'] < 60:
            abnormalities.append("舒張壓偏低")

        if row['脈搏'] > 100:
            abnormalities.append("脈搏過快")
        elif row['脈搏'] < 60:
            abnormalities.append("脈搏過慢")

        if row['血糖'] > 126:
            abnormalities.append("血糖偏高")

        return ", ".join(abnormalities) if abnormalities else "正常"

    # 檢查異常欄位
    df["異常警示"] = df.apply(check_abnormal, axis=1)
    abnormal_df = df[df["異常警示"] != "正常"]

    st.success(f"共偵測出 {len(abnormal_df)} 筆異常紀錄")

    # 展示異常紀錄表格
    st.dataframe(abnormal_df, use_container_width=True)

    # 匯出下載
    csv = abnormal_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="下載異常報表 (CSV)",
        data=csv,
        file_name="異常健康警示報表.csv",
        mime="text/csv"
    )
else:
    st.info("請上傳健康數據檔案以開始分析")

# 請開啟 Terminal 輸入 streamlit run app.py