import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './Maintenance.css';

const Maintenance = () => {
  return (
    <div className="maintenance-page">
      <Header />
      
      <main className="maintenance-main">
        <div className="maintenance-content">
          <h1 className="maintenance-title">Maintenance & Wiring Guide</h1>

          {/* Section 1: Disassembly */}
          <section className="maintenance-section">
            <h2 className="section-header">Disassembly Instructions</h2>
            <div className="safety-warning">
              <strong>⚠ SAFETY FIRST</strong>
              Always disconnect the power supply from the doorbell before attempting to open the case or modify wiring.
            </div>
            <p>The doorbell shell consists of three main components: the Front Shell, the Back Shell, and the Camera Holder.</p>
            <ul className="step-list">
              <li>
                <strong>Locate the Mounting Screws:</strong> The Camera Holder sticks into the center of the front shell but is screwed into the back shell (located above the Raspberry Pi).
              </li>
              <li>
                <strong>Unscrew the Holder:</strong> Carefully remove the screws securing the Camera Holder to the back piece.
              </li>
              <li>
                <strong>Separate the Shell:</strong> The Front and Back shell parts are friction-fitted. Once the camera screws are removed, gently pull the front and back sections apart to expose the internals.
              </li>
            </ul>
          </section>

          {/* Section 2: Wiring Diagram */}
          <section className="maintenance-section">
            <h2 className="section-header">Wiring Reference</h2>
            <p>Use this chart to verify all connections. <br/><em>Note: "GPIO" refers to the code pin number, "Physical" refers to the actual pin on the board.</em></p>
            
            <div className="table-responsive">
              <table className="wiring-table">
                <thead>
                  <tr>
                    <th>Component</th>
                    <th>Function</th>
                    <th>GPIO / BCM</th>
                    <th>Physical Pin</th>
                  </tr>
                </thead>
                <tbody>
                  {/* Buttons */}
                  <tr>
                    <td>Doorbell Button</td>
                    <td>Input</td>
                    <td className="pin-gpio">GPIO 14</td>
                    <td className="pin-physical">Pin 8</td>
                  </tr>
                  <tr>
                    <td>Stop Button</td>
                    <td>Input</td>
                    <td className="pin-gpio">GPIO 15</td>
                    <td className="pin-physical">Pin 10</td>
                  </tr>
                  
                  {/* Buzzer */}
                  <tr>
                    <td>Buzzer</td>
                    <td>Output</td>
                    <td className="pin-gpio">GPIO 18</td>
                    <td className="pin-physical">Pin 12</td>
                  </tr>

                  {/* Motion Sensors */}
                  <tr>
                    <td>PIR Sensor</td>
                    <td>Motion</td>
                    <td className="pin-gpio">GPIO 27</td>
                    <td className="pin-physical">Pin 13</td>
                  </tr>
                  <tr>
                    <td>Ultrasonic 1</td>
                    <td>Trigger</td>
                    <td className="pin-gpio">GPIO 23</td>
                    <td className="pin-physical">Pin 16</td>
                  </tr>
                  <tr>
                    <td>Ultrasonic 1</td>
                    <td>Echo</td>
                    <td className="pin-gpio">GPIO 24</td>
                    <td className="pin-physical">Pin 18</td>
                  </tr>
                  <tr>
                    <td>Ultrasonic 2</td>
                    <td>Trigger</td>
                    <td className="pin-gpio">GPIO 25</td>
                    <td className="pin-physical">Pin 22</td>
                  </tr>
                  <tr>
                    <td>Ultrasonic 2</td>
                    <td>Echo</td>
                    <td className="pin-gpio">GPIO 12</td>
                    <td className="pin-physical">Pin 32</td>
                  </tr>

                  {/* Camera Section - Added spacing row */}
                  <tr><td colSpan="4" style={{backgroundColor: '#eee', height: '5px', padding: '0'}}></td></tr>

                  {/* Arducam Wiring */}
                  <tr>
                    <td rowSpan="5" style={{verticalAlign: 'middle', fontWeight: 'bold'}}>Arducam 2MP Mini+</td>
                    <td>3.3V Power</td>
                    <td className="pin-gpio">-</td>
                    <td className="pin-physical">Pin 1</td>
                  </tr>
                  <tr>
                    <td>I2C (SDA / SCL)</td>
                    <td className="pin-gpio">GPIO 2 / 3</td>
                    <td className="pin-physical">Pins 3 & 5</td>
                  </tr>
                  <tr>
                    <td>Ground</td>
                    <td className="pin-gpio">-</td>
                    <td className="pin-physical">Pin 6</td>
                  </tr>
                  <tr>
                    <td>SPI Chip Select (CS)</td>
                    <td className="pin-gpio">GPIO 17</td>
                    <td className="pin-physical">Pin 11</td>
                  </tr>
                  <tr>
                    <td>SPI (MOSI, MISO, CLK)</td>
                    <td className="pin-gpio">GPIO 10, 9, 11</td>
                    <td className="pin-physical">Pins 19, 21, 23</td>
                  </tr>
                </tbody>
              </table>
            </div>
                      </section>

          {/* Section 3: Advanced Troubleshooting */}
          <section className="maintenance-section">
            <h2 className="section-header">System Diagnostics</h2>
            <div className="troubleshoot-grid">
              <div className="troubleshoot-card">
                <h4>Raspberry Pi Check</h4>
                <p>If the device is unresponsive:</p>
                <ol style={{paddingLeft: '20px', margin: '0'}}>
                  <li>Remove the Raspberry Pi from the case.</li>
                  <li>Connect it to an external monitor and keyboard.</li>
                  <li>Power on to verify the boot sequence is completing without errors.</li>
                </ol>
              </div>
              <div className="troubleshoot-card">
                <h4>Sensor Cleaning</h4>
                <p>
                  Dust accumulation on the <strong>Ultrasonic</strong> or <strong>PIR sensors</strong> can cause false readings. 
                  Gently wipe sensors with a dry, microfiber cloth during maintenance checks.
                </p>
              </div>
            </div>
          </section>

        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Maintenance;