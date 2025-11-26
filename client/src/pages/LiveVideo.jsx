import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './LiveVideo.css';

const LiveVideo = () => {
  const [videoError, setVideoError] = useState(false);
  const videoUrl = "https://doorbell-video-elec290.s3.us-east-1.amazonaws.com/video.mp4";

  const handleVideoError = () => {
    setVideoError(true);
  };

  return (
    <div className="live-video-page">
      <Header />
      
      <main className="live-video-main">
        <div className="live-video-content">
          <h1 className="video-title">Live Video Will Be Shown Here</h1>
          <div className="video-container">
            {!videoError ? (
              <video 
                className="video-player"
                controls
                onError={handleVideoError}
              >
                <source src={videoUrl} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            ) : (
              <div className="video-error">
                <p>Unable to load video</p>
                <p className="error-details">Please check your connection or try again later</p>
              </div>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default LiveVideo;
