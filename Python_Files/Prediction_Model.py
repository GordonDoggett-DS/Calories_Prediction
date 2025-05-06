# Importing the required libraries
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

from Load_Public_Dataset import load_and_prepare_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Define the save location for the final csv file
network_drive = r"C:\Users\GordonDoggett\Downloads\BPP\Data Science Professional Practice\Assignments"

# Load the dataset
calories_df_bmi = load_and_prepare_dataset()
print("Loading and EDA on Dataset")

# Split the features and outcome variable into separate dataframes
print("Original Model (with Duration):")
X = calories_df_bmi.drop(['Calories'], axis=1)
y = calories_df_bmi['Calories']
print("Splitting the dataset into features and outcome variables")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Splitting the data into training and testing sets")

# Print the Shape of the training and testing sets
print(f"The shape of the feature training set is: {X_train.shape}")
print(f"The shape of the feature testing set is: {X_test.shape}")

# Print the Shape of the outcome variable
print(f"The shape of the outcome variable testing set is: {y_train.shape}")
print(f"The shape of the outcome variable training set is: {y_test.shape}")

# Train the model
xgb_model = xgb.XGBRegressor(random_state=42)
xgb_model.fit(X_train, y_train)

# Create a prediction for the testing set
y_pred = xgb_model.predict(X_test)

# Print the accuracy of the model
print(f"The accuracy of the model is: {xgb_model.score(X_test, y_test)}")
print(f'The mean absolute error of the model is: {mean_absolute_error(y_test, y_pred)}')
print(f'The R2 score of the model is: {r2_score(y_test, y_pred)}')

# create a scatter plot to show the actual and predicted values
plt.figure(figsize=(10,6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
sns.lineplot(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], color='red')
plt.title('Actual vs Predicted Calories Burned')
plt.xlabel('Actual Calories Burned')
plt.ylabel('Predicted Calories Burned')
plt.show()

# Now lets looks at the importance of the features
importance = xgb_model.feature_importances_
feature_names = X.columns
feature_importance = list(zip(feature_names, importance))
sorted_importance = sorted(feature_importance, key=lambda x: x[1], reverse=True)

# Loop through the feature importance and print the name and importance score
print("\nFeature Importance:")
for name, score in sorted_importance:
    print(f"{name}: {score:.4f}")

# Visualize Feature Importance
plt.figure(figsize=(10, 6))
plt.bar([x[0] for x in sorted_importance], [x[1] for x in sorted_importance])
plt.xticks(rotation=90)
plt.xlabel("Features")
plt.ylabel("Importance Score")
plt.title("XGBoost Feature Importance")
plt.tight_layout()
plt.show()

# Model without Duration
print("\nModel without Duration:")
X_no_duration = calories_df_bmi.drop(['Calories', 'Duration'], axis=1)
y = calories_df_bmi['Calories']

# Split the data into training and testing sets
X_train_nd, X_test_nd, y_train_nd, y_test_nd = train_test_split(X_no_duration, y, test_size=0.2, random_state=42)

# Train the model
xgb_model_nd = xgb.XGBRegressor(random_state=42)
xgb_model_nd.fit(X_train_nd, y_train_nd)

# Create a prediction for the testing set
y_pred_nd = xgb_model_nd.predict(X_test_nd)

# Print the accuracy of the model
print(f"The accuracy of the model is: {xgb_model_nd.score(X_test_nd, y_test_nd)}")
print(f'The mean absolute error of the model is: {mean_absolute_error(y_test_nd, y_pred_nd)}')
print(f'The R2 score of the model is: {r2_score(y_test_nd, y_pred_nd)}')

# create a scatter plot to show the actual and predicted values
plt.figure(figsize=(10,6))
sns.scatterplot(x=y_test_nd, y=y_pred_nd, alpha=0.6)
sns.lineplot(x=[y_test_nd.min(), y_test_nd.max()], y=[y_test_nd.min(), y_test_nd.max()], color='red')
plt.title('Actual vs Predicted Calories Burned (Without Duration)')
plt.xlabel('Actual Calories Burned')
plt.ylabel('Predicted Calories Burned')
plt.show()

# Now lets looks at the importance of the features wihtout duration
importance_nd = xgb_model_nd.feature_importances_
feature_names_nd = X_no_duration.columns
feature_importance_nd = list(zip(feature_names_nd, importance_nd))
sorted_importance_nd = sorted(feature_importance_nd, key=lambda x: x[1], reverse=True)

print("\nFeature Importance (Without Duration):")
for name, score in sorted_importance_nd:
    print(f"{name}: {score:.4f}")

plt.figure(figsize=(10, 6))
plt.bar([x[0] for x in sorted_importance_nd], [x[1] for x in sorted_importance_nd])
plt.xticks(rotation=90)
plt.xlabel("Features")
plt.ylabel("Importance Score")
plt.title("XGBoost Feature Importance (Without Duration)")
plt.tight_layout()
plt.show()

# Now show the differences of the 2 models so we can compare in numbers
metrics_df = pd.DataFrame({
    'Metric': ['Accuracy', 'MAE', 'R2 Score'],
    'With Duration': [xgb_model.score(X_test, y_test), mean_absolute_error(y_test, y_pred), r2_score(y_test, y_pred)],
    'Without Duration': [xgb_model_nd.score(X_test_nd, y_test_nd), mean_absolute_error(y_test_nd, y_pred_nd), r2_score(y_test_nd, y_pred_nd)],
    'Difference': [
        xgb_model.score(X_test, y_test) - xgb_model_nd.score(X_test_nd, y_test_nd),
        mean_absolute_error(y_test, y_pred) - mean_absolute_error(y_test_nd, y_pred_nd),
        r2_score(y_test, y_pred) - r2_score(y_test_nd, y_pred_nd)
    ]
})
print("\nComparison of Model Performance:")
print(metrics_df)

# Change Gender column back to categorical values
calories_df_bmi['Gender'] = calories_df_bmi['Gender'].replace({0: 'Female', 1: 'Male'})
print("Converted Gender Column back to categorical")

# Create a DataFrame with the predicted values and features
final_output = calories_df_bmi[['Age', 'Gender', 'Duration', 'Heart_Rate', 'Body_Temp', 'BMI', 'Calories']]
final_output['Predicted_Calories'] = xgb_model.predict(X)
print("Final output DataFrame created")

# Save the final DataFrame to a csv file
csv_path = os.path.join(network_drive, "Calories Prediction.csv")
final_output.to_csv(csv_path, index=False)

print(f"\nFinal output saved to: {csv_path}")