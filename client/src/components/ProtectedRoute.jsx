import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Protected route component
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, loading } = useAuth();

    // If still loading, show loading state
    if (loading) {
        return (
            <div style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                height: '100vh',
                fontSize: '20px'
            }}>
                Loading...
            </div>
        );
    }

    // If not authenticated, redirect to login page
    if (!isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }

    // If authenticated, show protected content
    return children;
};

export default ProtectedRoute;

