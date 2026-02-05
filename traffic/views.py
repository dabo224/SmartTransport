import os
import joblib
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Load the model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_module', 'traffic_model.joblib')
model = None

def load_traffic_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            try:
                model = joblib.load(MODEL_PATH)
            except Exception as e:
                print(f"Error loading model: {e}")
                # Fallback hack for specific scikitlearn error if needed
                import sys
                import sklearn
                sys.modules['sklearn'] = sklearn
                try:
                    model = joblib.load(MODEL_PATH)
                except Exception as e2:
                    print(f"Second attempt failed: {e2}")
                    model = None
        else:
            print(f"Model not found at {MODEL_PATH}")
    return model

@login_required
def predict_traffic(request):
    prediction = None
    input_data = {
        'hour': 12,
        'day_of_week': 'Monday',
        'road_type': 'Urban',
        'weather': 'Sunny',
        'avg_speed': 40.0
    }
    
    if request.method == 'POST':
        try:
            hour = int(request.POST.get('hour', 12))
            day_of_week = request.POST.get('day_of_week', 'Monday')
            road_type = request.POST.get('road_type', 'Urban')
            weather = request.POST.get('weather', 'Sunny')
            avg_speed = float(request.POST.get('avg_speed', 40.0))
            
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
        except Exception as e:
            print(f"Prediction error: {e}")

    context = {
        'prediction': prediction,
        'input_data': input_data,
        'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'roads': ['Urban', 'Highway', 'Residential'],
        'weathers': ['Sunny', 'Rainy', 'Cloudy', 'Foggy']
    }
    return render(request, 'traffic/dashboard.html', context)
