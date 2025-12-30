# 🚀 Token Authentication System - Quick Start Guide

This is a simple step-by-step guide to help you quickly get started with the new JWT Token authentication system.

## ✅ Prerequisites

- Node.js and npm installed
- MongoDB Atlas account and connection string
- Project code cloned

## 📦 Step 1: Install Dependencies

### Install Backend Dependencies
```bash
cd server
npm install mongodb express cors jsonwebtoken bcryptjs
```

### Install Frontend Dependencies
```bash
cd client
npm install
```

## ⚙️ Step 2: Configure Environment Variables

1. Create `config.env` file in the `server/` directory
2. Copy from `config.env.example` or use the following template:

```bash
# server/config.env
ATLAS_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/?retryWrites=true&w=majority
PORT=5050
JWT_SECRET=my-super-secret-key-for-jwt-tokens-change-in-production
```

**⚠️ Important:**
- Replace `ATLAS_URI` with your actual MongoDB connection string
- Use a strong random string for `JWT_SECRET` in production
- **DO NOT** commit `config.env` file to Git!

## 🏃 Step 3: Start the Application

### Start Backend Server
Open first terminal:
```bash
cd server
node --env-file=config.env server
```

You should see:
```
Server is listening on port 5050
```

### Start Frontend Application
Open second terminal:
```bash
cd client
npm start
```

Browser will automatically open `http://localhost:3000`

## 🧪 Step 4: Test Authentication System

### 1. Create Account
1. Click "Find Your Doorbell" or visit `/create`
2. Enter:
   - Username: `testuser`
   - Password: `testpass123`
   - Doorbell Code: `DOORBELL001`
3. Click "Create"
4. You'll automatically login and redirect to `/notifications` page

### 2. Verify Login Status
- Check page header, should show "Welcome, testuser" and "Logout" button
- On NotificationHub page, should display your doorbell ID

### 3. Test Persistent Login
1. Refresh browser page (F5)
2. You should still be logged in
3. Open browser developer tools (F12)
4. Check Application → Local Storage → `http://localhost:3000`
5. You should see `authToken` and `user` keys

### 4. Test Protected Routes
1. Click "Logout" to logout
2. Try accessing `http://localhost:3000/notifications` directly
3. You'll be automatically redirected to login page

### 5. Test Login
1. Use the account you just created to login
2. Enter username and password
3. Click "Connect"
4. Successfully logged in and redirected to notifications page

## 🔍 Step 5: Check Token (Developer Tools)

### View Token in localStorage
1. Open browser developer tools (F12)
2. Go to Application/Storage → Local Storage
3. You'll see:
   ```
   authToken: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   user: {"id":"...","username":"testuser","doorbellID":"DOORBELL001"}
   ```

### Decode JWT Token (Optional)
1. Copy the `authToken` value
2. Visit https://jwt.io
3. Paste token in the "Encoded" area
4. View decoded payload, should contain:
   ```json
   {
     "userId": "...",
     "username": "testuser",
     "doorbellID": "DOORBELL001",
     "iat": ...,
     "exp": ...
   }
   ```

## 📱 Step 6: Test API Requests

### Test Using Browser Console
Open browser console (F12 → Console), run:

```javascript
// Get token
const token = localStorage.getItem('authToken');

// Test protected API endpoint
fetch('http://localhost:5050/record/me', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(res => res.json())
.then(data => console.log('User data:', data))
.catch(err => console.error('Error:', err));
```

### Test Using Postman (Optional)

**Login Request:**
```
POST http://localhost:5050/record/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "testpass123"
}
```

**Get User Info (requires token):**
```
GET http://localhost:5050/record/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🎯 Key Features Summary

### ✅ Implemented Features

1. **User Registration** - Passwords automatically encrypted
2. **User Login** - Generates JWT token
3. **Token Storage** - Auto-saved to localStorage
4. **Persistent Login** - Maintains login state after page refresh
5. **Route Protection** - Unauthenticated users cannot access protected pages
6. **Automatic Logout** - Token expiration auto-redirect
7. **User Info Display** - Header shows username
8. **Secure Passwords** - bcrypt encryption, 10-round salt

### 🔐 Protected Routes

- `/notifications` - requires login
- `/live-video` - requires login

### 🌍 Public Routes

- `/` - Home page
- `/login` - Login page
- `/create` - Registration page
- `/store` - Store
- `/our-goal` - Our Goal
- `/how-it-works` - How It Works
- `/setup-guide` - Setup Guide
- `/safety-ethics` - Safety Ethics
- `/maintenance` - Maintenance

## 🛠️ Troubleshooting

### Issue: Server fails to start
**Error:** `Cannot find module 'jsonwebtoken'`
**Solution:** 
```bash
cd server
npm install jsonwebtoken bcryptjs
```

### Issue: Database connection failed
**Error:** `MongoServerError: Authentication failed`
**Solution:** Check if `ATLAS_URI` in `config.env` is correct

### Issue: Invalid token
**Error:** `Invalid token. Please login again.`
**Solution:** 
1. Clear browser localStorage
2. Re-login
3. Ensure backend `JWT_SECRET` is configured correctly

### Issue: Still redirecting after login
**Solution:**
1. Check browser console for errors
2. Ensure both frontend and backend are running
3. Check if token exists in localStorage
4. Clear browser cache and retry

## 📚 Next Steps

- Read detailed documentation: [TOKEN_AUTHENTICATION.md](TOKEN_AUTHENTICATION.md)
- Check code examples: `client/src/examples/UsageExample.jsx`
- Explore API utility functions: `client/src/utils/api.js`
- Learn authentication context: `client/src/context/AuthContext.jsx`

## 💡 Tips

1. **Development Mode**: Token expires in 7 days by default, can be modified in `server/middleware/auth.js`
2. **Production Environment**: Must change `JWT_SECRET` to a strong random string
3. **Security**: Never hardcode sensitive information in client code
4. **Testing**: Create multiple accounts to test different scenarios
5. **Debugging**: Use browser developer tools to view network requests and localStorage

## 🎉 Done!

Congratulations! You have successfully set up and tested the JWT Token authentication system. Now you can:
- Create new accounts
- Login and logout
- Access protected pages
- Maintain login state in the application
- Use API utility functions for authenticated requests

For any questions, please refer to the complete documentation or contact the development team.

