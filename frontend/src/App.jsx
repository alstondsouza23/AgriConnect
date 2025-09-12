import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import CropPredictorForm from './components/CropPredictorForm';
import './App.css';
import TeamPage from './components/Team';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/predict" element={<CropPredictorForm />} />
         <Route path="/team" element={<TeamPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
