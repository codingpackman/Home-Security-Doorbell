import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './Create.css';

const Create = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [connectionCode, setConnectionCode] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleCreate = async () => {
    try {
      const response = await fetch("http://localhost:5050/record", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
          doorbellID: connectionCode,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Save token and user info
        login(data.token, data.user);
        // Navigate to notifications after successful account creation
        navigate('/notifications');
      } else {
        console.error("Failed to create account");
        setErrorMessage(data.message || "Failed to create account");
      }
    } catch (err) {
      console.error("Error:", err);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  return (
    <div className="create-page">
      <Header />
      
      <main className="create-main">
        <div className="create-content">
          <div className="creation-tab">
            <div className="creation-tab-background"></div>
            <div className="creation-form">
              <h1 className="creation-logo">Bells Bells</h1>
              
              <h2 className="creation-title">Find Your Doorbell</h2>
              
              {errorMessage && (
                <div style={{ color: 'red', marginBottom: '10px', textAlign: 'center' }}>
                  {errorMessage}
                </div>
              )}
              
              <div className="form-group">
                <label className="form-label">Create a Username</label>
                <input 
                  type="text" 
                  className="form-input"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Create a Password</label>
                <input 
                  type="password" 
                  className="form-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Doorbell Connection Code</label>
                <input 
                  type="text" 
                  className="form-input"
                  value={connectionCode}
                  onChange={(e) => setConnectionCode(e.target.value)}
                />
              </div>

              <button className="create-button" onClick={handleCreate}>
                <span className="button-text">Create</span>
              </button>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Create;
