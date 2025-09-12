import React from 'react';
import { useNavigate } from 'react-router-dom';
import Orb from './Orb';
import './HomePage.css';
import logo from '../assets/AgriConnect_logo.png'; // <-- added

const HomePage = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/predict');
  };

  const handleTeamClick = () => {
    navigate('/team');
  };

  return (
    <div className="home-container">
      {/* Glass Effect Navbar */}
      <nav className="glass-navbar">
        <div className="navbar-content">
          <div className="logo-container">
            <img src={logo} alt="AgriYield Logo" className="logo" />
          </div>
          <div className="nav-links">
            <button className="nav-link active">Home</button>
            <button className="nav-link" onClick={handleTeamClick}>Team</button>
          </div>
        </div>
      </nav>

      {/* Main Title */}
      <header className="main-header">
        <h1 className="main-title">Agriculture Yield Predictor</h1>
      </header>

      {/* Main Content with Orb */}
      <main className="home-main">
        <div className="orb-wrapper">
          <Orb hue={120} hoverIntensity={0.3} rotateOnHover={true} />
          
          <div className="orb-content">
            <p className="tagline">Growing tomorrow's harvest with today's smart technology</p>
            <button className="get-started-btn" onClick={handleGetStarted}>
              Get Started
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HomePage;
