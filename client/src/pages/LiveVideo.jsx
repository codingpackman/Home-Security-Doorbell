import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './LiveVideo.css';

const LiveVideo = () => {
  const [searchParams] = useSearchParams();
  const [videoError, setVideoError] = useState(false);
  const [videoUrl, setVideoUrl] = useState("");
  
  // S3 bucket base URL
  const S3_BUCKET_BASE = "https://doorbell-video-elec290.s3.us-east-1.amazonaws.com";

  useEffect(() => {
    // Get video path from URL parameter
    const videoParam = searchParams.get('video');
    
    if (videoParam) {
      // If video parameter exists, construct full S3 URL
      // Remove leading slash if present and construct URL
      const cleanPath = videoParam.startsWith('/') ? videoParam.slice(1) : videoParam;
      setVideoUrl(`${S3_BUCKET_BASE}/${cleanPath}`);
    } else {
      // Default to live video or a default video
      setVideoUrl(`${S3_BUCKET_BASE}/videos1.mp4`);
    }
  }, [searchParams]);

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
            {!videoError && videoUrl ? (
              <video 
                key={videoUrl} // Force re-render when URL changes
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
