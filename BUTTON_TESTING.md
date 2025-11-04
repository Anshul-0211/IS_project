# 🧪 Testing Warning Page Buttons

## ✅ Changes Made

1. **"Go Back to Safety" button** - Now properly returns to previous page or Google
2. **"Continue Anyway" button** - Shows strong warning and allows navigation to blocked site
3. **Bypass mechanism** - If user clicks "Continue Anyway", they can visit the site (for 5 minutes)

---

## 🔄 Before Testing - RELOAD EXTENSION

1. Go to `chrome://extensions/`
2. Find "Website Phishing Detector"
3. Click the **RELOAD** button (🔄)

---

## 🧪 Test Steps

### Test 1: Go Back Button

1. **Start Flask server** (if not running):
   ```bash
   cd server
   python app.py
   ```

2. **Visit a test URL** that will be flagged (or temporarily remove a site from whitelist)

3. **When warning page appears**, click **"🏠 Go Back to Safety"**

4. **Expected Result:**
   - Should return to previous page
   - Or if no history, should go to Google.com

---

### Test 2: Continue Anyway Button

1. **Visit a flagged URL** (warning page appears)

2. Click **"⚠️ Continue Anyway"**

3. **Expected Result:**
   - Shows a STRONG confirmation dialog with warnings
   - Lists dangers: password theft, malware, financial data compromise

4. **Click "Cancel"** in the dialog
   - Should stay on warning page
   - URL should NOT load

5. **Click "Continue Anyway" again**, then **"OK"** in dialog

6. **Expected Result:**
   - Navigates to the blocked URL
   - URL loads successfully
   - Bypass is set for 5 minutes

---

### Test 3: Bypass Mechanism

1. After successfully bypassing a URL (Test 2)

2. **Navigate away** from that site

3. **Try to visit the SAME URL again** within 5 minutes

4. **Expected Result:**
   - URL loads directly WITHOUT warning page
   - Bypass is consumed (one-time use)

5. **Try to visit the URL a THIRD time**

6. **Expected Result:**
   - Warning page appears again (bypass expired)

---

## 🎯 Button Behavior Summary

| Button | Action | User Sees |
|--------|--------|-----------|
| **Go Back to Safety** | `window.history.back()` or redirect to Google | Returns to previous page |
| **Continue Anyway** | Shows confirmation → Sets bypass → Navigates to URL | Confirmation dialog → Loads blocked site |

---

## 🐛 Troubleshooting

### Buttons Don't Respond
1. **Check browser console:**
   - Press F12 on warning page
   - Check Console tab for errors

2. **Check if clicking registers:**
   - Should see console.log messages:
     - "Go Back button clicked"
     - "Continue Anyway button clicked"

### "Continue Anyway" Shows "URL is unknown"
1. **Check URL is being passed:**
   - Look at the URL box on warning page
   - Should show actual URL, not "Unknown URL"

2. **Check URL parameters:**
   - Warning page URL should have `?url=...` parameter
   - Example: `chrome-extension://abc123/warning.html?url=https%3A%2F%2Fexample.com`

### Go Back Doesn't Work
1. **If no navigation history exists:**
   - Will redirect to Google.com instead
   - This is expected behavior

---

## 📋 Console Messages to Look For

When testing, open Console (F12) and look for:

```
✅ Good Messages:
- "Blocked URL: https://example.com"
- "Go Back button clicked"
- "Continue Anyway button clicked"
- "User confirmed, navigating to: https://example.com"
- "[Bypass] Allowing previously bypassed URL: https://example.com"

❌ Error Messages:
- "Cannot continue - URL is unknown or invalid"
- Any red error messages
```

---

## 🔄 Testing Cycle

1. **Visit flagged URL** → Warning page appears
2. **Test "Go Back"** → Should return
3. **Visit again** → Warning page appears
4. **Test "Continue Anyway"** → Should navigate after confirmation
5. **Visit again immediately** → Should load directly (bypass active)
6. **Visit again after 1 minute** → Warning page appears (bypass consumed)

---

**Remember:** Always reload the extension before testing!

`chrome://extensions/` → Click reload 🔄
