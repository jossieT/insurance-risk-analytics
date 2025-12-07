# ACIS Insurance Risk Analytics

## Project Overview
This project focuses on analyzing insurance claim data to optimize risk assessment and marketing strategies. By leveraging machine learning and data analysis techniques, we aim to:
- Identify low-risk targets for premium discounts.
- Understand the distribution of risk across various provinces and vehicle types.
- Prepare data for predictive modeling.

## Setup Instructions
To set up the project environment:

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd ACIS-Insurance-Risk-Analytics
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Ensure you have Python 3.8+ installed.*
3.  **Data Placement**:
    Ensure `MachineLearningRating_v3.txt` is located in the `data/` directory.

## Task 1: Data Understanding & EDA
**Notebook**: `notebooks/data_exploration_and_eda.ipynb`

This phase involves Exploratory Data Analysis (EDA) to understand the dataset's structure and quality. Key activities include:
- **Data Loading & Inspection**: Checking data types and shapes.
- **Missing Value Analysis**: Identifying and visualizing gaps in data.
- **Descriptive Statistics**: Summarizing key metrics like TotalPremium and TotalClaims.
- **Visualizations**:
    - Monthly trends of premiums vs. claims.
    - Loss Ratio heatmaps by Province.
    - Claims distribution by Vehicle Make.

## Task 2: Data Preparation & Versioning
**Notebook**: `notebooks/data_preparation_and_versioning.ipynb`

This phase prepares the data for machine learning models. Key steps include:
- **Feature Engineering**: Creating new features such as:
    - `LossRatio`: TotalClaims / TotalPremium
    - `ClaimSeverity`: TotalClaims / NumberOfClaims
    - `VehicleAge`: Calculated from RegistrationYear
- **Data Cleaning**: Imputing missing values (Median/Mode) and handling outliers.
- **Encoding**: Converting categorical variables (Make, Province, etc.) into numeric formats.
- **Scaling**: Standardizing numeric features for model compatibility.

## How to Run DVC
Data Version Control (DVC) is used to track dataset versions.

1.  **Initialize DVC** (if not already done):
    ```bash
    dvc init
    ```
2.  **Add Data**. After running Task 2, version the processed data:
    ```bash
    dvc add data/processed/cleaned_data.csv
    ```
3.  **Commit DVC File**:
    ```bash
    git add data/processed/cleaned_data.csv.dvc .gitignore
    git commit -m "Update processed data"
    ```
4.  **Push Data** (requires remote storage configuration):
    ```bash
    dvc push
    ```
