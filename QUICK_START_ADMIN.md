# 🚀 Quick Start Guide - Admin Panel Phase 3

## Complete Setup in 5 Steps

### Step 1: Create Admin User (2 minutes)

```cmd
cd "c:\Users\anshu\OneDrive\Desktop\5th sem\New folder\IS_project\server"
python setup_admin.py
```

**Enter when prompted:**
- Username: `admin` (or your choice)
- Password: `admin123` (or secure password)
- Email: (optional, just press Enter)

**You should see:**
```
✅ Admin user 'admin' created successfully!
🎉 SETUP COMPLETE!
```

---

### Step 2: Install React Dependencies (3 minutes)

```cmd
cd "..\admin_panel"
npm install
```

**This installs:**
- React + React Router
- Tailwind CSS
- Axios
- Recharts
- Lucide Icons

---

### Step 3: Start Flask Server (Terminal 1)

```cmd
cd "..\server"
python app.py
```

**Look for:**
```
[App] 🔐 Setting up encryption keys...
[App] ✅ Encrypted database initialized
 * Running on http://127.0.0.1:5000
```

**Keep this terminal open!**

---

### Step 4: Start Admin Panel (Terminal 2)

Open a **NEW terminal** (keep Flask running):

```cmd
cd "c:\Users\anshu\OneDrive\Desktop\5th sem\New folder\IS_project\admin_panel"
npm run dev
```

**Look for:**
```
  ➜  Local:   http://localhost:3000/
  ➜  ready in 500 ms
```

---

### Step 5: Login to Admin Panel

1. **Open browser:** http://localhost:3000
2. **Login:**
   - Username: `admin`
   - Password: `admin123`
3. **You're in!** 🎉

---

## 🎯 What to Test

### ✅ Dashboard
- View statistics cards
- Check threat trends graph
- See recent activity

### ✅ Reports Page
- Click "Decrypt" on any report
- View decrypted URL and metadata
- Check blockchain hash info
- Try export button

### ✅ Whitelist
- Click "Add Domain"
- Enter: `example.com`
- Reason: `Testing`
- Click "Add Domain" button
- See it appear in table
- Click trash icon to remove

### ✅ Audit Logs
- View all logged actions
- Filter by action type
- Export audit trail

---

## 🧪 Add Test Data (Optional)

To see reports in the admin panel:

```cmd
cd server
python test_system.py
```

This adds 3 encrypted phishing reports to test decryption.

---

## 🎨 UI Preview

### Login Page
- Modern gradient background
- Shield logo with primary color
- Clean input fields
- Password show/hide toggle

### Dashboard
- 4 colorful stat cards
- Line chart for 7-day trends
- Bar chart for top threats
- Recent activity timeline

### Reports
- Encrypted reports list
- Lock icons for encrypted data
- Unlock icons after decrypt
- Detailed threat information

### Whitelist
- Clean table layout
- Add domain modal
- Search functionality
- Delete confirmation

### Audit Logs
- Colored action badges
- Emoji icons
- Timestamp tracking
- IP address logging

---

## 🔒 Security Features Active

✅ **AES-256-GCM** - Data encryption  
✅ **RSA-2048** - Key exchange  
✅ **SHA-256** - Digital signatures  
✅ **BCrypt** - Password hashing  
✅ **JWT** - Token authentication  
✅ **Blockchain** - Hash chain linking  

---

## 🐛 Common Issues

### "Module not found" Error
```cmd
cd admin_panel
npm install
```

### Port 3000 Already in Use
```cmd
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Then restart
npm run dev
```

### Port 5000 Already in Use
```cmd
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Then restart
python app.py
```

### "Invalid credentials" on Login
```cmd
# Recreate admin user
cd server
python setup_admin.py
```

### No Reports to Decrypt
```cmd
# Add test data
cd server
python test_system.py
```

### CORS Errors in Browser
- Make sure Flask is running
- Check `flask-cors` is installed
- Restart Flask server

---

## 📊 Testing Checklist

Use this to verify everything works:

- [ ] Step 1: Admin user created successfully
- [ ] Step 2: npm install completed without errors
- [ ] Step 3: Flask server running on port 5000
- [ ] Step 4: Vite dev server running on port 3000
- [ ] Step 5: Login page loads in browser
- [ ] Login with credentials works
- [ ] Redirected to dashboard
- [ ] Dashboard shows statistics
- [ ] Reports page loads
- [ ] Can decrypt a report
- [ ] Whitelist page loads
- [ ] Can add a domain to whitelist
- [ ] Can remove domain from whitelist
- [ ] Audit logs page loads
- [ ] Logs show login action
- [ ] Can filter logs by action
- [ ] Logout works
- [ ] Redirected to login page

---

## 🎉 Success!

If all checks pass, Phase 3 is complete! You now have:

1. ✅ **Encrypted Database** (Phase 1-2)
2. ✅ **Admin Panel UI** (Phase 3)
3. ✅ **Authentication System** (Phase 3)
4. ✅ **Complete CRUD Operations** (Phase 3)

---

## 📝 Next Steps (Optional Enhancements)

- [ ] Add user management page
- [ ] Implement role-based access (admin/viewer)
- [ ] Add real-time notifications
- [ ] Implement dark mode
- [ ] Add bulk report operations
- [ ] Create API documentation
- [ ] Add unit tests
- [ ] Deploy to production

---

**Need help?** Check:
- Browser console (F12) for frontend errors
- Flask terminal for backend errors
- Network tab for API request failures

**Ready to test?** Follow the checklist above! 🚀
