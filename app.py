import streamlit as st
from datetime import datetime
import math
import pandas as pd

st.set_page_config(page_title="Smart Parking", layout="wide")

# ====== Dark Style ======
st.markdown("""
    <style>
    body {
        background-color: #0f172a;
        color: white;
    }
    .stApp {
        background-color: #0f172a;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 SMART PARKING SYSTEM")

# ====== Session Data ======
if "cars" not in st.session_state:
    st.session_state.cars = {}

cars = st.session_state.cars
price_per_hour = 5000

col1, col2 = st.columns(2)

# ================= XE VÀO =================
with col1:
    st.subheader("🚘 Xe vào")
    plate_in = st.text_input("Nhập biển số xe")

    if st.button("Gửi xe"):
        if plate_in == "":
            st.error("Vui lòng nhập biển số")
        elif plate_in in cars:
            st.warning("Xe đã có trong bãi")
        else:
            cars[plate_in] = datetime.now()
            st.success(f"Xe {plate_in} đã vào bãi")

# ================= XE RA =================
with col2:
    st.subheader("🚪 Xe ra")
    plate_out = st.text_input("Nhập biển số xe ra", key="out")

    if st.button("Thanh toán"):
        if plate_out not in cars:
            st.error("Không tìm thấy xe")
        else:
            entry_time = cars.pop(plate_out)
            exit_time = datetime.now()

            hours = (exit_time - entry_time).total_seconds() / 3600
            hours = max(1, math.ceil(hours))

            fee = hours * price_per_hour

            st.success(f"Xe {plate_out} đã ra bãi")
            st.info(f"💰 Tiền phải trả: {fee:,} VND")

# ================= DANH SÁCH =================
st.subheader("📋 Xe đang trong bãi")

if cars:
    data = []
    for plate, time in cars.items():
        data.append({
            "Biển số": plate,
            "Thời gian vào": time.strftime("%H:%M:%S %d/%m/%Y")
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Hiện chưa có xe trong bãi")

st.markdown("---")
st.write(f"🚘 Tổng số xe hiện tại: {len(cars)}")
