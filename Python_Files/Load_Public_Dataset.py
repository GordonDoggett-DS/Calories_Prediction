# Importing the required libraries
import kaggle
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

def load_and_prepare_dataset():

    # setting the path to save the data and make the directory if it doesn't exist
    save_path = r"C:\Users\GordonDoggett\Downloads\BPP\Data Science Professional Practice\Assignments"
    os.makedirs(save_path, exist_ok=True)

    # Authenticate with Kaggle and download the dataset
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('ruchikakumbhar/calories-burnt-prediction', path=save_path, unzip=True)

    # Load the dataset into a pandas DataFrame
    calories_df = pd.read_csv(os.path.join(save_path, 'calories.csv'))

    # Display the first few rows and get information about the dataset
    print(calories_df.head())
    print(calories_df.info())

    # Perform EDA on the dataset
    # Print the basic information about the dataset
    print("Basic Information:")
    print(calories_df.describe())

    # Print a list of distinct values for the Gender column
    print("Gender Values:")
    print(calories_df['Gender'].unique())

    # Change the Gender column to a numerical value
    calories_df['Gender'] = calories_df['Gender'].replace({'female': 0, 'male': 1})
    print("Converted Gender Column to Numerical")

    # Check for any missing values
    print("Nulls per Column Count:")
    print(calories_df.isnull().sum())

    # Check for any full line duplicates
    print(f"Full Line Duplicate Count: {calories_df.duplicated().sum()}")

    # Remove the User_ID Column, this is personal identifiable data under GDPR and not required for the model
    calories_df.drop('User_ID', axis=1, inplace=True)
    print("Removed User_ID Column")

    # Create a histogram for all numeric variable to see the distribution of the data
    calories_df.hist(figsize=(15, 10))
    plt.tight_layout()
    plt.show()
    print("Histogram for all numeric variables")

    # Create a box plot for all numeric variable to check for any outliers
    calories_df.boxplot(figsize=(15, 10))
    plt.tight_layout()
    plt.show()
    print("Box Plot for all numeric variables")

    # There are outliers in weight and height, with a few in calories but no extreme values so all data will remain in the dataframe

   # Create a bar chart to see the average calories burned by gender
    plt.figure(figsize=(10, 6))
    avg_calories = calories_df.groupby('Gender')['Calories'].mean()
    sns.barplot(x=avg_calories.index, y=avg_calories.values, palette=['#ff6b6b', '#4d94ff'])
    plt.title('Average Calories Burned by Gender', fontsize=14)
    plt.xlabel('Gender', labelpad=12)
    plt.ylabel('Average Calories Burned', labelpad=12)
    plt.xticks(ticks=[0, 1], labels=['Female (0)', 'Male (1)'])
    plt.grid(axis='y', alpha=0.3)
    sns.despine()

    # Add text labels on top of each bar
    for i, v in enumerate(avg_calories):
        plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')

    plt.show()
    print("Average calories burned by gender bar chart generated\n")

    # Print the correlation between the variables to see if any input variables are correlated
    corr = calories_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.show()
    print("Correlation Matrix for the dataset")

    # Create a copy of the dataset to combine weight and height due to the correlation between the two and calculate the BMI
    calories_df_bmi = calories_df.copy()
    calories_df_bmi['Weight'] = calories_df_bmi['Weight'].astype(float)
    calories_df_bmi['Height'] = calories_df_bmi['Height'].astype(float)
    calories_df_bmi['Height_m'] = calories_df_bmi['Height'] / 100
    calories_df_bmi['BMI'] = calories_df_bmi['Weight'] / (calories_df_bmi['Height_m'] ** 2)
    print("Copy of the dataset with BMI calculated")

    # Drop the Weight and Height columns
    calories_df_bmi.drop(['Weight', 'Height', 'Height_m'], axis=1, inplace=True)
    print("Dropped Weight and Height columns")

    # Print the correlation for the new dataset
    corr = calories_df_bmi.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.show()
    print("Correlation Matrix for the new dataset")

    #Return the dataset for the model to use
    return calories_df_bmi
