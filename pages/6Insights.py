import streamlit as st
import pandas as pd
import mysql.connector

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='inventory'
    )


# Sidebar
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()    
if st.session_state.get("role") != "admin":
    st.error("Unauthorized access.")
    st.stop()
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
st.sidebar.image("logo.svg", use_container_width=True)

# Streamlit UI
st.title("Insights")

# Get category names from the category table
# try:
#     conn = get_db_connection()
#     cursor = conn.cursor()