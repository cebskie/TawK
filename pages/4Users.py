import streamlit as st
import mysql.connector
import pandas as pd

# Function to connect to the database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',      # e.g. localhost or IP address
        user='root',      # Your MySQL username
        password='',  # Your MySQL password
        database='inventory'  # Your MySQL database name
    )
    return connection

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
# Register User
st.title("User Registration")

# User input fields
username = st.text_input("Enter Username")
address = st.text_input("Enter Address")
phone = st.text_input("Enter Phone Number")

# Submit button
if st.button("Register"):
    if username and address and phone:
        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Execute the stored procedure
            cursor.callproc("registerUser", (username, address, phone))
            
            # Commit and close
            conn.commit()
            cursor.close()
            conn.close()

            st.success(f"User '{username}' registered successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill in all fields before submitting.")

# Search User
st.title("Search User")

# User input fields
user_search = st.text_input("Enter Username or User ID", key="search-input")

# Search button
if st.button("Search"):
    if user_search:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE u_id = %s OR u_name = %s", 
                (user_search, user_search)
            )
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(rows, columns=columns)
            df = df.reset_index(drop=True)  # optional, but good for safety
            st.table(df)

            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error fetching user data: {e}")
