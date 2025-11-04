"""
Setup Script - Initialize Admin Panel
Creates default admin user and prepares the system
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from database import PhishingDatabase
import getpass

print("\n" + "="*70)
print("🔐 ADMIN PANEL SETUP - Phishing Detection System")
print("="*70 + "\n")

# Initialize database
print("📦 Initializing database...")
db = PhishingDatabase('phishing_database.db')
print("✅ Database initialized\n")

# Create default admin user
print("👤 Creating Admin User")
print("-" * 70)

username = input("Enter admin username [default: admin]: ").strip() or "admin"

while True:
    password = getpass.getpass("Enter admin password: ")
    if len(password) < 6:
        print("❌ Password must be at least 6 characters long")
        continue
    
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print("❌ Passwords don't match. Try again.")
        continue
    
    break

email = input("Enter admin email (optional): ").strip()

# Create user
print("\n🔐 Creating user...")
success = db.create_user(username, password, email, role='admin')

if success:
    print(f"\n✅ Admin user '{username}' created successfully!")
    print("\n" + "="*70)
    print("🎉 SETUP COMPLETE!")
    print("="*70)
    print("\n📝 Next Steps:")
    print("   1. Start Flask server: python app.py")
    print("   2. Start React admin panel: cd ../admin_panel && npm install && npm run dev")
    print("   3. Open browser: http://localhost:3000")
    print(f"   4. Login with username: {username}")
    print("\n🔒 Security Features Active:")
    print("   ✅ AES-256-GCM encryption")
    print("   ✅ RSA-2048 key exchange")
    print("   ✅ SHA-256 digital signatures")
    print("   ✅ Blockchain hash linking")
    print("   ✅ JWT authentication")
    print("   ✅ BCrypt password hashing")
    print()
else:
    print(f"\n❌ Failed to create user. User '{username}' may already exist.")
    print("Try a different username or delete the database to start fresh.")
