import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Team.css';
import logo from '../assets/AgriConnect_logo.png'; // <-- added

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

   </div>
  );
};

export default TeamPage;