import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Team.css';
import logo from '../assets/AgriConnect_logo.png';
import livona from '../assets/livona.png';
import alston from '../assets/alston.png';
import aidon from '../assets/aidon.png';
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
        <PixelCard variant="blue" className='livona-card'>
          <img src={livona} alt="Livona" className="team-photo" style={{ position: 'absolute', top: '-13%', left: '-5%' }} />
          <h2 style={{ position: 'absolute', top: '80%', left: '38%' }}>Livona</h2>
          <p style={{ position: 'absolute', top: '87%', left: '39%' }}>Frontend</p>
        </PixelCard>
        <PixelCard variant="blue" className='alston-card'>
          <img src={alston} alt="Alston" className="team-photo" style={{ position: 'absolute', top: '-13%', left: '-5%' }} />
          <h2 style={{  position: 'absolute', top: '80%', left: '38%' }}>Alston</h2>
          <p style={{ position: 'absolute', top: '87%', left: '39%' }}>Backend</p>
        </PixelCard>
        <PixelCard variant="blue" className='aidon-card'> 
          <img src={aidon} alt="Aidon" className="team-photo" style={{ position: 'absolute', top: '-13%', left: '-5%' }} />
          <h2 style={{  position: 'absolute', top: '80%', left: '38%' }}>Aidon</h2>
          <p style={{ position: 'absolute', top: '87%', left: '38%' }}>Frontend</p>
        </PixelCard>
      </div>
      </div>
  );
};

export default TeamPage;