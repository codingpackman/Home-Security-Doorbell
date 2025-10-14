// This file demonstrates how to use the authentication system and API utility functions
// This is an example file, not used in the actual application

import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';

const UsageExample = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Example 1: Get current user info
  const fetchCurrentUser = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getCurrentUser();
      setUserData(data);
      console.log('User data:', data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching user:', err);
    } finally {
      setLoading(false);
    }
  };

  // Example 2: Use useEffect to fetch data when component loads
  useEffect(() => {
    if (isAuthenticated()) {
      fetchCurrentUser();
    }
  }, []);

  // Example 3: Manually create authenticated API request
  const customApiRequest = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await fetch('http://localhost:5050/record/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      console.log('Custom request data:', data);
    } catch (err) {
      console.error('Error:', err);
    }
  };

  // Example 4: Handle logout
  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      logout();
      // Can redirect to login page
      // navigate('/login');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Authentication System Usage Example</h1>

      {/* Display authentication status */}
      <div style={{ marginBottom: '20px', padding: '10px', background: '#f0f0f0' }}>
        <h2>Authentication Status</h2>
        <p><strong>Logged In:</strong> {isAuthenticated() ? 'Yes' : 'No'}</p>
        {isAuthenticated() && (
          <>
            <p><strong>Username:</strong> {user?.username}</p>
            <p><strong>Doorbell ID:</strong> {user?.doorbellID}</p>
            <p><strong>User ID:</strong> {user?.id}</p>
          </>
        )}
      </div>

      {/* API Request Examples */}
      <div style={{ marginBottom: '20px', padding: '10px', background: '#f9f9f9' }}>
        <h2>API Request Examples</h2>
        <button 
          onClick={fetchCurrentUser}
          disabled={!isAuthenticated() || loading}
          style={{ marginRight: '10px', padding: '10px 20px', cursor: 'pointer' }}
        >
          {loading ? 'Loading...' : 'Get User Info'}
        </button>
        
        <button 
          onClick={customApiRequest}
          disabled={!isAuthenticated()}
          style={{ marginRight: '10px', padding: '10px 20px', cursor: 'pointer' }}
        >
          Custom API Request
        </button>

        <button 
          onClick={handleLogout}
          disabled={!isAuthenticated()}
          style={{ padding: '10px 20px', cursor: 'pointer', background: '#ff4444', color: 'white', border: 'none' }}
        >
          Logout
        </button>

        {error && (
          <div style={{ marginTop: '10px', padding: '10px', background: '#ffdddd', color: '#cc0000' }}>
            Error: {error}
          </div>
        )}
      </div>

      {/* Display fetched data */}
      {userData && (
        <div style={{ padding: '10px', background: '#e8f5e9' }}>
          <h2>Fetched User Data</h2>
          <pre style={{ background: '#fff', padding: '10px', overflow: 'auto' }}>
            {JSON.stringify(userData, null, 2)}
          </pre>
        </div>
      )}

      {/* Code Examples */}
      <div style={{ marginTop: '20px' }}>
        <h2>Code Examples</h2>
        
        <h3>1. Using AuthContext</h3>
        <pre style={{ background: '#282c34', color: '#abb2bf', padding: '15px', overflow: 'auto' }}>
{`import { useAuth } from '../context/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, logout } = useAuth();
  
  if (!isAuthenticated()) {
    return <div>Please login</div>;
  }
  
  return (
    <div>
      <h1>Welcome, {user.username}!</h1>
      <p>Doorbell ID: {user.doorbellID}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}`}
        </pre>

        <h3>2. Using API Utility Functions</h3>
        <pre style={{ background: '#282c34', color: '#abb2bf', padding: '15px', overflow: 'auto' }}>
{`import api from '../utils/api';

const fetchData = async () => {
  try {
    // 获取当前用户
    const user = await api.getCurrentUser();
    console.log(user);
    
    // 获取所有记录
    const records = await api.getAllRecords();
    console.log(records);
    
    // 更新记录
    await api.updateRecord(userId, { username: 'newname' });
  } catch (error) {
    console.error('Error:', error);
  }
};`}
        </pre>

        <h3>3. Protecting Routes</h3>
        <pre style={{ background: '#282c34', color: '#abb2bf', padding: '15px', overflow: 'auto' }}>
{`import ProtectedRoute from './components/ProtectedRoute';

<Route 
  path="/protected-page" 
  element={
    <ProtectedRoute>
      <YourProtectedComponent />
    </ProtectedRoute>
  } 
/>`}
        </pre>
      </div>
    </div>
  );
};

export default UsageExample;

