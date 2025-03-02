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

# Fetch categories from the database
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cat_id, cat_name FROM categories")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return categories  # Returns a list of tuples [(1, 'Electronics'), (2, 'Clothing')]
    except Exception as e:
        st.error(f"Error fetching categories: {e}")
        return []

# Fetch products based on selected category
def get_products_by_category(cat_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT prod_name FROM products WHERE cat_id = %s", (cat_id,))
        products = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return products
    except Exception as e:
        st.error(f"Error fetching products: {e}")
        return []

# Function to execute stored procedure for transactions
def execute_transaction(product_name, trans_type, quantity, cat_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc("recordTransaction", (product_name, trans_type, quantity, cat_id))
        conn.commit()
        st.success("Transaction recorded successfully!")
    except Exception as e:
        st.error(f"Error executing transaction: {e}")
    finally:
        cursor.close()
        conn.close()

# UI
st.title("Inventory Transaction Management")
st.sidebar.image("TawK logo.png", use_container_width=True)

# Get categories for dropdown
categories = get_categories()
category_options = {name: cat_id for cat_id, name in categories}  # Map category name → ID

# Category selection dropdown
selected_category = st.selectbox("Select Category", category_options.keys())

# Fetch products if a category is selected
if selected_category:
    cat_id = category_options[selected_category]
    products = get_products_by_category(cat_id)

    if products:
        # Product selection dropdown
        selected_product = st.selectbox("Select Product", products)

        # User input form
        with st.form("transaction_form"):
            st.subheader("Enter Transaction Details")
            trans_type = st.selectbox("Transaction Type", ["in", "out"])
            quantity = st.number_input("Quantity", min_value=1, value=5)

            submitted = st.form_submit_button("Execute Transaction")

        # Execute transaction if submitted
        if submitted:
            execute_transaction(selected_product, trans_type, quantity, cat_id)
    else:
        st.warning("No products found in this category.")
