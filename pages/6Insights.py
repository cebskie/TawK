import streamlit as st
import pandas as pd
from core.db import fetch_live_insights, fetch_available_years, fetch_monthly_category_summary

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
st.sidebar.image("logo.svg")

# Streamlit UI
st.title("Insights")


# --- Live Insights ---
st.header("📊 Live Inventory Insights")

@st.cache_data(ttl=300)
def load_live_insights():
    return fetch_live_insights()

popular_df, low_stock_df = load_live_insights()

if popular_df is not None:
    st.markdown("### 🔥 Most Popular Products 🔥")
    st.dataframe(popular_df, use_container_width=True)

if low_stock_df is not None:
    st.markdown("### 📉 Lowest Stock Products 📉")
    st.dataframe(low_stock_df, use_container_width=True)


# --- Monthly Insights ---
st.header("🔎 Monthly Insights")

# --- Year/Month Selection ---
col1, col2 = st.columns(2)
with col1:
    years = fetch_available_years()
    selected_year = st.selectbox("Select Year", years, index=0)

with col2:
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Select Month", months, index=0)
    month_num = months.index(selected_month) + 1

# --- Load Button ---
load_data = st.button("📥 Load Data")

@st.cache_data(ttl=300)
def load_category_summary(year, month):
    return fetch_monthly_category_summary(year, month)

# --- Show Summary ---
if load_data:
    summary_df = load_category_summary(selected_year, month_num)

    if summary_df is not None and not summary_df.empty:
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

        # --- Category Table ---
        st.subheader("📋 Category Details")
        styled_df = summary_df.style.format(
            "{:,.0f}", subset=["Stock In", "Stock Out", "Net Change"]
        )
        st.dataframe(styled_df, height=400, use_container_width=True)

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