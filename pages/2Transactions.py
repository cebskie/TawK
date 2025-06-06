import streamlit as st
from core.db import (
    check_authentication,
    render_sidebar,
    fetch_categories,
    get_category_id_map,
    fetch_products_by_category,
    execute_transaction,
)

def main():
    # Authentication & Sidebar
    check_authentication()
    render_sidebar()

    st.title("Inventory Transaction Management")

    # Fetch and map categories
    categories = fetch_categories()
    category_map = get_category_id_map()

    selected_category = st.selectbox("Select Category", category_map.keys())

    if selected_category:
        cat_id = category_map[selected_category]
        products = fetch_products_by_category(cat_id)

        if products:
            selected_product = st.selectbox("Select Product", products)

            with st.form("transaction_form"):
                st.subheader("Enter Transaction Details")
                trans_type = st.selectbox("Transaction Type", ["in", "out"])
                quantity = st.number_input("Quantity", min_value=1, value=5)
                submitted = st.form_submit_button("Execute Transaction")

            if submitted:
                user_id = st.session_state.get("user_id", None)
                if user_id is not None:
                    execute_transaction(selected_product, trans_type, quantity, user_id)
                else:
                    st.error("User is not logged in. Please log in to record a transaction.")
        else:
            st.warning("No products found in this category.")

if __name__ == "__main__":
    main()
