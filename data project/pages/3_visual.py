import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("📊 Data Distribution Dashboard")

# --- CHECK DATA ---
if "cleaned_df" in st.session_state:
    df = st.session_state["cleaned_df"]

    # Create the 50/50 screen split
    col1, col2 = st.columns(2)

    # ==========================================
    # LEFT COLUMN: NUMERIC DATA (HISTOGRAMS)
    # ==========================================
    with col1:
        st.subheader("📈 Numeric Analysis")
        # Filter for only number columns
        numeric_df = df.select_dtypes(include=['number'])

        if numeric_df.shape[1] > 0:
            # Dropdown for numeric columns
            # Note: We add a 'key' so Streamlit doesn't confuse the two dropdown menus
            num_col = st.selectbox("Select Numeric Column", numeric_df.columns, key="num_select")

            # Plot Seaborn Histogram
            fig, ax = plt.subplots()
            sns.histplot(df[num_col], kde=True, ax=ax, color='royalblue')
            ax.set_title(f"Distribution of {num_col}")
            st.pyplot(fig)
        else:
            st.warning("No numeric columns available for histogram")


   
    with col2:
        st.subheader("🥧 Category Analysis")
        
        # Filter out high-cardinality garbage (like IDs or full text)
        cat_columns = [col for col in df.columns if df[col].nunique() <= 100]

        if len(cat_columns) > 0:
            # Dropdown for categorical columns
            cat_col = st.selectbox("Select Categorical Column", cat_columns, key="cat_select")

            unique_count = df[cat_col].nunique()
            
            # Prepare the math for Plotly
            chart_data = df[cat_col].value_counts().reset_index()
            chart_data.columns = [cat_col, 'Count']

            # THE BRAIN: Pie Chart vs Bar Chart
            if 0 < unique_count <= 30:
                fig2 = px.pie(chart_data, names=cat_col, values='Count', hole=0.3)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                fig2 = px.bar(chart_data, x=cat_col, y='Count', color=cat_col)
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No categorical columns available.")

else:
    st.warning("⚠️ Please upload and clean data first on the Clean Data page.")
    st.stop()