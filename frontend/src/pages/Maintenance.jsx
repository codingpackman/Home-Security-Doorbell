import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './Maintenance.css';

const Maintenance = () => {
  return (
    <div className="maintenance-page">
      <Header />
      
      <main className="maintenance-main">
        <div className="maintenance-content">
          <h1 className="maintenance-title">Maintenance suggestions</h1>
          <div className="maintenance-placeholder">
            <p>Maintenance tips and suggestions coming soon...</p>
            <p>Keep your doorbell in perfect working condition.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Maintenance;
