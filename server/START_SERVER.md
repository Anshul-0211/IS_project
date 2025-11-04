# 🚀 Starting the Flask Server

## Option 1: Command Line (Recommended)

1. **Open Command Prompt**
2. **Navigate to server directory:**
   ```cmd
   cd "c:\Users\anshu\OneDrive\Desktop\5th sem\New folder\IS_project\server"
   ```

3. **Run the server:**
   ```cmd
   python app.py
   ```

4. **Look for these startup messages:**
   ```
   [App] 🔐 Setting up encryption keys...
   [App] ✅ Encrypted database initialized
   [App] 🚀 Server starting on http://127.0.0.1:5000
   ```

## Option 2: VS Code Terminal

1. **Open VS Code Terminal** (Ctrl + `)
2. **Change directory:**
   ```cmd
   cd server
   ```
3. **Run:**
   ```cmd
   python app.py
   ```

## ✅ Server is Running When You See:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

## 🧪 Testing the Server

### Test 1: Check Server is Alive
Open browser: http://127.0.0.1:5000

### Test 2: Try the Extension
1. Reload extension in Chrome (chrome://extensions/)
2. Visit a phishing site (e.g., http://clod.co/)
3. Watch server console for:
   ```
   [Database] 📝 Storing encrypted phishing report...
   [Database] ✅ Report stored with ID: 1
   ```

### Test 3: Verify Encrypted Storage
In Python console:
```python
from database import PhishingDatabase
db = PhishingDatabase()
reports = db.get_all_reports(limit=5)
print(f"Total encrypted reports: {len(reports)}")

# Decrypt latest report
if reports:
    decrypted = db.decrypt_report(reports[0])
    print(f"URL: {decrypted['url']}")
    print(f"Probability: {decrypted['metadata']['probability']}")
```

## 🔧 Troubleshooting

### Port Already in Use
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Module Not Found
```cmd
pip install -r requirements.txt
```

### Database Errors
Delete old database and restart:
```cmd
del phishing_database.db
python app.py
```

## 📊 Monitoring Logs

Watch for these key messages:

**✅ Good Signs:**
- `[Database] ✅ Report stored with ID: X`
- `[App] URL classified as phishing (XX% confidence)`
- `[CryptoManager] ✅ Data encrypted successfully`

**⚠️ Warnings:**
- `[Database] ⚠️ URL already in database`
- `[App] ⚠️ URL is whitelisted, skipping storage`

**❌ Errors:**
- `[Database] ❌ Failed to store report`
- `[CryptoManager] ❌ Encryption failed`

## 🎯 What Should Happen

1. **Extension detects phishing site**
2. **Sends URL to Flask server** (`POST /classify`)
3. **ML model predicts probability**
4. **VirusTotal checks for reports**
5. **Data gets encrypted** (AES-256 + RSA-2048)
6. **Digital signature created** (RSA-PSS)
7. **Stored in blockchain database** (linked to previous block)
8. **Extension shows warning page**

## 🔐 Security Features Active

- ✅ RSA-2048 key exchange
- ✅ AES-256-GCM data encryption
- ✅ SHA-256 digital signatures
- ✅ Blockchain hash linking
- ✅ Tamper detection via signatures
- ✅ Audit logging for all operations

## 📁 Files to Monitor

- `phishing_database.db` - Encrypted reports (grows with each detection)
- `app.log` - Server logs (if logging enabled)
- `keys/*.pem` - Cryptographic keys (must be kept secure)

---

**Ready to start?** Run: `cd server && python app.py`
