import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './CropPredictorForm.css';

const CropPredictorForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    crop_type: '',
    planting_date: '',
    previous_yield: '',
    temperature: 25,
    rainfall: 500,
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const cropOptions = [
    { value: 'wheat', label: ' Wheat' },
    { value: 'rice', label: ' Rice' },
    { value: 'corn', label: ' Corn' },
    { value: 'barley', label: ' Barley' },
    { value: 'soybean', label: ' Soybean' },
    { value: 'potato', label: ' Potato' },
    { value: 'tomato', label: ' Tomato' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSliderChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      // Convert form data to match your backend API
      const apiData = {
        crop_type: formData.crop_type,
        temperature: formData.temperature,
        rainfall: formData.rainfall,
        humidity: 60, // Default value
        soil_ph: 6.5, // Default value
        fertilizer: 100, // Default value
        area: 10 // Default value
      };

      const response = await axios.post('http://127.0.0.1:5000/predict', apiData, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 10000
      });

      setPrediction(response.data);
    } catch (err) {
      if (err.code === 'ECONNABORTED') {
        setError('Request timed out. Please make sure the backend server is running.');
      } else if (err.response) {
        setError(`Server Error: ${err.response.data.error || 'Unknown error'}`);
      } else if (err.request) {
        setError('Unable to connect to server. Make sure the backend is running on port 5000.');
      } else {
        setError(`Error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <div className="form-header">
        <button className="back-btn" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
        <h1>🌾 AgriYieldPredictor</h1>
      </div>

      <div className="form-card">
        <h2>Yield Prediction Form</h2>
        
        <form onSubmit={handleSubmit} className="prediction-form">
          {/* User Information */}
          <div className="form-section">
            <h3>User Information</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                />
              </div>
            </div>
          </div>

          {/* Crop Details */}
          <div className="form-section">
            <h3>Crop Details</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="crop_type">Crop Type</label>
                <select
                  id="crop_type"
                  name="crop_type"
                  value={formData.crop_type}
                  onChange={handleInputChange}
                  className="form-select"
                  required
                >
                  <option value="">Select Crop</option>
                  {cropOptions.map(crop => (
                    <option key={crop.value} value={crop.value}>
                      {crop.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="planting_date">Planting Date</label>
                <input
                  type="date"
                  id="planting_date"
                  name="planting_date"
                  value={formData.planting_date}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="YYYY-MM-DD"
                  required
                />
              </div>
            </div>
          </div>

          {/* Previous Yield Data */}
          <div className="form-section">
            <h3>Previous Yield Data</h3>
            <div className="form-group">
              <label htmlFor="previous_yield">Previous Yield (tons/acre)</label>
              <input
                type="number"
                id="previous_yield"
                name="previous_yield"
                value={formData.previous_yield}
                onChange={handleInputChange}
                step="0.1"
                className="form-input"
                placeholder="138"
              />
            </div>
          </div>

          {/* Environmental Factors */}
          <div className="form-section">
            <h3>Environmental Factors</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="temperature">
                  Temperature (°C): {formData.temperature}
                </label>
                <input
                  type="range"
                  id="temperature"
                  name="temperature"
                  min="0"
                  max="50"
                  step="1"
                  value={formData.temperature}
                  onChange={handleSliderChange}
                  className="form-slider"
                />
              </div>
              <div className="form-group">
                <label htmlFor="rainfall">
                  Rainfall (mm): {formData.rainfall}
                </label>
                <input
                  type="range"
                  id="rainfall"
                  name="rainfall"
                  min="0"
                  max="2000"
                  step="10"
                  value={formData.rainfall}
                  onChange={handleSliderChange}
                  className="form-slider"
                />
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            className={`submit-button ${loading ? 'loading' : ''}`}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Calculating...
              </>
            ) : (
              'Submit and View Predictions'
            )}
          </button>
        </form>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <h3> Error</h3>
            <p>{error}</p>
          </div>
        )}

        {/* Results Display */}
        {prediction && (
          <div className="results-card">
            <h3> Prediction Results</h3>
            <div className="result-summary">
              <div className="result-item">
                <span className="result-label">Total Yield</span>
                <span className="result-value">
                  {prediction.total_yield} tons
                </span>
              </div>
              <div className="result-item">
                <span className="result-label">Yield per Hectare</span>
                <span className="result-value">
                  {prediction.yield_per_hectare} tons/ha
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CropPredictorForm;
