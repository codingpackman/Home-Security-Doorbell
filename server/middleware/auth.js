import jwt from 'jsonwebtoken';

// Secret key for JWT - should use environment variable in production
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-this-in-production';

// Generate JWT Token
export const generateToken = (userId, username, doorbellID) => {
    return jwt.sign(
        { 
            userId, 
            username, 
            doorbellID 
        },
        JWT_SECRET,
        { expiresIn: '7d' } // Token expires in 7 days
    );
};

// Verify JWT Token middleware
export const verifyToken = (req, res, next) => {
    try {
        // Get token from request header
        const token = req.headers.authorization?.split(' ')[1]; // Format: "Bearer TOKEN"
        
        if (!token) {
            return res.status(401).json({ 
                message: 'No token provided. Please login first.' 
            });
        }

        // Verify token
        const decoded = jwt.verify(token, JWT_SECRET);
        
        // Attach decoded user info to request object
        req.user = decoded;
        
        next();
    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ 
                message: 'Token expired. Please login again.' 
            });
        }
        return res.status(401).json({ 
            message: 'Invalid token. Please login again.' 
        });
    }
};

