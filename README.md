### Website Explaination
  -  This current branch of the website has an implemented frontend, backend and database.
  -  The Frontend handles all the routing and page layouts.
  -  The backend handles the database and all of the doorbell login information stored in the database.
  -  **NEW: JWT Token Authentication System** - Users stay logged in after authentication
  -  **NEW: Notifications collection added** - New collection storing all notifications to all doorbells
  -  When adding credentials into the create account page, the username, password (encrypted), and doorbellID will be added to the database.
  -  Passwords are now encrypted using bcryptjs for security
  -  JWT tokens are generated on login/registration and stored in localStorage
  -  Protected routes (/notifications, /live-video) require authentication
  -  The Database requires a password to be accessed in config.env file.
  -  You can use your own database password or get the one I am currently using.
  -  **IMPORTANT:** Please do not push any database passwords or JWT secrets as that is sensitive information.

### Quick Setup (Clones Current Branch And Runs The Website) 
```bash
cd <folder-you-want-to-store-your-code>
git clone --branch feature/frontend+login-ep https://github.com/codingpackman/Home-Security-Doorbell.git
cd client
npm install    # only needed the first time
npm start
```
In A second Terminal Running At The Same Time As The First
```bash
cd server
npm install mongodb express cors   # only needed the first time
node --env-file=config.env server   # password for database needed in config.env file
```

### To Run The Frontend On A Server Hosted On Your PC
```bash
cd <folder you want to store your code>
npm install    #only do this the first time
npm start
```

### To Run The Backend + Database On A Server Hosted On Your PC
```bash
cd server
npm install mongodb express cors jsonwebtoken bcryptjs   # only needed the first time
node --env-file=config.env server   # password for database needed in config.env file
```

### 🔐 Security Configuration (config.env)
```bash
# server/config.env
ATLAS_URI=your_mongodb_connection_string
PORT=5050
JWT_SECRET=your-very-long-and-random-secret-key-here  # Add this for production!
```

### 📚 Documentation
- For detailed information about the Token Authentication System, see [TOKEN_AUTHENTICATION.md](TOKEN_AUTHENTICATION.md)

### To Clone This Branch In The Command Line (Only Do This Once)
```bash
cd <folder you want to store your code>
git clone --branch feature/frontend+login-ep https://github.com/codingpackman/Home-Security-Doorbell.git
```

### To Pull From This Branch In The Command Line (Only Do This After You Clone)
```bash
cd <folder you want to store your code>
git pull origin feature/frontend+login-ep
```

### To Push To This Branch In The Command Line (Do Not Push Code With Errors)
```bash
cd <folder you want to store your code>
git add .
git commit -m "Your commit message"
git push origin feature/frontend+login-ep
```

### To Create Your Own Branch
```bash
cd <folder you want to store your code>
git checkout -b <branchName>
git add .
git commit -m "Your commit message"
git push origin <branchName>
```
"# website-for-doorbell" 
"# website-for-doorbell" 
