import pandas as pd
import os

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    initial_rows = len(df)
    print(f"Initial rows: {initial_rows}")

    # 1. Drop rows with missing Data_Value
    df_clean = df.dropna(subset=['Data_Value'])
    print(f"Rows after dropping missing Data_Value: {len(df_clean)}")

    # 2. Select relevant columns
    # We need: YearStart, LocationAbbr, LocationDesc, Class, Topic, Question, Data_Value, 
    # StratificationCategory1, Stratification1, GeoLocation
    cols_to_keep = [
        'YearStart', 'LocationAbbr', 'LocationDesc', 'Class', 'Topic', 'Question', 
        'Data_Value', 'Data_Value_Unit', 'StratificationCategory1', 'Stratification1', 'GeoLocation'
    ]
    # Check if all columns exist
    missing_cols = [c for c in cols_to_keep if c not in df_clean.columns]
    if missing_cols:
        print(f"Warning: Missing columns: {missing_cols}")
        return

    df_clean = df_clean[cols_to_keep]

    # 3. Standardize Year
    df_clean = df_clean.rename(columns={'YearStart': 'Year'})

    # 4. Save cleaned data
    print(f"Saving cleaned data to {output_path}...")
    df_clean.to_csv(output_path, index=False)
    print("Data cleaning complete.")

if __name__ == "__main__":
    input_csv = 'Nutrition__Physical_Activity__and_Obesity_-_Behavioral_Risk_Factor_Surveillance_System.csv'
    output_csv = 'cleaned_data.csv'
    clean_data(input_csv, output_csv)
