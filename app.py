import json
import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import mlflow

app = Flask(__name__)

# Load the model
regmodel = pickle.load(open('claim_prediction_model.pkl', 'rb'))

# List of expected features
expected_features = [
    'InscClaimAmtReimbursed', 'IPAnnualReimbursementAmt', 'OPAnnualReimbursementAmt',
    'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary', 'Race_2', 'Race_3', 'Race_5',
    'Gender_2', 'ChronicCond_Alzheimer', 'ChronicCond_KidneyDisease', 'ChronicCond_Heartfailure'
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data and convert it to the proper format
    data = [float(x) for x in request.form.values()]
    final_input = np.array(data).reshape(1, -1)
    print(final_input)
    
    # Make prediction
    output = regmodel.predict(final_input)[0]
    
    # Log the input and prediction using MLflow
    with mlflow.start_run():
        mlflow.log_param("input_data", data)
        mlflow.log_metric("predicted_claim_amount", output)
    
    # Render the home template with the prediction
    return render_template("home.html", prediction_text=f"The predicted claim amount is ${output:,.2f}")

if __name__ == "__main__":
    app.run(debug=True)
# if __name__ == "__main__":
#     app.run(port=5002)  # Change 5002 to any other port that is available
