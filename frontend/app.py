import streamlit as st
import pandas as pd
import datetime

# ----- Config -----
st.set_page_config(page_title="Walmart AI Dashboard", layout="wide")

# ----- Dummy login users -----
USERS = {"admin": "admin123", "jhanvi": "hello123"}

# ----- Session state -----
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ----- Load dataset -----
@st.cache_data
def load_data():
    df = pd.read_csv("../shared_assets/expanded_dataset_walmart_final_priced.csv", parse_dates=["last_restock_date", "next_restock_date"])
    return df

# ----- Login page -----
def login():
    st.title("🔐 Walmart Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

# ----- Dashboard page -----
def dashboard(df):
    st.title("📊 Walmart Inventory Dashboard")

    # --- Filters ---
    st.markdown("#### 🔍 Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.multiselect("Select Category", df["category"].unique())
    with col2:
        dept_filter = st.multiselect("Select Department", df["department"].unique())
    with col3:
        search_query = st.text_input("Search Item")

    # --- Date Filter ---
    date_range = st.selectbox("📅 Time Period", ["Last 7 Days", "Last 30 Days"])
    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=7 if "7" in date_range else 30)
    if "date" in df.columns:
        df = df[df["date"] >= pd.to_datetime(cutoff)]

    # --- Apply Filters ---
    if category_filter:
        df = df[df["category"].isin(category_filter)]
    if dept_filter:
        df = df[df["department"].isin(dept_filter)]
    if search_query:
        df = df[df["item_name"].str.contains(search_query, case=False)]

    # --- KPIs ---
    st.markdown("### 📌 Key Stats")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("✅ Items Donated", df[df["current_stock"] == 0].shape[0])
    kpi2.metric("📈 Avg. Predicted Demand", round(df["predicted_daily_sales"].mean(), 2))
    kpi3.metric("🌍 Avg. Carbon Score", round(df["carbon_score"].mean(), 2))

    # --- Data Table ---
    st.markdown("### 📦 Filtered Inventory")
    st.dataframe(df, use_container_width=True)

    # --- Action Recommendations ---
    st.markdown("### 🧠 Action Recommendations")
    for _, row in df.iterrows():
        if row["predicted_daily_sales"] < 30:
            st.warning(f"Consider donating **{row['item_name']}** (Low predicted demand: {row['predicted_daily_sales']})")

# ----- Donations -----
def donations():
    st.title("🎁 Donation Manager")
    st.info("Feature coming soon: Manage donation requests, approvals, and history.")

# ----- Forecasting -----
def forecasting():
    st.title("📉 Demand Forecasting")
    st.info("Feature coming soon: View demand predictions by category, department, and item.")

# ----- Authenticated flow -----
if st.session_state.logged_in:
    df = load_data()

    # Sidebar Navigation
    with st.sidebar:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Walmart_logo.svg/2560px-Walmart_logo.svg.png",
            width=200,
        )
        st.markdown("### 📂 Navigation")
        page = st.radio("Go to", ["Dashboard", "Donations", "Forecasting"])
        st.markdown("---")
        st.markdown("### 🔒 User")
        st.info(f"Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

    # Page rendering
    if page == "Dashboard":
        dashboard(df)
    elif page == "Donations":
        donations()
    elif page == "Forecasting":
        forecasting()

# ----- If not logged in -----
else:
    login()
