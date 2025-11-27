import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './NotificationHub.css';

const NotificationHub = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = async () => {
        const token = localStorage.getItem("token"); // Retrieve token from localStorage
        console.log("Token being sent:", token); // Debug log

        try {
            const response = await fetch("http://localhost:5050/notification", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`, // Pass the token for authentication
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Fetched notifications:", data); // Debug log
                setNotifications(data);
            } else {
                console.error("Failed to fetch notifications");
            }
        } catch (err) {
            console.error("Error:", err);
        }
    };

    fetchNotifications();
  }, []);

  const handleLiveVideoClick = () => {
    navigate('/live-video');
  };

  const handleSeeRecordingClick = (recordingPath) => {
    // Navigate to live-video page with the recording path as a query parameter
    navigate(`/live-video?video=${encodeURIComponent(recordingPath)}`);
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

          {notifications.map((notification) => (
            <div className="notification-item" key={notification._id}>
              <div className="notification-card">
                <div className="notification-info">
                  <div className="notification-description">{notification.notificationType}</div>
                  <div className="notification-datetime">{notification.dateTime}</div>
                </div>
                <button 
                  className="recording-button"
                  onClick={() => handleSeeRecordingClick(notification.recordingPath)}
                >
                  <span className="button-text">See Recording</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default NotificationHub;