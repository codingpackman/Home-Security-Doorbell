# JWT Token Authentication System Documentation

## Overview

This project implements a complete JWT (JSON Web Token) authentication system for the Home Security Doorbell web application, providing secure persistent login functionality.

## Key Features

### 1. **Token Generation & Validation**
- JWT tokens automatically generated on login/registration
- 7-day token expiration
- Tokens stored in browser localStorage
- Automatic token inclusion in authenticated requests

### 2. **Password Security**
- Password encryption using bcryptjs
- 10-round salt value for bcrypt
- Backward compatible with existing plain-text passwords
- New passwords are automatically encrypted

### 3. **Protected Routes**
- `/notifications` - requires authentication
- `/live-video` - requires authentication
- Automatic redirection for unauthenticated users

### 4. **Automatic Logout**
- Token expiration handling
- Automatic redirect to login page
- Manual logout functionality

## Usage

### Backend API

#### 1. User Registration
```javascript
POST http://localhost:5050/record
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password",
  "doorbellID": "your_doorbell_code"
}

// Response
{
  "message": "Account created successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "username": "your_username",
    "doorbellID": "your_doorbell_code"
  }
}
```

#### 2. User Login
```javascript
POST http://localhost:5050/record/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}

// Response
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "username": "your_username",
    "doorbellID": "your_doorbell_code"
  }
}
```

#### 3. Get Current User Info (requires authentication)
```javascript
GET http://localhost:5050/record/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// Response
{
  "_id": "507f1f77bcf86cd799439011",
  "username": "your_username",
  "doorbellID": "your_doorbell_code",
  "createdAt": "2025-10-14T12:00:00.000Z"
}
```

### Frontend Usage

#### 1. Using AuthContext
```javascript
import { useAuth } from '../context/AuthContext';

function MyComponent() {
  const { user, token, login, logout, isAuthenticated, getAuthHeader } = useAuth();
  
  // Check if logged in
  if (isAuthenticated()) {
    console.log('User is logged in:', user.username);
  }
  
  // Logout
  const handleLogout = () => {
    logout();
  };
  
  return (
    <div>
      {isAuthenticated() ? (
        <p>Welcome, {user.username}!</p>
      ) : (
        <p>Please login</p>
      )}
    </div>
  );
}
```

#### 2. Using API Utility Functions
```javascript
import api from '../utils/api';

// Get current user info
const fetchUserInfo = async () => {
  try {
    const userData = await api.getCurrentUser();
    console.log(userData);
  } catch (error) {
    console.error('Failed to fetch user:', error);
  }
};

// Get all records
const fetchRecords = async () => {
  try {
    const records = await api.getAllRecords();
    console.log(records);
  } catch (error) {
    console.error('Failed to fetch records:', error);
  }
};
```

#### 3. Protecting Routes
```javascript
// In App.jsx
<Route 
  path="/notifications" 
  element={
    <ProtectedRoute>
      <NotificationHub />
    </ProtectedRoute>
  } 
/>
```

## Security Configuration

### JWT Secret Key
Current default key is defined in `server/middleware/auth.js`:
```javascript
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-this-in-production';
```

**⚠️ IMPORTANT: For production environments:**
1. Set `JWT_SECRET` environment variable in `server/config.env`
2. Use a strong random string as the secret key
3. Never commit the secret key to version control

Example configuration:
```bash
# server/config.env
ATLAS_URI=mongodb+srv://...
PORT=5050
JWT_SECRET=your-very-long-and-random-secret-key-here
```

### Token Storage
- Tokens are stored in browser's localStorage
- Login state persists after page refresh
- Tokens are automatically cleared on logout

### Password Policy
- Recommend minimum 8 characters
- Password strength validation can be added in frontend
- All new passwords are encrypted before storage

## File Structure

```
server/
  ├── middleware/
  │   └── auth.js              # JWT middleware and verification functions
  ├── routes/
  │   └── records.js           # Updated routes with token generation
  └── server.js

client/
  ├── src/
  │   ├── context/
  │   │   └── AuthContext.jsx  # Authentication context
  │   ├── components/
  │   │   ├── Header.jsx       # Updated header with login status
  │   │   └── ProtectedRoute.jsx # Route protection component
  │   ├── pages/
  │   │   ├── Login.jsx        # Updated login page
  │   │   └── Create.jsx       # Updated registration page
  │   ├── utils/
  │   │   └── api.js           # API utility functions
  │   └── App.jsx              # Updated main app with AuthProvider
```

## Testing

### Test Flow:
1. Start backend server:
   ```bash
   cd server
   node --env-file=config.env server
   ```

2. Start frontend:
   ```bash
   cd client
   npm start
   ```

3. Test steps:
   - Visit http://localhost:3000
   - Click "Find Your Doorbell" or visit `/create` to create account
   - Enter username, password, and doorbell code
   - After success, automatically redirect to `/notifications`
   - Refresh page, login state should persist
   - Click "Logout" button in header to logout
   - Try accessing `/notifications` directly, should redirect to login page

## Common Issues

### Q: What happens when token expires?
A: When token expires, the next API request will return 401 error, system will automatically clear local token and redirect to login page.

### Q: How to extend token validity period?
A: Modify in `server/middleware/auth.js`:
```javascript
{ expiresIn: '30d' } // 30 days
```

### Q: How to require authentication for new API routes?
A: Add `verifyToken` middleware in route definition:
```javascript
router.get("/your-route", verifyToken, async (req, res) => {
  // req.user contains decoded user information
  console.log(req.user.userId, req.user.username);
  // Your route logic
});
```

### Q: How to get current logged-in user's information?
A: In frontend:
```javascript
const { user } = useAuth();
console.log(user.username, user.doorbellID);
```

## Future Improvements

1. **Refresh Token** - Implement refresh token mechanism
2. **Password Reset** - Add forgot password functionality
3. **Email Verification** - Add email verification
4. **Two-Factor Authentication** - Enhance security
5. **Session Management** - Manage multi-device login
6. **Password Policy** - Enforce password complexity requirements

## Support

For questions or help:
1. Check documentation: `TOKEN_AUTHENTICATION.md`
2. Check quick start guide: `QUICK_START.md`
3. Check code examples: `client/src/examples/UsageExample.jsx`
4. Contact development team

