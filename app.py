import streamlit as st

st.title("Vehicle Parking Management System")
st.write("Only Frontend - DBMS Project")

# Temporary list bina database ke
if 'parked_list' not in st.session_state:
    st.session_state.parked_list = []

vehicle_no = st.text_input("Gaadi Number Daalo (MH31...)")
owner_name = st.text_input("Owner Name")

col1, col2 = st.columns(2)

with col1:
    if st.button("Park Karo"):
        if vehicle_no != "":
            st.session_state.parked_list.append(vehicle_no)
            st.success("Park Ho Gayi!")
        else:
            st.error("Pehle Gaadi Number Daalo")

with col2:
    if st.button("Saari Gaadiya Dikhao"):
        st.write(st.session_state.parked_list)

st.write("---")
st.write("Total Parked:", len(st.session_state.parked_list))
