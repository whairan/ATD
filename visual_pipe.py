import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------
# Data Ingestion & Preparation Pipeline
# -------------------------------------
@st.cache
def load_data(file) -> pd.DataFrame:
    """Load and clean data from an uploaded CSV file."""
    # Read CSV into a DataFrame
    df = pd.read_csv(file)
    
    # Basic cleaning: drop rows with all missing values
    df.dropna(how="all", inplace=True)
    
    # Example: if a 'date' column exists, convert to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # Drop rows with invalid dates
        df = df.dropna(subset=['date'])
    
    return df

# -------------------------
# Dashboard Layout & Design
# -------------------------
st.title("Interactive Data Visualization Dashboard")

st.markdown("""
This dashboard demonstrates a simple data pipeline and interactive visualizations. 
Upload a CSV file to begin, and use the widgets below to filter your data and choose your visualization.
""")

# File uploader for CSV input
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load data
    data = load_data(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(data.head())

    # --------------------------
    # Data Filtering (Interactivity)
    # --------------------------
    df = data.copy()
    
    # If the dataset has a 'date' column, allow filtering by date range
    if 'date' in df.columns:
        st.subheader("Filter by Date")
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        start_date, end_date = st.slider("Select date range", min_value=min_date, max_value=max_date,
                                         value=(min_date, max_date))
        df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    
    st.subheader("Filtered Data")
    st.dataframe(df.head())

    # --------------------------
    # Visualization Options
    # --------------------------
    st.subheader("Visualization Options")
    # Let the user choose a chart type and which columns to plot
    chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Scatter Plot"])

    # Choose columns for x and y axes (only numerical and date columns for y)
    columns = df.columns.tolist()
    x_col = st.selectbox("Select X-axis", columns)
    y_col = st.selectbox("Select Y-axis", columns)
    
    # -------------------------------------
    # Generate and Display the Visualization
    # -------------------------------------
    st.subheader("Chart")
    if chart_type == "Line Chart":
        fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart of {y_col} vs {x_col}")
    elif chart_type == "Bar Chart":
        fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart of {y_col} vs {x_col}")
    elif chart_type == "Scatter Plot":
        fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot of {y_col} vs {x_col}")

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # Additional Dashboard Elements
    # -------------------------
    st.markdown("""
    **Additional Features:**
    - Use the sidebar for additional filters.
    - Modify the code to include more complex aggregations or visualizations.
    - Integrate data from APIs or databases by extending the data ingestion function.
    """)
else:
    st.info("Please upload a CSV file to begin.")
