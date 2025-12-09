# Nutrition, Physical Activity, and Obesity Analysis

**Course:** DSA 5200: Advanced Data Visualization  
**Dataset Source:** Centers for Disease Control and Prevention (CDC) - Behavioral Risk Factor Surveillance System

## Project Overview

This project presents an interactive dashboard analyzing health data related to nutrition, physical activity, and obesity in the United States. The analysis utilizes the "Nutrition, Physical Activity, and Obesity - Behavioral Risk Factor Surveillance System" dataset to explore trends and disparities across different states and demographic groups.

**Live Demo:** [https://nutrition-dashboard.streamlit.app/](https://nutrition-dashboard.streamlit.app/)

## Key Research Questions

The analysis focuses on three primary dimensions:

1.  **Temporal Trends:** How have obesity and physical activity rates changed from 2011 to 2023?
2.  **Geographic Analysis:** What are the spatial patterns of these health metrics across the United States? Which states exhibit the highest and lowest rates?
3.  **Demographic Disparities:** How do health outcomes vary by income, education, age, and race/ethnicity?

## Repository Structure

*   `dashboard.py`: The main application script built with Streamlit and Altair.
*   `data_cleaning.py`: Script used for preprocessing the raw CDC dataset.
*   `cleaned_data.csv`: The processed dataset used for the dashboard.
*   `requirements.txt`: List of Python dependencies.

## Installation and Usage

To run this dashboard locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pushpakumar02/nutrition-dashboard.git
    cd nutrition-dashboard
    ```

2.  **Install dependencies:**
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run dashboard.py
    ```

The dashboard will open in your default web browser at `http://localhost:8501`.
