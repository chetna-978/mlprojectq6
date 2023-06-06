import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import pymongo
from dataclasses import dataclass
import os
from flask import Flask, request, jsonify

@dataclass
class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
# Load the dataset
def get_collection_as_dataframe(database_name: str, collection_name: str) -> pd.DataFrame:
    data = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
    if "_id" in data.columns:
        data = data.drop("_id", axis=1)
    return data

# Call the function to load the dataset
data = get_collection_as_dataframe('loan_prediction', 'loan_predict')

# Handling NaN values
data.fillna(value=0, inplace=True)  # Replace NaN with 0 or specify another appropriate value

# Preprocessing the dataset
X = data.drop('Loan_Status', axis=1)
y = data['Loan_Status']
X_encoded = pd.get_dummies(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train the Gradient Boosting Classifier model
model = GradientBoostingClassifier()
model.fit(X_train, y_train)

# Predict loan eligibility for the test set
y_pred = model.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


