# ✅ Phase 3 Testing Checklist

Use this checklist to verify that everything is working correctly.

---

## 📋 Pre-Testing Setup

### ✅ Step 1: Create Admin User
```cmd
cd server
python setup_admin.py
```

- [ ] Script runs without errors
- [ ] You entered username (e.g., `admin`)
- [ ] You entered password (e.g., `admin123`)
- [ ] You see: "✅ Admin user 'admin' created successfully!"

**If user already exists:** That's okay! You can use the existing credentials.

---

### ✅ Step 2: Install Dependencies
```cmd
cd ..\admin_panel
npm install
```

- [ ] npm install completes without errors
- [ ] You see: "added XXX packages"
- [ ] `node_modules` folder created

**If errors occur:** Delete `node_modules` and `package-lock.json`, then re-run.

---

### ✅ Step 3: Start Flask Server (Terminal 1)
```cmd
cd ..\server
python app.py
```

**Look for these messages:**
- [ ] `[App] 🔐 Setting up encryption keys...`
- [ ] `[App] ✅ Encrypted database initialized`
- [ ] `Running on http://127.0.0.1:5000`
- [ ] No error messages

**Keep this terminal open!**

---

### ✅ Step 4: Start React Dev Server (Terminal 2)
Open a **NEW** command prompt:
```cmd
cd "c:\Users\anshu\OneDrive\Desktop\5th sem\New folder\IS_project\admin_panel"
npm run dev
```

**Look for these messages:**
- [ ] `VITE v5.x.x ready in XXX ms`
- [ ] `➜ Local: http://localhost:3000/`
- [ ] No compilation errors

**Keep this terminal open too!**

---

## 🔐 Authentication Testing

### ✅ Step 5: Login Page
Open browser: **http://localhost:3000**

- [ ] Login page loads correctly
- [ ] Shield logo visible
- [ ] "Phishing Detection Admin" title visible
- [ ] Username and password fields visible
- [ ] "Sign In" button visible
- [ ] Security badge at bottom visible

---

### ✅ Step 6: Login with Valid Credentials
Enter:
- Username: `admin` (or your username)
- Password: `admin123` (or your password)

Click **"Sign In"**

- [ ] No error message appears
- [ ] Page redirects to `/dashboard`
- [ ] Sidebar appears on left
- [ ] "Dashboard" is highlighted in sidebar

---

