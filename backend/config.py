import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MODEL_PATH = 'models/trained_models/crop_yield_model.pkl'
    ENCODER_PATH = 'models/trained_models/label_encoder.pkl'
    DATA_PATH = 'data/processed/clean_crop_data.csv'
    
    # API Configuration
    API_HOST = '127.0.0.1'
    API_PORT = 5000
    DEBUG = True
    
    # Model Configuration
    SUPPORTED_CROPS = ['wheat', 'rice', 'corn', 'barley', 'soybean', 'potato', 'tomato']
    MAX_AREA = 1000  # hectares
    MIN_AREA = 0.1
    
    # Feature ranges for validation
    FEATURE_RANGES = {
        'temperature': {'min': -10, 'max': 50},  # Celsius
        'rainfall': {'min': 0, 'max': 3000},     # mm
        'humidity': {'min': 0, 'max': 100},      # %
        'soil_ph': {'min': 3.0, 'max': 10.0},
        'fertilizer': {'min': 0, 'max': 500},    # kg/hectare
        'area': {'min': 0.1, 'max': 1000}       # hectares
    }
