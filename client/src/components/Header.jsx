import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Header.css';
import SnorlaxLogo from '../assets/snorlax.png';

const Header = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="header-background"></div>
      <div className="header-content">
        <Link to="/" className="logo">
          <img src={SnorlaxLogo} alt="Snorlax Logo" className="snorlax-logo" />
          Snorlax DB
        </Link>
        <nav className="nav-menu">
          <Link to="/store" className="nav-link">Products</Link>
          <Link to="/our-goal" className="nav-link">Our Goal</Link>
        </nav>
        
        {isAuthenticated() ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <Link 
              to="/notifications" 
              className="nav-link" 
              style={{ cursor: 'pointer', textDecoration: 'none' }}
            >
              Welcome, {user?.username}
            </Link>
            <button 
              onClick={handleLogout} 
              className="header-title"
              style={{ 
                cursor: 'pointer',
                border: 'none',
                background: 'transparent',
                color: 'inherit',
                fontSize: 'inherit',
                fontFamily: 'inherit',
                padding: '0'
              }}
            >
              Logout
            </button>
          </div>
        ) : (
          <Link to="/login" className="header-title">Find Your Doorbell</Link>
        )}
      </div>
    </header>
  );
};

export default Header;