### ✅ Step 7: Login with Invalid Credentials
Go back to login (click logout or go to http://localhost:3000/login)

Enter:
- Username: `admin`
- Password: `wrongpassword`

Click **"Sign In"**

- [ ] Error message appears: "Invalid credentials"
- [ ] Stays on login page
- [ ] No crash or freeze

---

## 📊 Dashboard Testing

### ✅ Step 8: Dashboard Display
You should be on `/dashboard` after successful login.

**Check these elements:**

#### Stat Cards (Top Row)
- [ ] "Total Threats" card visible
- [ ] "Today's Reports" card visible
- [ ] "Whitelisted" card visible
- [ ] "Database Size" card visible
- [ ] Numbers display (even if 0)

#### Charts (Middle Row)
- [ ] "7-Day Threat Trend" chart visible
- [ ] Line/Area chart renders
- [ ] "Top 5 Threat Domains" chart visible
- [ ] Bar chart renders

#### Security Status (Bottom Row)
- [ ] "Encryption Status" card shows "Active"
- [ ] "Blockchain Integrity" card shows "Verified"
- [ ] "Digital Signatures" card shows "Valid"

---

## 💾 Reports Page Testing

### ✅ Step 9: Navigate to Reports
Click **"Reports"** in the sidebar

- [ ] URL changes to `/reports`
- [ ] "Encrypted Reports" title visible
- [ ] Search bar visible
- [ ] "Export Data" button visible

---

### ✅ Step 10: Add Test Data (if no reports)
If you see "No reports found", add test data:

Open a **NEW** terminal:
```cmd
cd server
python test_system.py
```

- [ ] Script runs successfully
- [ ] "✅ Report added successfully" messages appear
- [ ] Refresh the Reports page in browser
- [ ] Now you see encrypted reports

---

### ✅ Step 11: Decrypt a Report
Find any report and click **"Decrypt"** button

**Should see:**
- [ ] Button shows "Decrypting..." with spinner
- [ ] After ~1 second, button changes to "Decrypted"
- [ ] URL appears (e.g., http://fake-paypal.com)
- [ ] Threat Probability shown (e.g., 95%)
- [ ] Detection Source shown (ML Model or VirusTotal)
- [ ] VirusTotal Reports count shown
- [ ] Block Hash displayed (truncated)
- [ ] Previous Hash displayed
- [ ] Signature status shown (Valid/Invalid)

---

### ✅ Step 12: Export Reports
Click **"Export Data"** button

- [ ] CSV file downloads
- [ ] File named: `phishing_reports_YYYY-MM-DD.csv`
- [ ] Open file - contains report data
- [ ] Columns: ID, Timestamp, Block Hash, Previous Hash

---

## 🛡️ Whitelist Testing

### ✅ Step 13: Navigate to Whitelist
Click **"Whitelist"** in sidebar

- [ ] URL changes to `/whitelist`
- [ ] "Whitelist Management" title visible
- [ ] Search bar visible
- [ ] "Add Domain" button visible
- [ ] Table visible (may be empty)

---

### ✅ Step 14: Add Domain to Whitelist
Click **"Add Domain"** button

**Modal should open:**
- [ ] "Add Domain to Whitelist" title
- [ ] Domain input field
- [ ] Reason textarea
- [ ] Cancel button
- [ ] Add Domain button

**Fill in:**
- Domain: `example.com`
- Reason: `Testing whitelist functionality`

Click **"Add Domain"**

**Should see:**
- [ ] Modal closes
- [ ] Table refreshes
- [ ] New domain appears in table
- [ ] Domain: example.com
- [ ] Reason: Testing whitelist functionality
- [ ] Added By: admin (your username)
- [ ] Date Added: Today's date

---

### ✅ Step 15: Search Whitelist
In search bar, type: `example`

- [ ] Table filters
- [ ] Only shows "example.com"
- [ ] Clear search - all domains show

---

### ✅ Step 16: Remove Domain
Click **trash icon** next to example.com

**Should see:**
- [ ] Confirmation dialog: "Are you sure..."
- [ ] Click OK
- [ ] Domain disappears from table
- [ ] Table refreshes

---

## 📝 Audit Logs Testing

### ✅ Step 17: Navigate to Audit Logs
Click **"Audit Logs"** in sidebar

- [ ] URL changes to `/audit`
- [ ] "Audit Logs" title visible
- [ ] Filter dropdown visible
- [ ] "Export Logs" button visible

**Check Stats Cards:**
- [ ] "Total Actions" shows number
- [ ] "Active Users" shows at least 1
- [ ] "Today's Activity" shows your actions

---

### ✅ Step 18: View Logs
Scroll through the activity timeline

**You should see entries for:**
- [ ] Login action (when you logged in)
- [ ] View report action (if you decrypted)
- [ ] Add whitelist action (if you added domain)
- [ ] Remove whitelist action (if you removed domain)

**Each log entry should show:**
- [ ] Colored badge with action type
- [ ] Username (admin)
- [ ] Timestamp
- [ ] Description
- [ ] IP address (usually 127.0.0.1)

---

### ✅ Step 19: Filter Logs
Click filter dropdown, select **"Login"**

- [ ] Only login actions shown
- [ ] Other actions hidden
- [ ] Change to "All Actions" - everything shows

---

### ✅ Step 20: Export Audit Logs
Click **"Export Logs"** button

- [ ] CSV file downloads
- [ ] File named: `audit_logs_YYYY-MM-DD.csv`
- [ ] Open file - contains log data
- [ ] Columns: ID, Username, Action, Timestamp, IP, Details

---

## 🚪 Logout Testing

### ✅ Step 21: Logout
Click **"Sign Out"** button in sidebar (bottom left)

- [ ] Redirects to `/login`
- [ ] Token removed from localStorage
- [ ] Cannot access `/dashboard` directly

Try going to: http://localhost:3000/dashboard

- [ ] Automatically redirects to `/login`
- [ ] Shows you're not authenticated

---

## 🔒 Security Testing

### ✅ Step 22: Token Expiry (Optional)
JWT tokens expire after 24 hours. To test immediately:

1. Open browser DevTools (F12)
2. Go to Application tab
3. Local Storage → http://localhost:3000
4. Delete `token` entry
5. Try to visit `/dashboard`

**Should see:**
- [ ] Redirects to `/login`
- [ ] Need to login again

---

### ✅ Step 23: API Protection (Optional)
Open DevTools → Network tab

1. Make any action (decrypt, add whitelist, etc.)
2. Find the API request (starts with /api/)
3. Click on it
4. Check Headers tab

**Should see:**
- [ ] Authorization header present
- [ ] Value: `Bearer <long_token>`

Now try the request without token:
- Delete token from localStorage
- Try to access /dashboard
- [ ] Gets 401 Unauthorized
- [ ] Redirects to login

---

## 📊 Performance Testing

### ✅ Step 24: Page Load Speed
Clear browser cache (Ctrl+Shift+Delete)

Reload each page and check DevTools → Network:

**Login Page:**
- [ ] Loads in under 2 seconds
- [ ] No console errors

**Dashboard:**
- [ ] Loads in under 3 seconds
- [ ] Charts render smoothly
- [ ] No console errors

**Reports:**
- [ ] Loads in under 2 seconds
- [ ] Decrypt takes under 1 second
- [ ] No console errors

**Whitelist:**
- [ ] Loads in under 2 seconds
- [ ] Modal opens instantly
- [ ] No console errors

**Audit Logs:**
- [ ] Loads in under 2 seconds
- [ ] Filters work instantly
- [ ] No console errors

---

## 🎨 UI/UX Testing

### ✅ Step 25: Responsive Design
Resize browser window to different sizes:

**Desktop (1920x1080):**
- [ ] Sidebar always visible
- [ ] Charts display properly
- [ ] Tables not truncated

**Tablet (768px):**
- [ ] Sidebar collapses
- [ ] Hamburger menu appears
- [ ] Cards stack vertically

**Mobile (375px):**
- [ ] All content readable
- [ ] Buttons accessible
- [ ] Forms usable

---

### ✅ Step 26: Dark Mode (Optional)
If implemented:
- [ ] Toggle switches theme
- [ ] Colors invert properly
- [ ] Text remains readable

---

## 🐛 Error Handling

### ✅ Step 27: Network Errors
Stop Flask server (Ctrl+C in Terminal 1)

Try to:
- Login → Should show connection error
- Decrypt report → Should show error
- Add whitelist → Should show error

**Should see:**
- [ ] User-friendly error messages
- [ ] No app crash
- [ ] Can still navigate

Restart Flask server:
```cmd
python app.py
```

- [ ] App recovers when server back
- [ ] Can login again

---

## ✅ Final Checklist

### All Systems Go? ✈️

- [ ] ✅ Admin user created
- [ ] ✅ Dependencies installed
- [ ] ✅ Flask server running
- [ ] ✅ React dev server running
- [ ] ✅ Login page loads
- [ ] ✅ Can login successfully
- [ ] ✅ Dashboard displays stats
- [ ] ✅ Charts render correctly
- [ ] ✅ Can decrypt reports
- [ ] ✅ Can export reports
- [ ] ✅ Can add to whitelist
- [ ] ✅ Can remove from whitelist
- [ ] ✅ Can search whitelist
- [ ] ✅ Audit logs display
- [ ] ✅ Can filter logs
- [ ] ✅ Can export logs
- [ ] ✅ Logout works
- [ ] ✅ Protected routes work
- [ ] ✅ No console errors
- [ ] ✅ No server errors

---

## 🎉 Success!

If all checkboxes are checked, **congratulations!** 🎊

Your Phase 3 Admin Panel is **fully functional** and ready to use!

---

## 📝 Issue Tracker

If something didn't work, note it here:

| Item | Issue | Solution |
|------|-------|----------|
| Example | Port 3000 in use | Kill process: `taskkill /PID xxx /F` |
|  |  |  |
|  |  |  |
|  |  |  |

---

## 🚀 Next Steps

Now that testing is complete:

1. **Take screenshots** of each page for documentation
2. **Create a demo video** showing the features
3. **Write a project report** explaining the architecture
4. **Deploy to production** (optional)
5. **Present your project** with confidence!

---

**Testing completed by:** _______________

**Date:** _______________

**Overall status:** ✅ PASS / ❌ FAIL

**Notes:**
