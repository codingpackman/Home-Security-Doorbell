import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-background"></div>
      <div className="footer-content">
        <div className="footer-left">
          <div className="footer-section-title">Support and Wiki Pages</div>
          <Link to="/how-it-works" className="footer-link">How It Works</Link>
          <Link to="/setup-guide" className="footer-link">Setup Guide</Link>
          <Link to="/safety-ethics" className="footer-link">Safety and Ethics</Link>
          <Link to="/maintenance" className="footer-link">Maintenance</Link>
        </div>
        <div className="footer-right">
          <div className="footer-section-title">Contact Us</div>
          <div className="footer-email">BellsBells@gmail.com</div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
