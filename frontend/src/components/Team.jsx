import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Team.css';
import logo from '../assets/AgriConnect_logo.png'; // <-- added
import livona from '../assets/livona.png';
import PixelCard from './UI/PixelCard';



const TeamPage = () => {
  const navigate = useNavigate();

 const handleHomeClick = () => {
    navigate('/');
  };

  return (
   <div className="team-container">
    {/* Glass Effect Navbar */}
      <nav className="glass-navbar">
        <div className="navbar-content">
          <div className="logo-container">
            <img src={logo} alt="AgriYield Logo" className="logo" />
          </div>
          <div className="nav-links">
            <button className="nav-link" onClick={handleHomeClick}>Home</button>
            <button className="nav-link active">Team</button>
          </div>
        </div>
      </nav>
      {/* Main Title */}
      <header className="main-header">
        <h1 className="main-title">Team</h1>
      </header>
      <div className="team-members">
        <PixelCard variant="blue">
          {/* <img src={livona} alt="Livona" className="team-photo" style={{ position: 'absolute', top: '10px', left: '25%' }} /> */}
          <h2 style={{ position: 'absolute', top: '10px', left: '25%' }}>Livona</h2>
          <p style={{ position: 'absolute', top: '40px', left: '25%' }}>Frontend</p>
        </PixelCard>
      </div>
      </div>
  );
};

export default TeamPage;