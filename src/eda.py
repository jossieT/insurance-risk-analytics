import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def summarize_numeric(df):
    """
    Summarizes numeric columns.
    """
    print("\n--- Numeric Summary ---")
    return df.describe()

def missing_value_report(df):
    """
    Returns a DataFrame of missing values.
    """
    missing = df.isnull().sum()
    percent = (df.isnull().sum() / len(df)) * 100
    report = pd.concat([missing, percent], axis=1, keys=['Total', 'Percent'])
    return report[report['Total'] > 0].sort_values('Total', ascending=False)

def plot_loss_ratio_by_group(df):
    """
    Plots Loss Ratio by group (Placeholder functionality as specific logic not fully defined in prompt, 
    but 'Creative Visualizations' section asks for specific plots).
    """
    pass

def top_creative_plots(df):
    """
    Generates and saves the 3 mandatory creative plots.
    """
    import os
    output_dir = '../outputs/eda'
    if not os.path.exists(output_dir):
        # Try relative to root if running from src? No, assuming running from notebooks/
        if not os.path.exists('outputs/eda'):
            os.makedirs('outputs/eda', exist_ok=True)
            output_dir = 'outputs/eda'
        else:
             output_dir = 'outputs/eda'
    
    # Ensure necessary columns exist or create them temporarily for plotting
    plot_df = df.copy()
    
    # 1. Monthly trend of claims vs premium
    # Assuming 'TransactionMonth' exists and is date-like or convertible
    if 'TransactionMonth' in plot_df.columns:
        try:
            plot_df['TransactionMonth'] = pd.to_datetime(plot_df['TransactionMonth'], errors='coerce')
            monthly_stats = plot_df.groupby(plot_df['TransactionMonth'].dt.to_period('M'))[['TotalPremium', 'TotalClaims']].sum()
            
            plt.figure(figsize=(12, 6))
            monthly_stats.plot(kind='line', marker='o')
            plt.title('Monthly Trend: Total Premium vs Total Claims')
            plt.xlabel('Month')
            plt.ylabel('Amount')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/monthly_trend.png')
            plt.close()
            print(f"Saved monthly_trend.png to {output_dir}")
        except Exception as e:
            print(f"Could not plot monthly trend: {e}")

    # 2. Loss Ratio by Province (heatmap)
    # Loss Ratio = TotalClaims / TotalPremium
    if 'Province' in plot_df.columns and 'TotalPremium' in plot_df.columns and 'TotalClaims' in plot_df.columns:
        try:
            province_stats = plot_df.groupby('Province')[['TotalPremium', 'TotalClaims']].sum()
            province_stats['LossRatio'] = province_stats['TotalClaims'] / province_stats['TotalPremium']
            
            plt.figure(figsize=(10, 8))
            sns.heatmap(province_stats[['LossRatio']].sort_values(by='LossRatio', ascending=False), annot=True, cmap='coolwarm', fmt='.4f')
            plt.title('Loss Ratio by Province')
            plt.tight_layout()
            plt.savefig(f'{output_dir}/loss_ratio_province.png')
            plt.close()
            print(f"Saved loss_ratio_province.png to {output_dir}")
        except Exception as e:
             print(f"Could not plot Loss Ratio by Province: {e}")

    # 3. Claims distribution by Vehicle Make
    if 'Make' in plot_df.columns and 'TotalClaims' in plot_df.columns:
        try:
            top_makes = plot_df['Make'].value_counts().nlargest(10).index
            make_data = plot_df[plot_df['Make'].isin(top_makes)]
            
            plt.figure(figsize=(12, 6))
            sns.boxplot(x='Make', y='TotalClaims', data=make_data)
            plt.title('Claims Distribution by Top 10 Vehicle Makes')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/claims_by_make.png')
            plt.close()
            print(f"Saved claims_by_make.png to {output_dir}")
        except Exception as e:
             print(f"Could not plot Claims by Make: {e}")

