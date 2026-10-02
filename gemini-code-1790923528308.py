import streamlit as st
import pandas as pd

st.set_page_config(page_title="學生投籃歷程紀錄", layout="centered")
st.title("🏀 學生投籃歷程紀錄系統")

# 初始化 Session 狀態（儲存成績）
if "records" not in st.session_state:
    st.session_state.records = {}

# 輸入區塊
st.subheader("新增 / 補考紀錄")
col1, col2 = st.columns(2)
with col1:
    seat_num = st.number_input("學生座號", min_value=1, step=1)
with col2:
    made_shots = st.selectbox("投進球數 (共5球)", options=[0, 1, 2, 3, 4, 5])

if st.button("送出紀錄"):
    seat_num = int(seat_num)
    current_score = made_shots * 20
    
    if seat_num in st.session_state.records:
        old_shots, old_score = st.session_state.records[seat_num]
        if current_score > old_score:
            st.session_state.records[seat_num] = (made_shots, current_score)
            st.success(f"✅ 座號 {seat_num} 補考成績較高！更新為 {current_score} 分")
        else:
            st.info(f"ℹ️ 本次成績 ({current_score} 分) 未高於原成績 ({old_score} 分)，保留原紀錄。")
    else:
        st.session_state.records[seat_num] = (made_shots, current_score)
        st.success(f"✅ 已新增座號 {seat_num}：{current_score} 分")

# 顯示與匯出區塊
st.markdown("---")
st.subheader("📊 成績清單（按座號排序）")

if st.session_state.records:
    # 轉為 DataFrame 並按座號排序
    data = []
    for seat, (shots, score) in sorted(st.session_state.records.items()):
        data.append({"座號": seat, "進球數": shots, "最終成績": score})
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    # 匯出 CSV 檔案
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下載 CSV 成績單",
        data=csv,
        file_name="basketball_scores.csv",
        mime="text/csv"
    )
else:
    st.write("目前尚無成績資料。")