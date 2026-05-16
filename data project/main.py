import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# --- TITLE ---
st.title("📊 Data Cleaning & Visualization App")

# --- INTRO ---
st.markdown("""
Welcome to your **Data Analysis Dashboard** 🚀

This app helps you:
- 🧹 Clean messy datasets
- 📈 Analyze correlations
- 📊 Visualize data distributions
""")

st.divider()

# --- HOW TO USE ---
st.subheader("📌 How to Use")

st.markdown("""
1. Go to **🧹 Clean Data** page from sidebar  
2. Upload your dataset (CSV / Excel)  
3. Cleaned data will be saved automatically  
4. Visit:
   - 📈 Correlation page → to see relationships  
   - 📊 visual page → to see distributions  
""")

st.divider()

# --- SESSION STATUS ---
st.subheader("📡 Data Status")

if "cleaned_df" in st.session_state:
    df = st.session_state["cleaned_df"]

    st.success("✅ Data is loaded and ready for analysis")

    st.write("### Preview of your data:")
    st.dataframe(df.head())

    st.info(f"Shape: {df.shape}")

else:
    st.warning("⚠️ No data loaded yet")
    st.info("👉 Please go to **Clean Data** page and upload a dataset")