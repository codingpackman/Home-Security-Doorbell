import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './Login.css';

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleConnect = () => {
    // Navigate to notifications after login
    navigate('/notifications');
  };

  const handleCreateAccount = () => {
    navigate('/create');
  };

  return (
    <div className="login-page">
      <Header />
      
      <main className="login-main">
        <div className="login-content">
          <div className="login-tab">
            <div className="login-tab-background"></div>
            <div className="login-form">
              <h1 className="login-logo">Bells Bells</h1>
              
              <h2 className="login-title">Sign Into Your Doorbell</h2>
              
              <div className="form-group">
                <label className="form-label">Username</label>
                <input 
                  type="text" 
                  className="form-input"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Password</label>
                <input 
                  type="password" 
                  className="form-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <button className="connect-button" onClick={handleConnect}>
                <span className="button-text">Connect</span>
              </button>

              <div className="register-section">
                <h3 className="register-title">Haven't Registered A Doorbell</h3>
                <button className="register-link" onClick={handleCreateAccount}>
                  Click Here
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Login;
