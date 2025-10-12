import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-background"></div>
      <div className="header-content">
        <Link to="/" className="logo">Bells Bells</Link>
        <nav className="nav-menu">
          <Link to="/store" className="nav-link">Products</Link>
          <Link to="/our-goal" className="nav-link">Our Goal</Link>
        </nav>
        <Link to="/login" className="header-title">Find Your Doorbell</Link>
      </div>
    </header>
  );
};

export default Header;
