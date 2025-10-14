import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './NotificationHub.css';

const NotificationHub = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleLiveVideoClick = () => {
    navigate('/live-video');
  };

  return (
    <div className="notification-hub-page">
      <Header />

      <main className="notification-main">
        <div className="notification-content">
          <div className="notification-header">
            <h1 className="page-title">Notification List</h1>
            <div style={{ marginBottom: '10px', color: '#666' }}>
              Connected Doorbell: <strong>{user?.doorbellID || 'N/A'}</strong>
            </div>
            <button className="live-video-button" onClick={handleLiveVideoClick}>
              <span className="button-text">Live Video</span>
            </button>
          </div>

          <div className="notification-item">
            <div className="notification-card">
              <div className="notification-info">
                <div className="notification-description">Notification Description</div>
                <div className="notification-datetime">Date and Time</div>
              </div>
              <button className="recording-button">
                <span className="button-text">See Recording</span>
              </button>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default NotificationHub;
