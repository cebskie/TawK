import streamlit as st
import pandas as pd
import mysql.connector

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='root',
        password='',
        database='inventory'
    )


# Sidebar
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
if st.session_state.get("role") != "admin":
    st.error("Unauthorized access.")
    st.stop()
st.sidebar.image("logo.svg", use_container_width=True)

# Streamlit UI
st.title("Transactions Log")

# Getting the last 10 rows of transaction_log (most recent) 
try:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT tl.log_id AS 'log ID', tl.transaction_id AS 'transaction ID', p.prod_name AS 'product', tl.type, tl.date, u.u_name AS 'user name' FROM transaction_log tl JOIN products p ON tl.prod_id = p.prod_id JOIN users u ON tl.u_id = u.u_id ORDER BY tl.log_id DESC LIMIT 10")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(rows, columns=columns)
    df = df.reset_index(drop=True)  # optional, but good for safety
    # st.table(df)
    # st.dataframe(df, use_container_width=True)
    st.dataframe(
        df.style.set_properties(
            **{"white-space": "pre-wrap", "word-wrap": "break-word"}
        ),
        use_container_width=True
    )

    cursor.close()
    conn.close()
except Exception as e:
    st.error(f"Error fetching transaction logs: {e}")
