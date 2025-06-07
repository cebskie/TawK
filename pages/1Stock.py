import streamlit as st
import pandas as pd
from core.db import fetch_categories, fetch_products_by_category, fetch_product_details

# Sidebar
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
st.sidebar.image("logo.svg")

# Streamlit UI
st.title("Check Product Stock")

# Get category names from the category table
try:
    categories = fetch_categories()
except Exception as e:
    st.error(f"Database connection error: {e}")
    categories = []

# Select category dropdown
category_options = {name: cat_id for cat_id, name in categories}
selected_category_name = st.selectbox("Select Category", list(category_options.keys()))
selected_category_id = category_options[selected_category_name]

# Fetch products based on selected category
if selected_category_id:
    try:
        products = fetch_products_by_category(selected_category_id)
    except Exception as e:
        st.error(f"Error fetching products: {e}")
        products = []

    # Product selection dropdown (only if products exist)
    if products:
        selected_product = st.selectbox("Select Product", products)

        # Show product details when button is clicked
        if st.button("Check Details"):
            try:
                result, columns = fetch_product_details(selected_product)
                if result:
                    df = pd.DataFrame(result, columns=columns)
                    st.dataframe(df)
                else:
                    st.warning(f"Product '{selected_product}' not found.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("No products found in this category.")
