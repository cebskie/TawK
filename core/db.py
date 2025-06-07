import mysql.connector
import streamlit as st
import pandas as pd
import os

# Connect to DB (Streamlit Cloud or local)
def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='root',
        password='',
        database='inventory'
    )


def check_authentication():
    if not st.session_state.get("logged_in"):
        st.warning("Please log in to access this page.")
        st.stop()

    if st.session_state.get("role") != "admin":
        st.error("Unauthorized access.")
        st.stop()


def render_sidebar():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.sidebar.image("logo.svg")


def fetch_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.cat_id, c.cat_name
            FROM categories c
            JOIN products p ON c.cat_id = p.cat_id
        """)
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return categories
    except Exception as e:
        st.error(f"Error fetching categories: {e}")
        return []


def fetch_products_by_category(cat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT prod_name FROM products WHERE cat_id = %s", (cat_id,))
    products = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return products


def fetch_product_details(product_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.prod_name AS Product,
               p.stock_quantity AS 'Available Stock',
               p.price AS Price
        FROM products p
        JOIN categories c ON p.cat_id = c.cat_id
        WHERE p.prod_name = %s
    """, (product_name,))
    columns = [desc[0] for desc in cursor.description]
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result, columns

def get_category_id_map():
    rows = fetch_categories()
    return {name: cat_id for cat_id, name in rows}

# Transactions
def execute_transaction(product_name, trans_type, quantity, user_id): # Need to add User ID from the session
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc("recordTransaction", (product_name, trans_type, quantity, user_id))
        conn.commit()
        st.success("Transaction recorded successfully!")
    except Exception as e:
        st.error(f"Error executing transaction: {e}")
    finally:
        cursor.close()
        conn.close()

# Transactions Log
def fetch_transaction_logs(limit=10):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                tl.log_id AS 'log ID',
                tl.transaction_id AS 'transaction ID',
                p.prod_name AS 'product',
                tl.type,
                tl.date,
                u.u_name AS 'user name'
            FROM transaction_log tl
            JOIN products p ON tl.prod_id = p.prod_id
            JOIN users u ON tl.u_id = u.u_id
            ORDER BY tl.log_id DESC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        cursor.close()
        conn.close()
        return pd.DataFrame(rows, columns=columns)

    except Exception as e:
        st.error(f"Error fetching transaction logs: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    

def render_transaction_logs():
    st.title("Transactions Log")

    df = fetch_transaction_logs()
    if df.empty:
        st.info("No transaction logs found.")
        return

    st.dataframe(
        df.style.set_properties(
            **{"white-space": "pre-wrap", "word-wrap": "break-word"}
        ),
        use_container_width=True
    )


# Users
def register_user_to_db(username, address, phone):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.callproc("registerUser", (username, address, phone))

    conn.commit()
    cursor.close()
    conn.close()


def search_user_from_db(user_search):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE u_id = %s OR u_name = %s",
        (user_search, user_search)
    )

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return rows, columns

# Add Product


# Insights
def fetch_live_insights():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Most Popular Products (most taken out)
        cursor.execute("""
            SELECT prod_name AS Product, SUM(t.quantity) AS Taken_Out
            FROM transactions t
            JOIN products p ON t.prod_id = p.prod_id
            WHERE t.type = 'out'
            GROUP BY p.prod_id
            ORDER BY Taken_Out DESC
            LIMIT 10
        """)
        popular = pd.DataFrame(cursor.fetchall(), columns=["Product", "Taken Out"])

        # Low Stock Products
        cursor.execute("""
            SELECT prod_name AS Product, stock_quantity AS Stock
            FROM products
            ORDER BY stock_quantity ASC
            LIMIT 10
        """)
        low_stock = pd.DataFrame(cursor.fetchall(), columns=["Product", "Stock"])

        cursor.close()
        conn.close()

        return popular, low_stock

    except Exception as e:
        print(f"[DB ERROR] fetch_live_insights: {e}")
        return None, None


def fetch_available_years():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT YEAR(date) AS year FROM transactions ORDER BY year DESC")
        years = [str(row[0]) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return years
    except Exception as e:
        print(f"[DB ERROR] fetch_available_years: {e}")
        return ["2023"]  # fallback


def fetch_monthly_category_summary(year, month):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                c.cat_name AS Category,
                CAST(SUM(CASE WHEN t.type = 'in' THEN t.quantity ELSE 0 END) AS FLOAT) AS "Stock In",
                CAST(SUM(CASE WHEN t.type = 'out' THEN t.quantity ELSE 0 END) AS FLOAT) AS "Stock Out",
                CAST(SUM(CASE WHEN t.type = 'in' THEN t.quantity ELSE 0 END) - 
                     SUM(CASE WHEN t.type = 'out' THEN t.quantity ELSE 0 END) AS FLOAT) AS "Net Change",
                COUNT(DISTINCT t.prod_id) AS "Unique Products"
            FROM transactions t
            JOIN products p ON t.prod_id = p.prod_id
            JOIN categories c ON p.cat_id = c.cat_id
            WHERE YEAR(t.date) = %s
              AND MONTH(t.date) = %s
            GROUP BY c.cat_name
            ORDER BY "Stock Out" DESC
        """
        cursor.execute(query, (year, month))
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if data:
            df = pd.DataFrame(data, columns=columns)
            numeric_cols = ["Stock In", "Stock Out", "Net Change"]
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
            return df
        return pd.DataFrame()

    except Exception as e:
        print(f"[DB ERROR] fetch_monthly_category_summary: {e}")
        return None
    

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
