import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './SafetyEthics.css';

const SafetyEthics = () => {
  return (
    <div className="safety-ethics-page">
      <Header />
      
      <main className="safety-ethics-main">
        <div className="safety-ethics-content">
          <h1 className="safety-ethics-title">Safety Standards & Ethical Commitment</h1>
          
          <p className="intro-blurb">
            We believe that securing your home shouldn't mean compromising your privacy or safety. 
            Transparency is at the core of our design philosophy.
          </p>

          <div className="policy-section">
            
            {/* Card 1: Data Privacy (Ethics) */}
            <div className="policy-card">
              <h2>
                <span role="img" aria-label="shield">🛡️</span> 
                Data Privacy & Ownership
              </h2>
              <p>
                Unlike commercial smart doorbells that upload footage to remote servers, our system is designed for <strong>local processing</strong>.
              </p><ul className="policy-list">
                <li><strong>No Cloud Storage:</strong> All video data is processed directly on the Raspberry Pi. You own the hardware, so you own the data.</li>
                <li><strong>Local Network Only:</strong> Notifications and video streams are transmitted over your local secure network.</li>
                <li><strong>Responsible Surveillance:</strong> We encourage users to position the Arducam to focus solely on their private property to respect neighbor privacy.</li>
              </ul>
            </div>

            {/* Card 2: Hardware Safety */}
            <div className="policy-card warning">
              <h2>
                <span role="img" aria-label="warning">⚠️</span> 
                Hardware Safety
              </h2>
              <p>
                This device utilizes exposed electronic components. Please adhere to the following safety guidelines during maintenance or installation.
              </p><ul className="policy-list">
                <li><strong>Low Voltage Handling:</strong> The Raspberry Pi and Arducam operate on 3.3V and 5V logic. Do not connect these components directly to mains electricity (120V/240V).</li>
                <li><strong>Moisture Protection:</strong> Ensure the friction-fit shell is securely closed before mounting to prevent moisture from reaching the pins.</li>
                <li><strong>Static Electricity:</strong> When handling the internal board (during the disassembly described in the Maintenance section), ground yourself to avoid damaging the GPIO pins.</li>
              </ul>

              <div className="voltage-alert">
                <strong>ELECTRICAL WARNING:</strong> <br/>
                Ensure the 3.3V (Pin 1) and Ground (Pin 6) connections are never bridged, as this will permanently damage the Raspberry Pi unit.
              </div>
            </div>

          </div>

          <div className="policy-card" style={{borderLeftColor: '#00cec9'}}>
             <h2>Community & Open Source</h2>
             <p>
               We believe in the right to repair and modify. Our hardware pinouts and software logic are transparent, allowing you to audit the code and ensure the device behaves exactly as you expect it to.
             </p>
          </div>

        </div>
      </main>

      <Footer />
    </div>
  );
};

export default SafetyEthics;