import streamlit as st
import pandas as pd
import plotly.express as px  # <--- This is the missing piece!
import google.generativeai as genai

# Add render_mode="svg" to your px.line call
fig = px.line(df, x="Year", y=["CVD_Mortality_Rate", "Obesity_Prevalence"], 
              render_mode="svg",  # <--- Add this!
              markers=True)

# --- 1. SETUP ---
st.set_page_config(page_title="Cardio-Risk Explorer", layout="wide")
try:
    genai.configure(api_key=st.secrets["AIzaSyCsXL7XQ4JtLR40wThSvzlCb59vQZ7p6ck"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Please set your GEMINI_API_KEY in Streamlit Secrets.")

# --- 2. THE DATA (Simulated Global Trends) ---
# In a full app, you would load this from a CSV
data = {
    "Year": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "CVD_Mortality_Rate": [345, 342, 355, 360, 352, 348, 340, 335], # Deaths per 100k
    "Obesity_Prevalence": [12.1, 12.4, 13.2, 13.8, 14.1, 14.5, 14.8, 15.2], # % of population
}
df = pd.DataFrame(data)

# --- 3. UI LAYOUT ---
st.title("📊 Cardio-Risk Explorer")
st.markdown("### Regional Cardiometabolic Trend Analysis (2018-2025)")

col1, col2 = st.columns([2, 1])

with col1:
    # Interactive Chart
    fig = px.line(df, x="Year", y=["CVD_Mortality_Rate", "Obesity_Prevalence"], 
                  title="Cardiovascular Mortality vs. Obesity Trends",
                  labels={"value": "Rate / Percentage", "variable": "Metric"},
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("### AI Analysis")
    selected_year = st.selectbox("Select a Year for Deep Dive:", df["Year"])
    
    # Get data for that specific year
    year_data = df[df["Year"] == selected_year].iloc[0]
    
    if st.button("Generate Health Insights"):
        with st.spinner("Analyzing global health drivers..."):
            prompt = f"""
            You are a senior public health data scientist. 
            Analyze these cardiometabolic stats for the year {selected_year}:
            - Cardiovascular Mortality: {year_data['CVD_Mortality_Rate']} per 100k
            - Obesity Prevalence: {year_data['Obesity_Prevalence']}%
            
            Based on global health trends (like the COVID-19 impact in 2020-2021 or 
            recent breakthroughs in GLP-1 medications), explain the 'why' behind 
            these numbers and provide one recommendation for health officials.
            """
            response = model.generate_content(prompt)
            st.info(response.text)

# --- 4. DATA TABLE ---
with st.expander("View Raw Global Statistics"):
    st.table(df)
