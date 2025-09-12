import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os

class CropYieldPredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_names = ['crop_type_encoded', 'temperature', 'rainfall', 
                             'humidity', 'soil_ph', 'fertilizer', 'area']
        self.crop_types = ['wheat', 'rice', 'corn', 'barley', 'soybean', 'potato', 'tomato']
        
        # Get the backend directory path (parent of models folder)
        self.backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def load_model(self, model_path=None, encoder_path=None):
        """Load the trained model and label encoder"""
        if model_path is None:
            model_path = os.path.join(self.backend_dir, 'models', 'trained_models', 'crop_yield_model.pkl')
        if encoder_path is None:
            encoder_path = os.path.join(self.backend_dir, 'models', 'trained_models', 'label_encoder.pkl')
            
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            print("Model loaded successfully!")
            return True
        except FileNotFoundError as e:
            print(f"Model files not found: {e}")
            print("Please train the model first by running train_model()")
            return False
    
    def train_model(self, data_path=None):
        """Train a new model"""
        print("Training new model...")
        
        if data_path is None:
            data_path = os.path.join(self.backend_dir, 'data', 'processed', 'clean_crop_data.csv')
        
        # Load data
        if not os.path.exists(data_path):
            print(f"Data file not found: {data_path}")
            print("Please run data/sample_data.py first to generate training data")
            return False
        
        df = pd.read_csv(data_path)
        print(f"Loaded dataset with {len(df)} samples")
        
        # Encode categorical variables
        self.label_encoder = LabelEncoder()
        df['crop_type_encoded'] = self.label_encoder.fit_transform(df['crop_type'])
        
        # Prepare features and target
        X = df[self.feature_names]
        y = df['yield']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=df['crop_type']
        )
        
        # Train model
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"\nModel Performance:")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R² Score: {r2:.3f}")
        print(f"Average Prediction Error: {np.sqrt(mse):.2f} tons")
        
        # Save model
        model_dir = os.path.join(self.backend_dir, 'models', 'trained_models')
        os.makedirs(model_dir, exist_ok=True)
        
        model_path = os.path.join(model_dir, 'crop_yield_model.pkl')
        encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        print("Model saved successfully!")
        return True
    
    def predict_yield(self, crop_type, temperature, rainfall, humidity, 
                     soil_ph, fertilizer, area):
        """Make a yield prediction"""
        if not self.model or not self.label_encoder:
            print("Model not loaded. Loading model...")
            if not self.load_model():
                print("Failed to load model. Training new model...")
                if not self.train_model():
                    raise ValueError("Failed to train model")
        
        # Validate inputs
        if crop_type.lower() not in [c.lower() for c in self.crop_types]:
            print(f"Warning: Unknown crop type '{crop_type}'. Using 'wheat' as default.")
            crop_type = 'wheat'
        
        # Encode crop type
        try:
            crop_encoded = self.label_encoder.transform([crop_type.lower()])[0]
        except ValueError:
            # Handle unknown crop types
            crop_encoded = self.label_encoder.transform(['wheat'])[0]
        
        # Prepare features
        features = np.array([[crop_encoded, temperature, rainfall, humidity, 
                            soil_ph, fertilizer, area]])
        
        # Make prediction
        prediction = self.model.predict(features)[0]
        
        # Ensure positive yield
        prediction = max(0, prediction)
        
        # Calculate yield per hectare for reference
        yield_per_hectare = prediction / area if area > 0 else 0
        
        return {
            'total_yield': round(prediction, 2),
            'yield_per_hectare': round(yield_per_hectare, 2),
            'crop_type': crop_type,
            'area': area
        }
    
    def get_feature_importance(self):
        """Get which factors most affect yield"""
        if not self.model or not hasattr(self.model, 'coef_'):
            return None
            
        feature_names_readable = ['Crop Type', 'Temperature', 'Rainfall', 
                                 'Humidity', 'Soil pH', 'Fertilizer', 'Area']
        importance = dict(zip(feature_names_readable, self.model.coef_))
        
        # Sort by absolute importance
        importance_sorted = dict(sorted(importance.items(), 
                                      key=lambda x: abs(x[1]), reverse=True))
        return importance_sorted

# Test the model
if __name__ == "__main__":
    predictor = CropYieldPredictor()
    
    # Train model if needed
    if not predictor.load_model():
        predictor.train_model()
    
    # Test prediction
    result = predictor.predict_yield(
        crop_type='wheat',
        temperature=20,
        rainfall=500,
        humidity=60,
        soil_ph=6.5,
        fertilizer=100,
        area=10
    )
    
    print(f"\nTest Prediction:")
    print(f"Crop: {result['crop_type']}")
    print(f"Area: {result['area']} hectares")
    print(f"Total Yield: {result['total_yield']} tons")
    print(f"Yield per Hectare: {result['yield_per_hectare']} tons/hectare")
