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
          <h1 className="how-it-works-title">Intelligent Security Logic</h1>
          
          <p className="intro-text">
            Our doorbell isn't just a camera; it's a smart environmental analyzer. 
            By combining heat signatures with ultrasonic depth mapping, we eliminate false alarms 
            and ensure you only get notified when it matters.
          </p>

          {/* Section 1: The 3-Step Process */}
          <section className="workflow-grid">
            <div className="workflow-card">
              <div className="step-number">1</div>
              <h3>Motion Detection</h3>
              <p>
                The system uses a <strong>PIR (Passive Infrared) sensor</strong> to detect heat signatures from living beings, ensuring falling leaves or moving shadows don't trigger the system.
              </p>
            </div>

            <div className="workflow-card">
              <div className="step-number">2</div>
              <h3>Depth Validation</h3>
              <p>
                Once motion is detected, <strong>two Ultrasonic Sensors</strong> activate to measure the precise distance of the object. This verifies that a visitor is actually approaching the door.
              </p>
            </div>

            <div className="workflow-card">
              <div className="step-number">3</div>
              <h3>Instant Notification</h3>
              <p>
                Upon validation, the camera records the event and pushes a notification immediately to your app, allowing you to view the visitor in real-time.
              </p>
            </div>
          </section>

          {/* Section 2: Technical Breakdown */}
          <section className="tech-section">
            <div>
              <h2 className="tech-header">The Multi-Sensor Advantage</h2>
              <div className="sensor-diagram">
                <div className="sensor-text">
                  <p style={{ marginBottom: '20px', lineHeight: '1.6' }}>
                    Most doorbells rely on a single method of detection, leading to constant false alarms. 
                    Our system employs a <strong>Triple-Check Protocol</strong>:
                  </p>
                  <div className="sensor-details">
                    <ul>
                      <li>
                        <strong>PIR Sensor (The Scout)</strong>
                        Constantly monitors for changes in infrared heat radiation (human body heat). 
                        It acts as the low-power trigger to wake the system up.
                        
                      </li>
                      <li>
                        <strong>Dual Ultrasonic Array (The Validators)</strong>
                        Two sensors emit high-frequency sound waves to create a depth map. 
                        By using two sensors, we can determine not just presence, but position and approach speed.
                        
                      </li>
                      <li>
                        <strong>Video Capture</strong>
                        Once the sensors agree, the camera captures high-definition video which is securely processed and streamed.
                      </li>
                    </ul>
                  </div>
                </div>
                {/* This is a placeholder for an image if you have one, or a CSS illustration */}
                <div style={{ background: '#f1f3f5', height: '300px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#aaa' }}>
                 
                </div>
              </div>
            </div>
          </section>

        </div>
      </main>

      <Footer />
    </div>
  );
};

export default HowItWorks;