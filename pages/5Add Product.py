import streamlit as st
import mysql.connector
import pandas as pd

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="inventory"
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

# Function to call stored procedure 'addProduct'
def add_product(product_name, price, cat_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc("addProduct", (product_name, price, cat_id))
        conn.commit()
        st.success(f"✅ Product '{product_name}' added successfully!")
    except Exception as e:
        st.error(f"❌ Error adding product: {e}")
    finally:
        cursor.close()
        conn.close()

# Fetch category names and IDs from database
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT cat_id, cat_name FROM categories")  
        categories = cursor.fetchall()  # Get list of (cat_id, cat_name)
        
        cursor.close()
        conn.close()
        return categories
    except Exception as e:
        st.error(f"❌ Error fetching categories: {e}")
        return []

# Streamlit UI
st.title("Add New Product")

# Get categories and create a dropdown
categories = get_categories()

if categories:
    category_names = {cat_name: cat_id for cat_id, cat_name in categories}  # Mapping
    selected_category = st.selectbox("Select Category", category_names.keys())  # Show names

    # Get corresponding cat_id
    cat_id = category_names[selected_category]
else:
    st.warning("⚠ No categories found. Please add categories first.")
    cat_id = None

# Product form
with st.form("add_product_form"):
    product_name = st.text_input("Product Name")
    # stock_quantity = st.number_input("Stock Quantity", min_value=1, value=10)
    price = st.number_input("Price", min_value=0.01, value=10.0)

    submitted = st.form_submit_button("Add Product")

if submitted:
    if cat_id:
        add_product(product_name, price, cat_id)
    else:
        st.error("❌ Cannot add product. No valid category selected.")