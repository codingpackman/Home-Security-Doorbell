import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './Create.css';

const Create = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [connectionCode, setConnectionCode] = useState('');

  const handleCreate = () => {
    // Navigate to notifications after account creation
    navigate('/notifications');
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
