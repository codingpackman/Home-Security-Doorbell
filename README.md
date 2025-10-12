### Quick Setup (Clones Master Branch And Runs The Frontend) 
```bash
cd <folder-you-want-to-store-your-code>
git clone --branch master https://github.com/codingpackman/Home-Security-Doorbell.git
cd Home-Security-Doorbell
npm install    # only needed the first time
npm start
```

### To Run The Frontend On A Server Hostly On Your PC
```bash
cd <folder you want to store your code>
npm install    #only do this the first time
npm start
```

### To Clone This Branch In The Command Line (Only Do This Once)
```bash
cd <folder you want to store your code>
git clone --branch master https://github.com/codingpackman/Home-Security-Doorbell.git
```

### To Pull From This Branch In The Command Line (Only Do This After You Clone)
```bash
cd <folder you want to store your code>
git pull origin master
```

### To Push To This Branch In The Command Line (Do Not Push Code With Errors)
```bash
cd <folder you want to store your code>
git add .
git commit -m "Your commit message"
git push origin master
```

### To Create Your Own Branch
```bash
cd <folder you want to store your code>
git checkout -b <branchName>
git add .
git commit -m "Your commit message"
git push origin <branchName>
```
