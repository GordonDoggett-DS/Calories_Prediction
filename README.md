# Calories_Prediction

The files in here are the files that were used to create a data science project that preidtcs the number of calories burned using XGBoost library in Python and produce the results to a CSV file that is then consumed by a PowerBI report, below are the full steps to recreate the project. I am always happy to listen to feedback and recommendations or provide support to people learning data science so feel free to drop me a message or download and user the files for your development.

## Reseach Question

How does the different features of a physical gym workout and person affect the predicted number of calories that can be burned, what use cases does the data science model offer to provide improved personalised workout plans.

## Summary

The project aim was to understand the features that affect the target variable (calories burned) which then allows for a data science model to be created with over 90% accuracy that will predict the number of calories that will be burnt using the features of the dataset. This will allow for creation of gym workout plans customised for individual users based on their personal physique such as age, gender, height and weight. 

The model used was XGBoost utilising python for the coding element and then presenting the results in PowerBI for deeper trend analysis and visualisations for the end user. The model producedes an R2 score of 99.7% which is very high and an MAE of 2.44 which means the predictions are this number away from the actual result on average across the dataset.

A hypothesis before the project commenced was that males will burn a significantly higher number of calories during their workouts than females, this was based on the prior knowledge of the fitness industry, the results disprove this hypothesis as shown in Fig1.


