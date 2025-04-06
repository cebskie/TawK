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

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
st.sidebar.image("logo.svg", use_container_width=True)

# Streamlit UI
st.title("Check Product Stock")

# Get category names from the category table
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT c.cat_name FROM categories c JOIN products p ON c.cat_id = p.cat_id")  
    categories = [row[0] for row in cursor.fetchall()]  

    cursor.close()
    conn.close()
except Exception as e:
    st.error(f"Database connection error: {e}")
    categories = []

# Select category dropdown
selected_category = st.selectbox("Select Category", categories)

# Fetch products based on selected category
if selected_category:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get products where category name matches
        cursor.execute("""
            SELECT p.prod_name 
            FROM products p 
            JOIN categories c ON p.cat_id = c.cat_id 
            WHERE c.cat_name = %s
        """, (selected_category,))
        
        products = [row[0] for row in cursor.fetchall()]  

        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error fetching products: {e}")
        products = []

    # Product selection dropdown (only if products exist)
    if products:
        selected_product = st.selectbox("Select Product", products)

        # Show product details when button is clicked
        if st.button("Check Details"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Select * but also include the category name
                cursor.execute("""
                    SELECT p.prod_name AS Product, 
                               p.stock_quantity AS 'Available Stock',
                               p.price AS Price 
                    FROM products p 
                    JOIN categories c ON p.cat_id = c.cat_id 
                    WHERE p.prod_name = %s
                """, (selected_product,))
                
                columns = [desc[0] for desc in cursor.description]  # Get column names
                result = cursor.fetchall()

                cursor.close()
                conn.close()

                if result:
                    df = pd.DataFrame(result, columns=columns)  # Convert to DataFrame
                    st.dataframe(df)  # Display table
                    # df = pd.DataFrame(result, columns=columns)
                    # df = df.reset_index(drop=True)  # optional, but good for safety
                    # st.table(df)
                else:
                    st.warning(f"Product '{selected_product}' not found.")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("No products found in this category.")
