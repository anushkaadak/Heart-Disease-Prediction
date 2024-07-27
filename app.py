from flask import Flask, request, jsonify, render_template
import requests


app = Flask(__name__)

# NOTE: set your API key and endpoint here
API_KEY = "NDx2QZgY-UWp4wFuIBkgR6ZWknNPt3unj74agAfKb7mA"
DEPLOYMENT_URL = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/cf84092e-f44f-414d-9a7c-f1c4cca821e8/predictions?version=2021-05-01"

# Get the authentication token
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
    "apikey": API_KEY,
    "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
})
mltoken = token_response.json()["access_token"]

header = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + mltoken
}

@app.route('/')
def home():
    return render_template('index.html')


def index():
    data = {
        'title': 'Hello, World!',
        'message': 'This data is sent from the Flask app to the HTML template.'
    }
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Extract the form data
    Age = int(data['Age'])
    Sex = data['Sex']
    ChestPainType = (data['ChestPainType'])
    RestingBP = int(data['RestingBP'])
    Cholesterol = int(data['Cholesterol'])
    FastingBS = bool(data['FastingBS'])
    RestingECG = (data['RestingECG'])
    MaxHR = int(data['MaxHR'])
    ExerciseAngina = data['ExerciseAngina']
    Oldpeak = float(data['Oldpeak'])
    ST_Slope = data['ST_Slope']
    
    # Prepare the payload for scoring
    payload_scoring = {
        "input_data": [{
            "fields": ["Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol", "FastingBS", "RestingECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"],
            "values": [[Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope]]
        }]
    }
    
    # print("Receving response")
    response_scoring = requests.post(DEPLOYMENT_URL, json=payload_scoring, headers=header)
    result = response_scoring.json()
    
    # print(result)
    # Get the prediction result
    prediction = result['predictions'][0]['values'][0][1][0]
    
    if prediction == 0:
        message = "You have no such risk of heart disease!"
    else:
        message = "You have a risk of Heart disease :("
    # print(message)
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True)