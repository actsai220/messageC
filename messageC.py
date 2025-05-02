import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google Sheet 設定
SERVICE_ACCOUNT_FILE = "messagec-458205-70af97b34a0c.json"  # 金鑰檔名
SPREADSHEET_ID = "1A9SSIxJfmeDLQZr1tE8-FzXk6xOpZM5YzueilnRiBnE"    # 替換成你的 Sheet ID
SHEET_NAME = "工作表1"                       # 你的工作表名稱

def connect_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    return sheet

def submit_message(name, message):
    sheet = connect_sheet()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, name, message])

# Streamlit 介面
st.set_page_config(page_title="互動留言板")
st.title("💬 互動留言板")

name = st.text_input("請輸入你的名字")
message = st.text_area("請輸入你的留言")

if st.button("送出留言"):
    if name.strip() and message.strip():
        submit_message(name, message)
        st.success("✅ 留言已送出！")
    else:
        st.warning("⚠️ 請輸入名字與留言")

st.subheader("📋 最新留言")
try:
    sheet = connect_sheet()
    records = sheet.get_all_values()[1:]  # 跳過標題列
    for row in reversed(records[-10:]):  # 顯示最新10筆留言
        timestamp, username, content = row
        st.markdown(f"**{username}** 🕒 {timestamp}\n\n> {content}\n---")
except Exception as e:
    st.error(f"無法讀取留言：{e}")
