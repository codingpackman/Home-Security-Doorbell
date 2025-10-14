import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Header.css';

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
        <Link to="/" className="logo">Bells Bells</Link>
        <nav className="nav-menu">
          <Link to="/store" className="nav-link">Products</Link>
          <Link to="/our-goal" className="nav-link">Our Goal</Link>
        </nav>
        
        {isAuthenticated() ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <span className="nav-link" style={{ cursor: 'default' }}>
              Welcome, {user?.username}
            </span>
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
