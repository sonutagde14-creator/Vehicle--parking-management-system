import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

conn = sqlite3.connect('parking.db', check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS parking(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 vehicle_no TEXT, vehicle_type TEXT, owner_name TEXT,
 entry_time TEXT, exit_time TEXT, status TEXT, fee INTEGER)""")
conn.commit()

st.set_page_config(page_title="Parking System", layout="wide")
st.title("Vehicle Parking Management System")

menu = st.sidebar.selectbox("Menu", ["Park Vehicle", "Remove Vehicle", "View Parked", "History"])
rates = {"Car": 50, "Bike": 20, "Truck": 100, "Auto": 30}

if "search_data" not in st.session_state:
    st.session_state.search_data = None

if menu == "Park Vehicle":
    st.subheader("New Entry")
    v_no = st.text_input("Vehicle Number").upper().strip()
    v_type = st.selectbox("Type", ["Car", "Bike", "Truck", "Auto"])
    owner = st.text_input("Owner Name / Mobile")
    if st.button("Park Now", type="primary"):
        if v_no and owner:
            c.execute("SELECT * FROM parking WHERE vehicle_no=? AND status='Parked'", (v_no,))
            if c.fetchone():
                st.error("Pehle se parked hai!")
            else:
                entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO parking (vehicle_no, vehicle_type, owner_name, entry_time, status, fee) VALUES (?,?,?,?,?,?)", (v_no, v_type, owner, entry, "Parked", 0))
                conn.commit()
                st.success(f"{v_no} Park Ho Gayi!")
                st.balloons()
        else:
            st.warning("Number bharo")

elif menu == "Remove Vehicle":
    st.subheader("Exit")
    v_no = st.text_input("Vehicle Number for Exit").upper().strip()
    if st.button("Search"):
        c.execute("SELECT * FROM parking WHERE vehicle_no=? AND status='Parked'", (v_no,))
        data = c.fetchone()
        if data:
            st.session_state.search_data = data
        else:
            st.session_state.search_data = None
            st.error("Nahi mili! Pehle Park karo ya View Parked me check karo")

    if st.session_state.search_data:
        data = st.session_state.search_data
        entry_time = datetime.strptime(data[4], "%Y-%m-%d %H:%M:%S")
        hours = max(1, int((datetime.now() - entry_time).total_seconds() / 3600) + 1)
        fee = hours * rates.get(data[2], 50)

        st.write(f"**Found:** {data[1]} | {data[2]} | Owner: {data[3]}")
        st.write(f"Entry: {data[4]} | Hours: {hours} | Fee: Rs.{fee}")

        if st.button("Confirm Exit & Pay"):
            c.execute("UPDATE parking SET exit_time=?, status='Exited', fee=? WHERE id=?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fee, data[0]))
            conn.commit()
            st.success(f"Exit Done! Rs.{fee} Paid")
            st.session_state.search_data = None

elif menu == "View Parked":
    df = pd.read_sql_query("SELECT vehicle_no, vehicle_type, owner_name, entry_time FROM parking WHERE status='Parked'", conn)
    st.dataframe(df, use_container_width=True)

else:
    df = pd.read_sql_query("SELECT * FROM parking ORDER BY id DESC", conn)
    st.dataframe(df, use_container_width=True)
