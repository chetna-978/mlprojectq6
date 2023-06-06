import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import pymongo
import pickle
from dotenv import load_dotenv
from data_dump import DATABASE_NAME, COLLECTION_NAME

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
mongo_db_url = os.getenv("MONGO_DB_URL")
mongo_client = pymongo.MongoClient(mongo_db_url)

# Load the dataset from MongoDB
collection = mongo_client[DATABASE_NAME][COLLECTION_NAME]
data = pd.DataFrame(list(collection.find()))

# Handling NaN values
data.fillna(value=0, inplace=True)

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

# Save the trained model
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Save the encoder
with open('encoder.pkl', 'wb') as file:
    pickle.dump(X_encoded.columns, file)
