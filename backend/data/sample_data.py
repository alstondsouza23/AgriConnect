import pandas as pd
import numpy as np
import os

def generate_sample_data(n_samples=2000):
    """Generate realistic agricultural data for training"""
    
    np.random.seed(42)  # For reproducible results
    
    crops = ['wheat', 'rice', 'corn', 'barley', 'soybean', 'potato', 'tomato']
    
    # Crop-specific parameters (realistic agricultural data)
    crop_params = {
        'wheat': {'temp_opt': 20, 'temp_var': 4, 'rain_opt': 500, 'rain_var': 100, 'base_yield': 3.5},
        'rice': {'temp_opt': 28, 'temp_var': 3, 'rain_opt': 1200, 'rain_var': 200, 'base_yield': 4.2},
        'corn': {'temp_opt': 25, 'temp_var': 5, 'rain_opt': 800, 'rain_var': 150, 'base_yield': 9.5},
        'barley': {'temp_opt': 18, 'temp_var': 4, 'rain_opt': 400, 'rain_var': 80, 'base_yield': 3.0},
        'soybean': {'temp_opt': 24, 'temp_var': 4, 'rain_opt': 700, 'rain_var': 120, 'base_yield': 2.8},
        'potato': {'temp_opt': 17, 'temp_var': 3, 'rain_opt': 600, 'rain_var': 100, 'base_yield': 25.0},
        'tomato': {'temp_opt': 22, 'temp_var': 3, 'rain_opt': 600, 'rain_var': 100, 'base_yield': 50.0}
    }
    
    data = []
    
    for _ in range(n_samples):
        # Randomly select crop
        crop = np.random.choice(crops)
        params = crop_params[crop]
        
        # Generate environmental conditions based on crop preferences
        temperature = np.random.normal(params['temp_opt'], params['temp_var'])
        rainfall = np.random.normal(params['rain_opt'], params['rain_var'])
        humidity = np.random.normal(65, 10)
        soil_ph = np.random.normal(6.5, 0.8)
        fertilizer = np.random.exponential(80)  # Most farmers use moderate amounts
        area = np.random.exponential(5)  # Most farms are small to medium
        
        # Ensure realistic ranges
        temperature = np.clip(temperature, 5, 45)
        rainfall = np.clip(rainfall, 100, 2500)
        humidity = np.clip(humidity, 30, 95)
        soil_ph = np.clip(soil_ph, 4.0, 9.0)
        fertilizer = np.clip(fertilizer, 0, 400)
        area = np.clip(area, 0.5, 100)
        
        # Calculate yield with realistic relationships
        # Temperature factor (optimal curve)
        temp_factor = 1 - (abs(temperature - params['temp_opt']) / 20) ** 2
        temp_factor = np.clip(temp_factor, 0.1, 1)
        
        # Rainfall factor (diminishing returns)
        rain_factor = 1 - abs(rainfall - params['rain_opt']) / params['rain_opt']
        rain_factor = np.clip(rain_factor, 0.2, 1)
        
        # Soil pH factor (optimal around 6.5)
        ph_factor = 1 - abs(soil_ph - 6.5) * 0.15
        ph_factor = np.clip(ph_factor, 0.3, 1)
        
        # Humidity factor (moderate humidity is best)
        humidity_factor = 1 - abs(humidity - 60) * 0.008
        humidity_factor = np.clip(humidity_factor, 0.5, 1)
        
        # Fertilizer factor (diminishing returns after optimal point)
        fert_optimal = 120
        if fertilizer <= fert_optimal:
            fert_factor = 0.6 + 0.4 * (fertilizer / fert_optimal)
        else:
            fert_factor = 1 - (fertilizer - fert_optimal) * 0.001
        fert_factor = np.clip(fert_factor, 0.6, 1)
        
        # Calculate yield per hectare
        yield_per_hectare = (params['base_yield'] * temp_factor * rain_factor * 
                           ph_factor * humidity_factor * fert_factor * 
                           np.random.normal(1, 0.1))
        
        # Total yield = yield per hectare * area
        total_yield = yield_per_hectare * area
        total_yield = max(0, total_yield)  # Yield can't be negative
        
        data.append({
            'crop_type': crop,
            'temperature': round(temperature, 1),
            'rainfall': round(rainfall, 1),
            'humidity': round(humidity, 1),
            'soil_ph': round(soil_ph, 1),
            'fertilizer': round(fertilizer, 1),
            'area': round(area, 1),
            'yield': round(total_yield, 2)
        })
    
    return pd.DataFrame(data)

def save_sample_data():
    """Generate and save sample data"""
    print("Generating sample agricultural data...")
    
    # Generate data
    df = generate_sample_data(2000)
    
    # Create directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Save raw data
    raw_path = 'data/raw/crop_data.csv'
    df.to_csv(raw_path, index=False)
    print(f"Raw data saved to: {raw_path}")
    
    # Basic data cleaning
    df_clean = df.copy()
    
    # Remove outliers (beyond 3 standard deviations)
    for column in ['temperature', 'rainfall', 'humidity', 'fertilizer', 'yield']:
        mean = df_clean[column].mean()
        std = df_clean[column].std()
        df_clean = df_clean[
            (df_clean[column] >= mean - 3*std) & 
            (df_clean[column] <= mean + 3*std)
        ]
    
    # Save cleaned data
    clean_path = 'data/processed/clean_crop_data.csv'
    df_clean.to_csv(clean_path, index=False)
    print(f"Clean data saved to: {clean_path}")
    print(f"Dataset shape: {df_clean.shape}")
    
    # Print basic statistics
    print("\nDataset Statistics:")
    print(df_clean.groupby('crop_type')['yield'].agg(['count', 'mean', 'std']).round(2))
    
    return df_clean

if __name__ == "__main__":
    save_sample_data()
