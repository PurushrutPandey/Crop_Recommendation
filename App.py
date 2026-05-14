import joblib
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Map crop names to image files in static/crops/
CROP_IMAGES = {
    'rice': 'rice.jpg',
    'maize': 'maize.jpg',
    'chickpea': 'chickpea.jpg',
    'kidneybeans': 'kidneybeans.jpg',
    'pigeonpeas': 'pigeonpeas.jpg',
    'mothbeans': 'mothbeans.jpg',
    'mungbean': 'mungbean.jpg',
    'blackgram': 'blackgram.jpg',
    'lentil': 'lentil.jpg',
    'pomegranate': 'pomegranate.png',
    'banana': 'banana.jpg',
    'mango': 'mango.png',
    'grapes': 'grapes.png',
    'watermelon': 'watermelon.png',
    'muskmelon': 'muskmelon.png',
    'apple': 'apple.png',
    'orange': 'orange.png',
    'papaya': 'papaya.png',
    'coconut': 'coconut.png',
    'cotton': 'cotton.png',
    'jute': 'jute.png',
    'coffee': 'coffee.png'
}

@app.route('/')
def home():
    return render_template('Home_1.html')

@app.route('/Predict', methods=["GET"])
@app.route('/predict', methods=["GET"])
def prediction():
    return render_template('Index.html')

import pandas as pd

@app.route('/form', methods=["GET", "POST"])
def brain():
    if request.method == 'GET':
        return redirect('/Predict')
    try:
        Nitrogen = request.form.get('Nitrogen', '')
        Phosphorus = request.form.get('Phosphorus', '')
        Potassium = request.form.get('Potassium', '')
        Temperature = request.form.get('Temperature', '')
        Humidity = request.form.get('Humidity', '')
        Ph = request.form.get('ph', '')
        Rainfall = request.form.get('Rainfall', '')

        print(f"Nitrogen: {Nitrogen}, Phosphorus: {Phosphorus}, Potassium: {Potassium}, "
              f"Temperature: {Temperature}, Humidity: {Humidity}, Ph: {Ph}, Rainfall: {Rainfall}")

        if not Nitrogen or not Phosphorus or not Potassium or not Temperature or not Humidity or not Ph or not Rainfall:
            return "All fields must be filled out. Please check the 'Phosphorus' field and others."

        try:
            Nitrogen = float(Nitrogen)
            Phosphorus = float(Phosphorus)
            Potassium = float(Potassium)
            Temperature = float(Temperature)
            Humidity = float(Humidity)
            Ph = float(Ph)
            Rainfall = float(Rainfall)
        except ValueError as e:
            return f"Invalid input. Please enter numeric values only. Error: {e}"

        if not (0 < Ph < 14 and 10 < Temperature < 60 and 0 < Humidity <= 100 and 0 <= Nitrogen <= 100 and 0 <= Phosphorus <= 100 and 0 <= Potassium <= 100 and 0 <= Rainfall):
            return "Invalid input values. Please ensure all fields are filled correctly."

        model = joblib.load("Project_1")
        scaler = joblib.load("scaler")

        input_data = pd.DataFrame([[Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]],
                                  columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

        # Scale the input data before prediction
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]

        # Normalize prediction name and select matching image
        normalized_prediction = str(prediction).strip().lower().replace(' ', '')
        crop_image = CROP_IMAGES.get(normalized_prediction, None)

        return render_template('Prediction.html', prediction=prediction, crop_image=crop_image)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__=='__main__':
    app.run(debug=True)
                                 
