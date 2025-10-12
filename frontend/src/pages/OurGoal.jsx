import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './OurGoal.css';

const OurGoal = () => {
  return (
    <div className="our-goal-page">
      <Header />
      
      <main className="our-goal-main">
        <div className="our-goal-content">
          <h1 className="our-goal-title">Our Goals</h1>
          <div className="our-goal-placeholder">
            <p>Our company goals and mission coming soon...</p>
            <p>Learn about our vision for home security innovation.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default OurGoal;
