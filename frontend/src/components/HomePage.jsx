import React from 'react';
import { useNavigate } from 'react-router-dom';
import Orb from './Orb';
import './HomePage.css';
import logo from '../assets/AgriConnect_logo.png';
import workflowImg from '../assets/workflow.png';
import TextType from './UI/TextType'; 

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

      {/* Description Section */}
      <section className="description-section">
        <header className="description-header">
          <h2 className="description-title">Project Description</h2>
        </header>
        
        <div className="text-section">
          <div className="text-container">
            <TextType
              text={[
                "This project aims to develop a web-based crop yield prediction system that leverages machine learning to estimate the expected yield of various crops based on user-provided inputs such as crop type, area, soil conditions, weather data, and farming practices.",
                "The goal is to provide farmers and agricultural stakeholders with actionable insights that can help them make informed decisions regarding crop planning, resource allocation, and risk management.",
                "The system consists of a user-friendly React frontend that gathers relevant cultivation data through a form, and a Python Flask backend powered by a machine learning model that processes the data and returns a yield prediction.",
                "The model is trained on historical datasets that include parameters like temperature, rainfall, humidity, soil pH, fertilizer use, and actual yields recorded for different crops."
              ]}
              typingSpeed={50}
              pauseDuration={2000}
              showCursor={true}
              cursorCharacter="|"
            />
          </div>
        </div>

        {/* Workflow Section */}
        <div className="workflow-section">
          <h3 className="workflow-title">Workflow Architecture</h3>
          <div className="workflow-container">
            <img src={workflowImg} alt="Workflow Diagram" className="workflow-image" />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4 className="footer-title">Agriculture Yield Predictor</h4>
            <p className="footer-text">
              Empowering farmers with AI-driven insights for better crop planning and sustainable agriculture.
            </p>
          </div>
          
          <div className="footer-section">
            <h5 className="footer-subtitle">Features</h5>
            <ul className="footer-list">
              <li>ML-powered predictions</li>
              <li>Multi-crop support</li>
              <li>Weather integration</li>
              <li>Real-time analysis</li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h5 className="footer-subtitle">Technology</h5>
            <ul className="footer-list">
              <li>React Frontend</li>
              <li>Flask Backend</li>
              <li>Scikit-learn ML</li>
              <li>Python Analytics</li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h5 className="footer-subtitle">Contact</h5>
            <ul className="footer-list">
              <li> info@agriyield.com</li>
              <li> www.xyz.com</li>
              <li> +91 6969696969</li>
              <li> Agriculture Tech Hub</li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom">
          <div className="footer-border"></div>
          <p className="footer-copyright">
            © 2025 Agriculture Yield Predictor. Crafted by Team Optivius
          </p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
