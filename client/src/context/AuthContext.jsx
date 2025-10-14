import React, { createContext, useState, useContext, useEffect } from 'react';

// Create authentication context
const AuthContext = createContext(null);

// Custom hook to use authentication context
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

// Authentication provider component
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true);

    // Read token and user info from localStorage on initialization
    useEffect(() => {
        const storedToken = localStorage.getItem('authToken');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
            setToken(storedToken);
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    // Login function
    const login = (authToken, userData) => {
        setToken(authToken);
        setUser(userData);
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('user', JSON.stringify(userData));
    };

    // Logout function
    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
    };

    // Check if user is authenticated
    const isAuthenticated = () => {
        return !!token && !!user;
    };

    // Get authorization request header
    const getAuthHeader = () => {
        if (token) {
            return {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            };
        }
        return {
            'Content-Type': 'application/json'
        };
    };

    const value = {
        user,
        token,
        login,
        logout,
        isAuthenticated,
        getAuthHeader,
        loading
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

