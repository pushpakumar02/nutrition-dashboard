import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

def analyze_data(input_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Loading cleaned data from {input_path}...")
    df = pd.read_csv(input_path)

    # --- 1. Temporal Trends ---
    print("Analyzing Temporal Trends...")
    # Group by Year and Class (Obesity, Physical Activity, etc.)
    # We filter for 'Total' stratification to get the general population trend
    df_total = df[df['StratificationCategory1'] == 'Total']
    
    yearly_trends = df_total.groupby(['Year', 'Class'])['Data_Value'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=yearly_trends, x='Year', y='Data_Value', hue='Class', marker='o')
    plt.title('Trends in Obesity, Physical Activity, and Nutrition (2011-2023)')
    plt.ylabel('Percentage (%)')
    plt.xlabel('Year')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/temporal_trends.png")
    plt.close()

    # --- 2. Geographic Analysis (Latest Year) ---
    print("Analyzing Geographic Trends...")
    latest_year = df['Year'].max()
    print(f"Latest year in dataset: {latest_year}")
    
    # Filter for Obesity in the latest year, Total population
    obesity_geo = df[(df['Year'] == latest_year) & 
                     (df['Class'] == 'Obesity / Weight Status') & 
                     (df['StratificationCategory1'] == 'Total') &
                     (df['Question'] == 'Percent of adults aged 18 years and older who have obesity')]
    
    # Sort by obesity rate
    obesity_geo_sorted = obesity_geo.sort_values('Data_Value', ascending=False)
    
    # Top 10 and Bottom 10 States
    top_10 = obesity_geo_sorted.head(10)
    bottom_10 = obesity_geo_sorted.tail(10)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(data=pd.concat([top_10, bottom_10]), x='Data_Value', y='LocationDesc', palette='viridis')
    plt.title(f'Top 10 and Bottom 10 States by Obesity Rate ({latest_year})')
    plt.xlabel('Obesity Rate (%)')
    plt.ylabel('State')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/geographic_obesity_ranking.png")
    plt.close()

    # --- 3. Demographic Analysis ---
    print("Analyzing Demographic Trends...")
    # Analyze by Income, Education, Age, Race
    demographics = ['Income', 'Education', 'Age (years)', 'Race/Ethnicity']
    
    for demo in demographics:
        # Filter for Obesity, all years combined (or could do latest year)
        df_demo = df[(df['Class'] == 'Obesity / Weight Status') & 
                     (df['Question'] == 'Percent of adults aged 18 years and older who have obesity') &
                     (df['StratificationCategory1'] == demo)]
        
        # Calculate mean obesity rate for each group
        demo_stats = df_demo.groupby('Stratification1')['Data_Value'].mean().sort_values().reset_index()
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=demo_stats, x='Data_Value', y='Stratification1', palette='magma')
        plt.title(f'Average Obesity Rate by {demo} (2011-2023)')
        plt.xlabel('Obesity Rate (%)')
        plt.ylabel(demo)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/demographic_{demo.replace('/', '_').replace(' ', '_')}.png")
        plt.close()

    # --- 4. Correlation Analysis ---
    print("Analyzing Correlations...")
    # We want to see if Physical Activity correlates with Obesity at the state level
    # Filter for Total population, latest year
    df_corr = df[(df['Year'] == latest_year) & (df['StratificationCategory1'] == 'Total')]
    
    # Pivot to get columns for Obesity and Physical Activity
    # We need to aggregate because there might be multiple questions per class
    # Let's pick specific questions to correlate
    
    q_obesity = 'Percent of adults aged 18 years and older who have obesity'
    q_activity = 'Percent of adults who engage in no leisure-time physical activity'
    
    df_obesity = df_corr[df_corr['Question'] == q_obesity][['LocationAbbr', 'Data_Value']].rename(columns={'Data_Value': 'Obesity_Rate'})
    df_activity = df_corr[df_corr['Question'] == q_activity][['LocationAbbr', 'Data_Value']].rename(columns={'Data_Value': 'Inactivity_Rate'})
    
    merged = pd.merge(df_obesity, df_activity, on='LocationAbbr')
    
    correlation = merged['Obesity_Rate'].corr(merged['Inactivity_Rate'])
    print(f"Correlation between Obesity and Physical Inactivity: {correlation:.2f}")
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=merged, x='Inactivity_Rate', y='Obesity_Rate')
    sns.regplot(data=merged, x='Inactivity_Rate', y='Obesity_Rate', scatter=False, color='red')
    plt.title(f'Obesity vs. Physical Inactivity by State ({latest_year})\nCorrelation: {correlation:.2f}')
    plt.xlabel('Physical Inactivity Rate (%)')
    plt.ylabel('Obesity Rate (%)')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_obesity_inactivity.png")
    plt.close()
    
    print("Analysis complete. Visualizations saved to output directory.")

if __name__ == "__main__":
    input_csv = 'cleaned_data.csv'
    output_directory = 'output'
    analyze_data(input_csv, output_directory)
