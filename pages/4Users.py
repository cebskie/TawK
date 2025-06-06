import streamlit as st
import pandas as pd
from core.db import register_user_to_db, search_user_from_db

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

st.sidebar.image("logo.svg")

# Streamlit UI
st.title("User Registration")

# Register User
username = st.text_input("Enter Username")
address = st.text_input("Enter Address")
phone = st.text_input("Enter Phone Number")

if st.button("Register"):
    if username and address and phone:
        try:
            register_user_to_db(username, address, phone)
            st.success(f"User '{username}' registered successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill in all fields before submitting.")

# Search User
st.title("Search User")

user_search = st.text_input("Enter Username or User ID", key="search-input")

if st.button("Search"):
    if user_search:
        try:
            rows, columns = search_user_from_db(user_search)
            if rows:
                df = pd.DataFrame(rows, columns=columns)
                st.table(df)
            else:
                st.warning(f"No user found for '{user_search}'.")
        except Exception as e:
            st.error(f"Error fetching user data: {e}")
    else:
        st.warning("Please enter a Username or User ID to search.")
