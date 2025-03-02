import streamlit as st
import mysql.connector

# Function to connect to the database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',      # e.g. localhost or IP address
        user='root',      # Your MySQL username
        password='',  # Your MySQL password
        database='inventory'  # Your MySQL database name
    )
    return connection


 # Streamlit UI
st.title("User Registration")
st.sidebar.image("TawK logo.png", use_container_width=True)

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

# Button to go back to home
if st.button("Back to Home"):
    st.switch_page("TawK.py")
