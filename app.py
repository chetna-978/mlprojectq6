import os
import pandas as pd
import pickle
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define the paths to the model and encoder files
model_path = os.path.join('models', 'model.pkl')
encoder_path = os.path.join('models', 'encoder.pkl')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Load the trained model
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    # Load the loan features from the request
    data = request.form
    loan_features = pd.DataFrame(data, index=[0])

    # Load the encoder for one-hot encoding
    with open(encoder_path, 'rb') as file:
        encoder_columns = pickle.load(file)

    # Preprocess the loan features using the encoder
    loan_features_encoded = pd.get_dummies(loan_features)
    loan_features_encoded = loan_features_encoded.reindex(columns=encoder_columns, fill_value=0)

    # Predict the loan eligibility
    prediction = model.predict(loan_features_encoded)

    # Return the prediction as JSON response
    return render_template('index.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
