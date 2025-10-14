//Continue Session npx builder.io@latest code --url "cgen://completion/cgen-36f3382dadf64428b80a1a5e3b6d63a2"

import React from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  const handleStoreClick = () => {
    navigate('/store');
  };

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="home-page">
      <Header />

      <main className="home-main">
        <div className="home-content">
          <div className="info-sections">
            <div className="purchase-info-section">
              <h2 className="section-title">Bells Bells Is The New Innovator In The Home Security Industry!</h2>
              <p className="section-description">Want To Get Your Hands On One Of Our Premium Doorbells</p>
              <button className="store-button" onClick={handleStoreClick}>
                <span className="button-text">Purchase A Doorbell</span>
              </button>
            </div>

            <div className="access-info-section">
              <h2 className="section-title">Do You Already Own A Premium Doorbell From Us?</h2>
              <p className="section-description">Login To Access Everything That Comes With Out Doorbell</p>
              <button className="login-button" onClick={handleLoginClick}>
                <span className="button-text white-text">Find Your Doorbell</span>
              </button>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Home;
