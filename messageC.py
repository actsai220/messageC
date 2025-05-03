import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 設定授權範圍
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# 從 secrets 讀取金鑰資訊
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)
client = gspread.authorize(creds)

# 接下來你就可以操作 Sheet：
SPREADSHEET_ID = '1A9SSIxJfmeDLQZr1tE8-FzXk6xOpZM5YzueilnRiBnE'
SHEET_NAME = '工作表1'

sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# 可以用 Streamlit 輸入或寫死測試
name = st.text_input("請輸入你的大名：")
if st.button("送出留言"):
    if name:
        sheet.append_row([name])
        st.success("✅ 已成功送出留言！")
    else:
        st.warning("請先輸入姓名")
