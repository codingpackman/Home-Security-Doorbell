import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './LiveVideo.css';

const LiveVideo = () => {
  return (
    <div className="live-video-page">
      <Header />
      
      <main className="live-video-main">
        <div className="live-video-content">
          <h1 className="video-title">Live Video Will Be Shown Here</h1>
          <div className="video-placeholder">
            {/* Video component would go here */}
            <div className="video-coming-soon">
              <p>Live Video Feed</p>
              <p>Coming Soon</p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default LiveVideo;
