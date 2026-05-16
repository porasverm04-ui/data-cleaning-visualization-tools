import pandas as pd
import streamlit as st 

st.set_page_config(page_title="Data Cleaner", layout="wide")
st.title("📊 DATA VISUALIZATION DASHBOARD")

uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # --- LOADING DATA ---
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        df1 = df.copy()
    else:
        df = pd.read_excel(uploaded_file)
        df1=df.copy()
    
    st.success(f"File '{uploaded_file.name}' loaded successfully!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Raw Data")
        st.write(df)
        st.info(f"Original Shape: {df.shape}")

    # --- AUTO CLEANING LOGIC ---
    
    # 1. Date Conversion
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    for date_col in date_columns:
        df[date_col] = pd.to_datetime(df[date_col], format='mixed', errors='coerce')

    # 2. Row Purge (Missing < 5%)
    missing_percentages = df.isnull().mean() * 100
    columns_to_purge = missing_percentages[(missing_percentages > 0) & (missing_percentages < 5)].index.tolist()
    
    if columns_to_purge:
        df = df.dropna(subset=columns_to_purge)
        df = df.reset_index(drop=True)

    # 3. Handling Remaining Missing Values & Formatting
    total_columns=len(df.columns)
    for n in range (0,total_columns):
        nth_column=df.iloc[:, n]

        data_type=str(nth_column.dtype)
        if nth_column.isnull().any()== True:
            if "object"in data_type:
                df.iloc[:, n] = nth_column.fillna("Unknown")
                ##handles all the values which same but differnt in format like "new york " and "NEW YORK"
                df.iloc[:, n] = df.iloc[:, n].astype(str).str.strip().str.title()

            elif "int64" in data_type:
                df.iloc[:, n] = nth_column.fillna(nth_column.mean())

            elif "float64" in data_type:
                df.iloc[:, n] = nth_column.fillna(nth_column.mean())

            elif  "datetime64" in data_type:
                df = df.dropna(subset=[nth_column.name])
                df = df.reset_index(drop=True)
    # --- DISPLAY CLEAN DATA 
    with col2:
        st.subheader("Cleaned Data")
        st.write(df)
        st.success(f"Cleaned Shape: {df.shape}")
    
     # --- OPTIONAL: DOWNLOAD BUTTON -
    st.divider()
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Cleaned CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")

     #link to next page   
    st.session_state["cleaned_df"] = df
    st.session_state["raw_df"] = df1

elif "cleaned_df" in st.session_state:
    df = st.session_state["cleaned_df"]
    df1 = st.session_state["raw_df"]
    st.info("Showing previously cleaned data (no need to upload again)")

    # 👉 SHOW DATA AGAIN
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Raw Data (Saved)")
        st.write(df1)
        st.info(f"Shape: {df1.shape}")

    with col2:
        st.subheader("Cleaned Data (Saved)")
        st.write(df)
        st.success(f"Shape: {df.shape}")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Cleaned CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")

    