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
if st.session_state.get("role") != "admin":
    st.error("Unauthorized access.")
    st.stop()
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
st.sidebar.image("logo.svg", use_container_width=True)

# Streamlit UI
st.title("Insights")


# --- Live Insights ---
st.header("📊 Live Inventory Insights")
@st.cache_data(ttl=300)
def load_live_insights():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Most Popular Products (most taken out)
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

        # 2. Low Stock Products
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
        st.error(f"Database error while loading live insights: {str(e)}")
        return None, None


# --- Display Live Insights (Vertically) ---
popular_df, low_stock_df = load_live_insights()

if popular_df is not None:
    st.markdown("### 🔥 Most Popular Products 🔥")
    st.dataframe(popular_df, use_container_width=True)

if low_stock_df is not None:
    st.markdown("### 📉 Lowest Stock Products 📉")
    st.dataframe(low_stock_df, use_container_width=True)

st.header("🔎 Monthly Insights")
# --- Year/Month Selection ---
col1, col2 = st.columns(2)
with col1:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT YEAR(date) AS year FROM transactions ORDER BY year DESC")
        years = [str(row[0]) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")
        years = ["2023"]  # fallback
    selected_year = st.selectbox("Select Year", years, index=0)

with col2:
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Select Month", months, index=0)
    month_num = months.index(selected_month) + 1

# --- Load Button ---
load_data = st.button("📥 Load Data")

# --- Data Loading Function ---
@st.cache_data(ttl=300)
def load_category_summary(year, month):
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
        st.error(f"Database error: {str(e)}")
        return None

# --- Show Summary on Button Click ---
if load_data:
    summary_df = load_category_summary(selected_year, month_num)

    if summary_df is not None:
        if not summary_df.empty:
            # --- Summary Metrics ---
            st.subheader(f"📈 {selected_month} {selected_year} Summary")

            total_in = summary_df["Stock In"].sum()
            total_out = summary_df["Stock Out"].sum()
            net_change = total_in - total_out

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Stock In", f"{total_in:,.0f}")
            col2.metric("Total Stock Out", f"{total_out:,.0f}")
            col3.metric("Net Change", f"{net_change:,.0f}", 
                        delta_color="inverse" if net_change < 0 else "normal")

            # --- Data Table ---
            st.subheader("📋 Category Details")

            styled_df = summary_df.style.format(
                "{:,.0f}", 
                subset=["Stock In", "Stock Out", "Net Change"]
            )

            st.dataframe(
                styled_df.apply(
                    lambda x: ['color: blue' if x.name == 'Stock In' else 
                              'color: red' if x.name == 'Stock Out' else 
                              '' for _ in x],
                    axis=0
                ),
                height=400,
                use_container_width=True
            )

            # --- Visualizations ---
            st.subheader("📊 Trends")
            tab1, tab2 = st.tabs(["Monthly Movement", "Category Ranking"])

            with tab1:
                st.line_chart(
                    summary_df.set_index("Category")[["Stock In", "Stock Out"]],
                    height=400
                )

            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**🔻Categories by Stock Out**")
                    st.bar_chart(
                        summary_df.set_index("Category")["Stock Out"].head(10),
                        color="#ff6b6b",
                        height=400
                    )
                with col2:
                    st.markdown("**📈 Net Change by Category**")
                    st.bar_chart(
                        summary_df.set_index("Category")["Net Change"],
                        color="#51cf66",
                        height=400
                    )
        else:
            st.info("No data found for the selected month.")
