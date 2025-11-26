import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './SetupGuide.css';

const SetupGuide = () => {
  return (
    <div className="setup-guide-page">
      <Header />
      
      <main className="setup-guide-main">
        <div className="setup-guide-content">
          <h1 className="setup-guide-title">Quick Start Guide</h1>

          {/* Section 1: Box Contents */}
          <section className="box-contents">
            <h2>What's in the Box?</h2>
            <div className="checklist-grid">
              <div className="checklist-item"><span className="check-icon">✓</span> Smart Doorbell Unit</div>
              <div className="checklist-item"><span className="check-icon">✓</span> Mounting Screws (x2)</div>
              <div className="checklist-item"><span className="check-icon">✓</span> USB-C Power Cable</div>
              <div className="checklist-item"><span className="check-icon">✓</span> Wall Anchors</div>
            </div>
          </section>

          {/* Section 2: Installation Steps */}
          <div className="setup-steps">
            
            {/* Step 1 */}
            <div className="step-card">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Separate the Shell</h3>
                <p>
                  The doorbell comes pre-assembled. To mount it, you must separate the <strong>Back Shell</strong> from the <strong>Front Shell</strong>. 
                  These parts are friction-fitted. Firmly grip both sides and pull them apart gently.
                </p>
                
                <div className="note">Note: Do not remove the screws holding the camera module.</div>
              </div>
            </div>

            {/* Step 2 */}
            <div className="step-card">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Mount the Back Plate</h3>
                <p>
                  Place the Back Shell against your wall or doorframe at the desired height (recommended 48 inches from the ground). 
                  Use the provided screws to secure the back plate to the surface.
                </p>
                
              </div>
            </div>

            {/* Step 3 */}
            <div className="step-card">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Connect Power & Reassemble</h3>
                <p>
                  Pass your power cable through the back plate opening and plug it into the Raspberry Pi power port. 
                  Once powered, snap the Front Shell back onto the mounted Back Plate until it clicks securely.
                </p>
              </div>
            </div>

            {/* Step 4 */}
            <div className="step-card">
              <div className="step-number">4</div>
              <div className="step-content">
                <h3>System Initialization</h3>
                <p>
                  The device will boot up automatically. You will hear a confirmation tone from the buzzer.
                  <br /><br />
                  <strong>Button Functions:</strong>
                  <br />• <strong>Main Button:</strong> Rings the doorbell.
                  <br />• <strong>Secondary Button:</strong> Used for stopping the alarm or resetting network settings.
                </p>
              </div>
            </div>

          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default SetupGuide;