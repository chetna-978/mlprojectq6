from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import pickle

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Load the trained model
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Load the loan features from the request
    data = request.form
    loan_features = pd.DataFrame(data, index=[0])
    
    # Load the encoder for one-hot encoding
    with open('encoder.pkl', 'rb') as file:
        encoder = pickle.load(file)
    
    # Preprocess the loan features using the encoder
    loan_features_encoded = encoder.transform(loan_features)
    
    # Predict the loan eligibility
    prediction = model.predict(loan_features_encoded)
    
    # Return the prediction as JSON response
    return render_template('index.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
