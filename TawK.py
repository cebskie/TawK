import streamlit as st
import mysql.connector

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="inventory"
    )

# Function to validate login credentials from database
def validate_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE u_name = %s AND phone = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Session management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Centered layout using columns
def centered_login():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logo.svg", width=400)
    with col2:
        st.markdown("<h2 style='text-align: center;'>Welcome to TawK</h2>", unsafe_allow_html=True)
        st.write(" ")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("🔓 Login"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT u_id, u_name FROM users WHERE u_name = %s AND phone = %s",
                    (username, password)
                )
                user = cursor.fetchone()

                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]
                    st.session_state.role = "admin" if user[1].lower() == "admin" else "user"
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

                cursor.close()
                conn.close()
            except Exception as e:
                st.error(f"Database error: {e}")

if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 25vh;
        }
        </style>
        """, unsafe_allow_html=True
    )
    centered_login()
else:
    # Landing Page
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo-drop.svg", width=250)

    st.markdown(f"## 👋 Welcome to TawK, {st.session_state.username}!")
    st.write("Manage your inventory with ease and speed.")

    if st.session_state.role == "admin":
        st.write("TawK is a streamlined warehouse management system designed to simplify stock tracking, product transactions, and category management. Built with an intuitive interface, TawK allows users to efficiently monitor inventory levels, record transactions, and manage product details in real time. Whether for small businesses or larger operations, TawK ensures accurate inventory control, reducing errors and improving operational efficiency!")
        st.write("Admin Features:")
        st.page_link("pages/3Transaction Log.py", label="📋 Transaction Log")
        st.write("To check a transaction performed by a user, click the transaction button in the side bar. You’ll see a table of 10 rows of the most recent transactions done by the users. You can then prepare the product to be taken for out-type transactions, or prepare the storage for in-type transactions.")
        st.page_link("pages/4Users.py", label="👥 Users")
        st.write("Before a user has access to check products stock and perform transactions, they need to be registered to the system. You can do that by clicking the user button in the side bar and type the user’s name, address, and phone number. Once you make sure everything is correct, click the button to add the user to the system. You can also search for any user by the user id or user name. Just scroll down and select the search type, then type in the user id or user name. The user’s details will be shown in a table once you click the search button.")
        st.page_link("pages/5Add Product.py", label="➕ Add Product")
        st.write("If there’s a new product, that has never been registered in product database, you must input the product details first. To add new product, click the product button in the side bar, then you can select the category of new product, type the new product’s name, and the price. Once you make sure the details are right, click on the button to add the product to the database.")
        st.page_link("pages/1Stock.py", label="📦 Stock Overview")
        st.write("To check a product’s stock quantity, just click the stock button in the side bar and you’ll be directed to the check stock page. There, you can select the product category and product name. You can then click the button to check the product stock. There will be a table that shows the product name, stock quantity, and product price.")
        st.page_link("pages/6Insights.py", label="📊 Insights")
        st.write("By clicking the insight button in the side bar, you can see some reports of the products, such as the stock movement, most popular products, low stock products, and dead stock")
    else:
        st.write("TawK is a streamlined warehouse management system designed to simplify stock tracking, product transactions, and category management. Built with an intuitive interface, TawK allows users to efficiently monitor inventory levels, record transactions, and manage product details in real time. Whether for small businesses or larger operations, TawK ensures accurate inventory control, reducing errors and improving operational efficiency!")
        st.write("User Features:")
        st.page_link("pages/1Stock.py", label="📦 Stock Overview")
        st.write("Want to check product stock? No problem! Just click the stock button in the side bar and you’ll be directed to the check stock page. There, you can select the product category and product name. You can then click the button to check the product stock. There will be a table that shows the product name, stock quantity, and product price. This stock quantity is real time! The system updates the stock immediately after a transaction is performed.")
        st.page_link("pages/2Transactions.py", label="💰 Transactions")
        st.write("Performing in and out transactions is never easier! You can click the transaction button in the side bar and you’ll be directed to the transaction page. There, you can select the product category, the product name, and the transaction type (in or out). Make sure you’ve checked the product stock before performing the out-type transaction! You can then type the amount of product and then click the button to execute your transaction. Once your transaction is recorded, you can head to the warehouse and report your transaction. The admin there will get your products ready in no time!")
        st.write("Note: if you can’t find the product name when performing the in-type transaction, you can report to the admin and they will add the product for you. Once added, you can then perform the in-type transaction to your product.")

# Sidebar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.sidebar.image("logo.svg", use_container_width=True)
