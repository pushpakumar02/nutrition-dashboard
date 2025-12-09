import streamlit as st
import pandas as pd
import altair as alt
import os

# Set page config
st.set_page_config(page_title="Nutrition & Obesity Dashboard", layout="wide")

# Title
st.title("Nutrition, Physical Activity, and Obesity Dashboard")

# Load Data
@st.cache_data
def load_data():
    if os.path.exists('cleaned_data.csv'):
        return pd.read_csv('cleaned_data.csv')
    else:
        st.error("Data file 'cleaned_data.csv' not found. Please run data cleaning first.")
        return None

df = load_data()

if df is not None:
    # --- Sidebar Filters ---
    st.sidebar.header("Global Filters")
    
    # Year Filter
    years = sorted(df['Year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Select Year", years, index=0)
    
    # Class Filter (Obesity, Physical Activity, etc.)
    classes = df['Class'].unique()
    selected_class = st.sidebar.selectbox("Select Category", classes, index=0)

    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.header("Navigation")
    options = [
        "1. Background & Intro", 
        "2. Data Cleaning & Stats",
        "3. Q1: Temporal Trends", 
        "4. Q2: Geographic Analysis", 
        "5. Q3: Demographic Analysis", 
        "6. Correlation Analysis", 
        "7. Q&A Prep",
        "8. Summary & Conclusion"
    ]
    selection = st.sidebar.radio("Go to", options)

    # --- 1. Background & Intro ---
    if selection == "1. Background & Intro":
        st.header("1. Background and Introduction")
        st.markdown("""
        ### Dataset Overview
        This dashboard analyzes data from the **Nutrition, Physical Activity, and Obesity - Behavioral Risk Factor Surveillance System**. 
        It provides state-level data on the health behaviors and status of adults in the United States.

        ### Public Health Importance
        Obesity is a major public health issue linked to chronic diseases such as diabetes, heart disease, and cancer. 
        Understanding the trends, geographic distribution, and demographic disparities of obesity and its related factors (physical activity, nutrition) is crucial for:
        *   **Policy Making**: Targeting resources to high-need areas.
        *   **Intervention Planning**: Designing effective programs for specific demographic groups.
        *   **Health Promotion**: Raising awareness about the importance of healthy behaviors.
        """)
        st.info("Use the sidebar to filter the data by Year and Category.")

    # --- 2. Data Cleaning & Stats ---
    elif selection == "2. Data Cleaning & Stats":
        st.header("2. Data Cleaning, Statistics, and Analysis")
        
        st.subheader("Data Cleaning Process")
        st.markdown("""
        The raw dataset contained over 100,000 rows. The following cleaning steps were performed:
        1.  **Handling Missing Values**: Rows with missing `Data_Value` were removed to ensure analysis accuracy.
        2.  **Column Selection**: Only relevant columns (Year, Location, Class, Topic, Question, Data_Value, Stratification) were retained.
        3.  **Standardization**: Column names were standardized for consistency.
        """)
        
        st.subheader("Summary Statistics (Filtered Data)")
        # Filter based on sidebar selection
        df_stats = df[(df['Class'] == selected_class) & (df['Year'] == selected_year)]
        
        if not df_stats.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean Value (%)", f"{df_stats['Data_Value'].mean():.2f}")
            with col2:
                st.metric("Median Value (%)", f"{df_stats['Data_Value'].median():.2f}")
            with col3:
                st.metric("Total Records", f"{len(df_stats)}")
            
            st.write("### Data Preview")
            st.dataframe(df_stats.head())
        else:
            st.warning("No data available for the selected filters.")

    # --- 3. Temporal Trends ---
    elif selection == "3. Q1: Temporal Trends":
        st.header("Q1: How have health metrics changed over time?")
        st.markdown("This interactive chart shows the trend of the selected category over the years. **Hover** over points for details. **Zoom** and **Pan** are enabled.")
        
        # Filter for Total population to show general trend
        df_trend = df[(df['Class'] == selected_class) & (df['StratificationCategory1'] == 'Total')]
        
        # Aggregate
        trend_data = df_trend.groupby(['Year', 'Question'])['Data_Value'].mean().reset_index()
        
        # Altair Chart
        chart = alt.Chart(trend_data).mark_line(point=True).encode(
            x=alt.X('Year:O', title='Year'),
            y=alt.Y('Data_Value', title='Percentage (%)', scale=alt.Scale(zero=False)),
            color='Question',
            tooltip=['Year', 'Question', alt.Tooltip('Data_Value', format='.1f')]
        ).properties(
            width=800,
            height=500,
            title=f"Trends in {selected_class} (2011-2023)"
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)

    # --- 4. Geographic Analysis ---
    elif selection == "4. Q2: Geographic Analysis":
        st.header("Q2: Which states have the highest/lowest rates?")
        st.markdown(f"Ranking of states for **{selected_class}** in **{selected_year}**.")
        
        # Filter data
        questions = df[df['Class'] == selected_class]['Question'].unique()
        selected_question = st.selectbox("Select Metric", questions, index=0)
        
        df_geo = df[(df['Year'] == selected_year) & 
                    (df['Question'] == selected_question) & 
                    (df['StratificationCategory1'] == 'Total')]
        
        # Sort for better visualization
        df_geo = df_geo.sort_values('Data_Value', ascending=False)
        
        # Altair Bar Chart (Better for ranking than a map without geojson)
        chart = alt.Chart(df_geo).mark_bar().encode(
            x=alt.X('Data_Value', title='Percentage (%)'),
            y=alt.Y('LocationDesc', sort='-x', title='State'),
            color=alt.Color('Data_Value', scale=alt.Scale(scheme='viridis')),
            tooltip=['LocationDesc', 'Data_Value', 'Year']
        ).properties(
            height=800,
            title=f"State Rankings for {selected_question} ({selected_year})"
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)

    # --- 5. Demographic Analysis ---
    elif selection == "5. Q3: Demographic Analysis":
        st.header("Q3: How do metrics vary by Demographics?")
        
        demo_cats = ['Income', 'Education', 'Age (years)', 'Race/Ethnicity', 'Sex']
        selected_demo = st.selectbox("Select Demographic Category", demo_cats)
        
        # Filter
        questions = df[df['Class'] == selected_class]['Question'].unique()
        selected_question_demo = st.selectbox("Select Metric", questions, index=0)
        
        df_demo = df[(df['StratificationCategory1'] == selected_demo) & 
                     (df['Question'] == selected_question_demo) &
                     (df['Year'] == selected_year)] # Use global year filter
        
        # Aggregate
        demo_agg = df_demo.groupby('Stratification1')['Data_Value'].mean().reset_index()
        
        # Altair Chart
        chart = alt.Chart(demo_agg).mark_bar().encode(
            x=alt.X('Stratification1', title=selected_demo, sort='-y'),
            y=alt.Y('Data_Value', title='Percentage (%)'),
            color=alt.Color('Stratification1', legend=None),
            tooltip=['Stratification1', alt.Tooltip('Data_Value', format='.1f')]
        ).properties(
            title=f"Average {selected_question_demo} by {selected_demo} ({selected_year})"
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)

    # --- 6. Correlation Analysis ---
    elif selection == "6. Correlation Analysis":
        st.header("Correlation: Obesity vs. Physical Inactivity")
        st.markdown(f"Analyzing the relationship for **{selected_year}**.")
        
        # Prepare data
        df_corr = df[(df['Year'] == selected_year) & (df['StratificationCategory1'] == 'Total')]
        
        q_obesity = 'Percent of adults aged 18 years and older who have obesity'
        q_inactivity = 'Percent of adults who engage in no leisure-time physical activity'
        
        # Check if questions exist in the dataset
        available_questions = df_corr['Question'].unique()
        has_obesity = any(q_obesity in q for q in available_questions)
        has_inactivity = any(q_inactivity in q for q in available_questions)

        if has_obesity and has_inactivity:
            # We need to be careful with exact string matching, so let's filter by substring if needed
            # But the dataset seems consistent.
            df_obesity = df_corr[df_corr['Question'] == q_obesity][['LocationAbbr', 'Data_Value', 'LocationDesc']].rename(columns={'Data_Value': 'Obesity_Rate'})
            df_inactivity = df_corr[df_corr['Question'] == q_inactivity][['LocationAbbr', 'Data_Value']].rename(columns={'Data_Value': 'Inactivity_Rate'})
            
            merged = pd.merge(df_obesity, df_inactivity, on='LocationAbbr')
            
            if not merged.empty:
                corr_coeff = merged['Obesity_Rate'].corr(merged['Inactivity_Rate'])
                st.metric("Correlation Coefficient", f"{corr_coeff:.2f}")
                
                # Altair Scatter Plot
                chart = alt.Chart(merged).mark_circle(size=60).encode(
                    x=alt.X('Inactivity_Rate', title='Physical Inactivity (%)', scale=alt.Scale(zero=False)),
                    y=alt.Y('Obesity_Rate', title='Obesity Rate (%)', scale=alt.Scale(zero=False)),
                    tooltip=['LocationDesc', 'Obesity_Rate', 'Inactivity_Rate']
                ).properties(
                    title=f"Obesity vs. Inactivity ({selected_year})"
                ).interactive()
                
                # Regression line
                line = chart.transform_regression('Inactivity_Rate', 'Obesity_Rate').mark_line(color='red')
                
                st.altair_chart(chart + line, use_container_width=True)
            else:
                st.warning("Not enough data to perform correlation analysis for this year.")
        else:
            st.warning("Required data for correlation (Obesity & Inactivity) not found for this year.")

    # --- 7. Q&A Prep ---
    elif selection == "7. Q&A Prep":
        st.header("7. Q&A Preparation")
        st.markdown("### Potential Professor Questions & Answers")
        
        qa_pairs = [
            ("1. How did you handle missing data?", 
             "I removed rows where the primary metric (`Data_Value`) was missing. I also filtered out rows with insufficient sample sizes if they were flagged in the dataset."),
            ("2. Is there any bias in this dataset?", 
             "Yes, BRFSS data is self-reported via telephone surveys. This can lead to **social desirability bias** (underreporting weight, overreporting activity) and **selection bias** (excluding those without phones)."),
            ("3. Why did you choose these specific variables for correlation?", 
             "I chose Obesity and Physical Inactivity because literature suggests a strong energy-balance link. Inactivity is a modifiable risk factor directly related to weight gain."),
            ("4. Did you identify any outliers?", 
             "Yes, in the geographic analysis, certain states (e.g., West Virginia, Mississippi) consistently appeared as outliers with significantly higher obesity rates compared to the national average."),
            ("5. What are the limitations of your analysis?", 
             "The analysis is correlational, not causal. We cannot prove inactivity causes obesity from this data alone. Also, the aggregated state-level data masks local variations within states.")
        ]
        
        for q, a in qa_pairs:
            with st.expander(q):
                st.write(a)

    # --- 8. Summary & Conclusion ---
    elif selection == "8. Summary & Conclusion":
        st.header("8. Summary and Conclusion")
        st.markdown("""
        ### Summary of Insights
        1.  **Rising Trends**: Obesity rates have shown a concerning upward trend from 2011 to 2023 across the US.
        2.  **Geographic Hotspots**: The South and Midwest regions consistently exhibit higher rates of obesity and physical inactivity.
        3.  **Socioeconomic Link**: There is a clear gradient where lower income and education levels correlate with poorer health outcomes.
        4.  **Behavioral Connection**: A strong positive correlation exists between physical inactivity and obesity prevalence.

        ### Conclusion
        The dashboard successfully highlights the multi-dimensional nature of the obesity epidemic. The data suggests that interventions must be multi-faceted, targeting not just individual behaviors but also the socioeconomic and environmental determinants of health. 
        Future work could incorporate county-level data for more granular insights.
        """)
