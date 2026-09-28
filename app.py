import streamlit as st
import sqlite3
from datetime import datetime

# --- DBMS CONNECTION ---
conn = sqlite3.connect('abc_parking.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS parked (vehicle_no TEXT PRIMARY KEY, type TEXT, owner TEXT, department TEXT, entry_time TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS history (vehicle_no TEXT, type TEXT, owner TEXT, department TEXT, entry_time TEXT, exit_time TEXT, fee INTEGER, status TEXT)")
conn.commit()

st.set_page_config(page_title="ABC College Parking", page_icon="🎓")
st.title("🎓 ABC College")
st.subheader("Vehicle Parking Management System (DBMS Project)")

menu = ["Park Vehicle", "View Parked", "Remove Vehicle", "History", "About Project"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Park Vehicle":
    st.header("Park Vehicle - ABC College")
    no = st.text_input("Vehicle Number (e.g. MH27 AB1234)").upper()
    v_type = st.selectbox("Vehicle Type", ["Bike", "Car", "Scooty", "Faculty Car"])
    owner = st.text_input("Student / Faculty Name")
    dept = st.selectbox("Department", ["CSE", "ENTC", "Mechanical", "Civil", "Faculty", "Visitor"])
    if st.button("Park Vehicle"):
        if no and owner:
            try:
                entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO parked VALUES (?,?,?,?,?)", (no, v_type, owner, dept, entry))
                conn.commit()
                st.success(f"Park Ho Gayi! {no} |
