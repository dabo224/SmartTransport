import os
import joblib
import pandas as pd
from django.shortcuts import render
from django.conf import settings

# Load the model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_module', 'traffic_model.joblib')
model = None

def load_traffic_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            print(f"Model not found at {MODEL_PATH}")
    return model

def predict_traffic(request):
    prediction = None
    input_data = None
    
    if request.method == 'POST':
        hour = int(request.POST.get('hour'))
        day_of_week = request.POST.get('day_of_week')
        road_type = request.POST.get('road_type')
        weather = request.POST.get('weather')
        avg_speed = float(request.POST.get('avg_speed'))
        
        input_df = pd.DataFrame([{
            'hour': hour,
            'day_of_week': day_of_week,
            'road_type': road_type,
            'weather_condition': weather,
            'avg_speed': avg_speed
        }])
        
        clf = load_traffic_model()
        if clf:
            prediction_idx = clf.predict(input_df)[0]
            levels = {0: 'Faible', 1: 'Moyen', 2: 'Elevé'}
            prediction = levels.get(prediction_idx, 'Inconnu')
            
            # Additional logic for recommended route (mock for now)
            recommendation = "Itinéraire principal conseillé."
            if prediction == 'Elevé':
                recommendation = "Attention : Trafic dense. Nous vous conseillons de prendre les voies secondaires."
            elif prediction == 'Moyen':
                recommendation = "Trafic modéré. Surveillez les mises à jour."
                
            input_data = {
                'hour': hour,
                'day_of_week': day_of_week,
                'road_type': road_type,
                'weather': weather,
                'avg_speed': avg_speed,
                'recommendation': recommendation
            }

    context = {
        'prediction': prediction,
        'input_data': input_data,
        'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'roads': ['Urban', 'Highway', 'Residential'],
        'weathers': ['Sunny', 'Rainy', 'Cloudy', 'Foggy']
    }
    return render(request, 'traffic/dashboard.html', context)
