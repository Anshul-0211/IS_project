# 🛡️ Admin Panel - Phishing Detection System

Modern React-based admin panel for managing encrypted phishing threat database with blockchain-like storage.

## 🎨 Features

### ✅ Completed
- **🔐 Authentication**
  - JWT-based login system
  - BCrypt password hashing
  - Secure session management
  - Protected routes

- **📊 Dashboard**
  - Real-time statistics
  - 7-day threat trends (Line/Area charts)
  - Top 5 threat domains (Bar charts)
  - Recent activity feed
  - Security status indicators

- **💾 Database Viewer**
  - View encrypted reports
  - One-click decrypt functionality
  - Detailed threat information
  - Blockchain hash verification
  - Digital signature validation
  - Search and filter
  - Export to CSV

- **🛡️ Whitelist Management**
  - Add/remove trusted domains
  - Search functionality
  - Bulk operations
  - Domain validation
  - Reason tracking

- **📝 Audit Logs**
  - Complete activity tracking
  - Filter by action type
  - User activity monitoring
  - IP address logging
  - Export audit trail

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+
- Flask server running on port 5000

### Installation

1. **Install Dependencies**
   ```cmd
   cd admin_panel
   npm install
   ```

2. **Create Admin User**
   ```cmd
   cd ..\server
   python setup_admin.py
   ```
   Follow the prompts to create your admin credentials.

3. **Start Flask Server**
   ```cmd
   python app.py
   ```
   Server should be running on http://localhost:5000

4. **Start Admin Panel**
   ```cmd
   cd ..\admin_panel
   npm run dev
   ```
   Panel will open at http://localhost:3000

## 🔑 First Login

1. Open http://localhost:3000
2. Enter credentials created during setup
3. You'll be redirected to the Dashboard

**Default credentials (if using quick setup):**
- Username: `admin`
- Password: `admin123` (Change immediately!)

## 📱 UI Components

### Login Page
- Modern glassmorphism design
- Form validation
- Password visibility toggle
- Error handling
- Security badges

### Dashboard
- 4 stat cards (threats, today, whitelist, DB size)
- Interactive Recharts graphs
- Recent activity timeline
- Security status indicators

### Reports Page
- Encrypted reports list
- Decrypt button per report
- Detailed threat metrics
- Blockchain verification status
- Export functionality

### Whitelist Page
- Domain table with actions
- Add domain modal
- Search functionality
- Statistics card

### Audit Logs
- Filterable activity timeline
- Action type badges
- User/IP tracking
- Export to CSV

## 🔒 Security Features

### Encryption
- **AES-256-GCM**: Symmetric encryption for data
- **RSA-2048**: Asymmetric encryption for keys
- **SHA-256**: Digital signatures
- **BCrypt**: Password hashing (12 rounds)

### Authentication
- **JWT tokens**: 24-hour expiry
- **Bearer tokens**: Authorization header
- **Protected routes**: All API endpoints secured

### Blockchain
- **Hash linking**: Each record linked to previous
- **Tamper detection**: Signature verification
- **Integrity checks**: Complete chain validation

## 🛠️ Tech Stack

### Frontend
- **React 18**: UI library
- **Vite**: Build tool
- **React Router**: Navigation
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **Recharts**: Data visualization
- **Lucide React**: Icons

### Backend
- **Flask**: Web framework
- **PyJWT**: Token generation
- **BCrypt**: Password hashing
- **SQLite**: Database
- **Cryptography**: Encryption library

## 📂 Project Structure

```
admin_panel/
├── public/
├── src/
│   ├── components/
│   │   ├── Layout.jsx          # Main layout with sidebar
│   │   └── ProtectedRoute.jsx  # Auth guard
│   ├── context/
│   │   └── AuthContext.jsx     # Auth state management
│   ├── pages/
│   │   ├── Login.jsx           # Login page
│   │   ├── Dashboard.jsx       # Dashboard with stats
│   │   ├── Reports.jsx         # Database viewer
│   │   ├── Whitelist.jsx       # Whitelist management
│   │   └── AuditLogs.jsx       # Audit trail
│   ├── utils/
│   │   └── api.js              # API client
│   ├── App.jsx                 # Root component
│   ├── main.jsx                # Entry point
│   └── index.css               # Tailwind styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/register` - Register new user

### Reports
- `GET /api/reports` - Get all reports (encrypted)
- `GET /api/reports/:id` - Get single report
- `POST /api/reports/:id/decrypt` - Decrypt report
- `GET /api/reports/export` - Export as CSV

### Whitelist
- `GET /api/whitelist` - Get whitelist
- `POST /api/whitelist` - Add domain
- `DELETE /api/whitelist/:domain` - Remove domain
- `GET /api/whitelist/check/:domain` - Check if whitelisted

### Statistics
- `GET /api/stats/overview` - Get overview stats
- `GET /api/stats/trends` - Get trend data
- `GET /api/stats/top-threats` - Get top threats

### Audit
- `GET /api/audit` - Get audit logs
- `GET /api/audit/export` - Export audit logs

## 🎨 Customization

### Colors
Edit `tailwind.config.js` to change the color scheme:
```js
theme: {
  extend: {
    colors: {
      primary: { /* your colors */ },
      danger: { /* your colors */ }
    }
  }
}
```

### Logo
Replace the Shield icon in `Layout.jsx` with your logo.

### API URL
Change `API_BASE_URL` in `src/utils/api.js` if Flask runs on different port.

## 🐛 Troubleshooting

### Port Already in Use
```cmd
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### CORS Errors
Ensure Flask has `flask-cors` installed and configured:
```python
from flask_cors import CORS
CORS(app)
```

### Token Expired
Tokens expire after 24 hours. Just log in again.

### Can't Decrypt Reports
- Check that RSA keys exist in `server/keys/`
- Ensure database has reports to decrypt
- Check browser console for errors

## 📊 Sample Data

To add sample phishing reports for testing:
```python
python test_system.py
```

This creates 3 test reports with encryption.

## 🔄 Development

### Hot Reload
Both Flask (debug=True) and Vite support hot reload. Changes reflect immediately.

### Build for Production
```cmd
npm run build
```
Creates optimized build in `dist/` folder.

### Environment Variables
Create `.env` file:
```env
VITE_API_URL=http://localhost:5000/api
```

## 🚢 Deployment

### Frontend
Deploy `dist/` folder to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3

### Backend
Deploy Flask app to:
- Heroku
- AWS EC2
- Azure App Service
- DigitalOcean

**Important**: Change `SECRET_KEY` in `app.py` for production!

## 📝 License

Part of the Phishing Detection System project.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📞 Support

For issues or questions, check:
- Browser console for errors
- Flask logs for API errors
- Network tab for request failures

---

**Built with ❤️ for Information Security**
