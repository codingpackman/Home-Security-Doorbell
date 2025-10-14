import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './SetupGuide.css';

const SetupGuide = () => {
  return (
    <div className="setup-guide-page">
      <Header />
      
      <main className="setup-guide-main">
        <div className="setup-guide-content">
          <h1 className="setup-guide-title">How To Setup...</h1>
          <div className="setup-guide-placeholder">
            <p>Setup instructions coming soon...</p>
            <p>Step-by-step guide for installing your doorbell.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default SetupGuide;
