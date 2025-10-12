import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './SafetyEthics.css';

const SafetyEthics = () => {
  return (
    <div className="safety-ethics-page">
      <Header />
      
      <main className="safety-ethics-main">
        <div className="safety-ethics-content">
          <h1 className="safety-ethics-title">Safety and Ethics or Smth</h1>
          <div className="safety-ethics-placeholder">
            <p>Safety and ethics information coming soon...</p>
            <p>Our commitment to responsible home security practices.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default SafetyEthics;
