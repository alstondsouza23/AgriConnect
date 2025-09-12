from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from models.crop_model import CropYieldPredictor
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize the predictor
predictor = CropYieldPredictor()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple HTML template for testing the API
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Crop Yield Predictor API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin: 10px 0; }
        label { display: inline-block; width: 120px; }
        input, select { padding: 5px; width: 200px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Crop Yield Predictor API Test</h1>
    
    <form id="cropForm">
        <div class="form-group">
            <label>Crop Type:</label>
            <select name="crop_type" required>
                <option value="wheat">Wheat</option>
                <option value="rice">Rice</option>
                <option value="corn">Corn</option>
                <option value="barley">Barley</option>
                <option value="soybean">Soybean</option>
                <option value="potato">Potato</option>
                <option value="tomato">Tomato</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>Temperature (°C):</label>
            <input type="number" name="temperature" step="0.1" value="20" required>
        </div>
        
        <div class="form-group">
            <label>Rainfall (mm):</label>
            <input type="number" name="rainfall" step="0.1" value="500" required>
        </div>
        
        <div class="form-group">
            <label>Humidity (%):</label>
            <input type="number" name="humidity" step="0.1" value="60" min="0" max="100" required>
        </div>
        
        <div class="form-group">
            <label>Soil pH:</label>
            <input type="number" name="soil_ph" step="0.1" value="6.5" min="3" max="10" required>
        </div>
        
        <div class="form-group">
            <label>Fertilizer (kg/ha):</label>
            <input type="number" name="fertilizer" step="0.1" value="100" min="0" required>
        </div>
        
        <div class="form-group">
            <label>Area (hectares):</label>
            <input type="number" name="area" step="0.1" value="10" min="0.1" required>
        </div>
        
        <button type="submit">Predict Yield</button>
    </form>
    
    <div id="result" class="result" style="display: none;"></div>
    
    <script>
        document.getElementById('cropForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            
            // Convert numeric fields
            ['temperature', 'rainfall', 'humidity', 'soil_ph', 'fertilizer', 'area'].forEach(field => {
                data[field] = parseFloat(data[field]);
            });
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById('result').innerHTML = `
                        <h3>Prediction Result:</h3>
                        <p><strong>Crop:</strong> ${result.crop_type}</p>
                        <p><strong>Area:</strong> ${result.area} hectares</p>
                        <p><strong>Total Yield:</strong> ${result.total_yield} tons</p>
                        <p><strong>Yield per Hectare:</strong> ${result.yield_per_hectare} tons/hectare</p>
                    `;
                } else {
                    document.getElementById('result').innerHTML = `
                        <h3>Error:</h3>
                        <p>${result.error}</p>
                    `;
                }
                
                document.getElementById('result').style.display = 'block';
            } catch (error) {
                document.getElementById('result').innerHTML = `
                    <h3>Error:</h3>
                    <p>Failed to connect to server: ${error.message}</p>
                `;
                document.getElementById('result').style.display = 'block';
            }
        });
    </script>
</body>
</html>
'''

def validate_input_data(data):
    """Validate input data against configured ranges"""
    errors = []
    
    # Check required fields
    required_fields = ['crop_type', 'temperature', 'rainfall', 'humidity', 'soil_ph', 'fertilizer', 'area']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return errors
    
    # Validate ranges
    ranges = app.config['FEATURE_RANGES']
    for field, limits in ranges.items():
        if field in data:
            value = data[field]
            if not isinstance(value, (int, float)):
                errors.append(f"{field} must be a number")
            elif value < limits['min'] or value > limits['max']:
                errors.append(f"{field} must be between {limits['min']} and {limits['max']}")
    
    # Validate crop type
    if data.get('crop_type', '').lower() not in [c.lower() for c in app.config['SUPPORTED_CROPS']]:
        errors.append(f"Supported crops: {', '.join(app.config['SUPPORTED_CROPS'])}")
    
    return errors

@app.route('/', methods=['GET'])
def home():
    """Serve a simple test page for the API"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict_yield():
    """Predict crop yield based on input parameters"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        logger.info(f"Received prediction request: {data}")
        
        # Validate input data
        validation_errors = validate_input_data(data)
        if validation_errors:
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
        # Make prediction
        result = predictor.predict_yield(
            crop_type=data['crop_type'],
            temperature=float(data['temperature']),
            rainfall=float(data['rainfall']),
            humidity=float(data['humidity']),
            soil_ph=float(data['soil_ph']),
            fertilizer=float(data['fertilizer']),
            area=float(data['area'])
        )
        
        logger.info(f"Prediction result: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the model"""
    try:
        importance = predictor.get_feature_importance()
        return jsonify({
            'supported_crops': app.config['SUPPORTED_CROPS'],
            'feature_ranges': app.config['FEATURE_RANGES'],
            'feature_importance': importance
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})

if __name__ == '__main__':
    # Load or train model on startup
    print("Starting Crop Yield Predictor API...")
    
    if not predictor.load_model():
        print("Model not found. Training new model...")
        if not predictor.train_model():
            print("Failed to train model. Exiting...")
            exit(1)
    
    print(f"API running at: http://{app.config['API_HOST']}:{app.config['API_PORT']}")
    print("Test the API by visiting the URL above in your browser")
    
    app.run(
        host=app.config['API_HOST'],
        port=app.config['API_PORT'],
        debug=app.config['DEBUG']
    )
