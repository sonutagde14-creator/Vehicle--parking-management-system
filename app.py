import streamlit as st
from datetime import datetime
import time

st.title("Vehicle Parking Management System")
st.write("Only Frontend - DBMS Project with Payment")

if 'parked_list' not in st.session_state:
    st.session_state.parked_list = {}
if 'history' not in st.session_state:
    st.session_state.history = []

vehicle_no = st.text_input("Gaadi Number Daalo (MH31...)").upper()
owner_name = st.text_input("Owner Name")

col1, col2 = st.columns(2)

with col1:
    if st.button("Park Karo"):
        if vehicle_no != "":
            entry_time = datetime.now()
            st.session_state.parked_list[vehicle_no] = {
                "owner": owner_name,
                "entry": entry_time
            }
            st.success(f"{vehicle_no} Park Ho Gayi!")
        else:
            st.error("Pehle Number Daalo")

with col2:
    if st.button("Remove Karo - Payment Nikalo"):
        if vehicle_no in st.session_state.parked_list:
            entry_time = st.session_state.parked_list[vehicle_no]["entry"]
            exit_time = datetime.now()
            duration_sec = (exit_time - entry_time).total_seconds()
            minutes = int(duration_sec / 60)
            if minutes < 1:
                minutes = 1
            payment = minutes * 10
            if payment < 20:
                payment = 20

            st.warning(f"{vehicle_no} Remove Ho Gayi!")
            st.info(f"Payment: Rs. {payment} | Time: {minutes} min")

            st.session_state.history.append({
                "Gaadi No": vehicle_no,
                "Owner": st.session_state.parked_list[vehicle_no]["owner"],
                "Payment": f"Rs. {payment}"
            })
            del st.session_state.parked_list[vehicle_no]
        else:
            st.error("Ye Gaadi Park Hi Nahi Hai")

st.write("---")
st.subheader(f"Abhi Park Hai: {len(st.session_state.parked_list)}")
st.write(list(st.session_state.parked_list.keys()))

st.subheader("Parking History + Payment")
if len(st.session_state.history) > 0:
    st.table(st.session_state.history)
else:
    st.write("Abhi koi history nahi hai")
