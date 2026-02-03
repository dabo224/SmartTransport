import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_traffic_data(num_records=1000):
    data = []
    start_date = datetime(2025, 1, 1)
    
    road_types = ['Urban', 'Highway', 'Residential']
    weather_conditions = ['Sunny', 'Rainy', 'Cloudy', 'Foggy']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for i in range(num_records):
        date = start_date + timedelta(hours=i)
        hour = date.hour
        day_of_week = days[date.weekday()]
        road_type = random.choice(road_types)
        weather = random.choice(weather_conditions)
        
        # Logic to simulate traffic level based on hour and day
        # Peak hours: 7-9 AM and 4-7 PM on weekdays
        is_peak = False
        if 7 <= hour <= 9 or 16 <= hour <= 19:
            if date.weekday() < 5: # Monday to Friday
                is_peak = True
        
        # Base speed based on road type
        if road_type == 'Highway':
            base_speed = 100
        elif road_type == 'Urban':
            base_speed = 50
        else:
            base_speed = 30
            
        # Adjust speed based on peak and weather
        traffic_factor = 1.0
        if is_peak:
            traffic_factor -= random.uniform(0.4, 0.7)
        if weather in ['Rainy', 'Foggy']:
            traffic_factor -= random.uniform(0.1, 0.3)
            
        avg_speed = max(5, base_speed * traffic_factor + random.uniform(-5, 5))
        
        # Traffic level labeling
        # 0: Low, 1: Medium, 2: High
        if is_peak or avg_speed < base_speed * 0.4:
            traffic_level = 2 # High
        elif avg_speed < base_speed * 0.7:
            traffic_level = 1 # Medium
        else:
            traffic_level = 0 # Low
            
        data.append([
            date,
            hour,
            day_of_week,
            road_type,
            weather,
            round(avg_speed, 2),
            traffic_level
        ])
        
    columns = ['timestamp', 'hour', 'day_of_week', 'road_type', 'weather_condition', 'avg_speed', 'traffic_level']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('ml_module/traffic_data.csv', index=False)
    print(f"Generated {num_records} records of traffic data in 'ml_module/traffic_data.csv'")

if __name__ == "__main__":
    generate_traffic_data(5000)
