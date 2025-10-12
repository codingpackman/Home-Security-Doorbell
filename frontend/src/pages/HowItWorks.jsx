import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './HowItWorks.css';

const HowItWorks = () => {
  return (
    <div className="how-it-works-page">
      <Header />
      
      <main className="how-it-works-main">
        <div className="how-it-works-content">
          <h1 className="how-it-works-title">How The Product Works!</h1>
          <div className="how-it-works-placeholder">
            <p>Detailed product information coming soon...</p>
            <p>Learn how our innovative doorbell system operates.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default HowItWorks;
