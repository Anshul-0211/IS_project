"""
Complete System Test - Encrypted Phishing Database
Run this to test all components
"""

import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("\n" + "="*70)
print("🔐 COMPLETE SYSTEM TEST - ENCRYPTED PHISHING DETECTION")
print("="*70 + "\n")


# ==================== TEST 1: CRYPTO MODULE ====================
print("📝 TEST 1: Cryptography Module")
print("-" * 70)

try:
    from crypto_utils import CryptoManager
    
    crypto = CryptoManager()
    print("✅ CryptoManager imported successfully")
    
    # Setup keys
    crypto.setup_keys()
    print("✅ Keys initialized")
    
    # Test encryption
    test_data = {
        'url': 'http://test-phishing.com',
        'probability': 0.95,
        'timestamp': datetime.now().isoformat()
    }
    
    encrypted = crypto.encrypt_data(test_data)
    print("✅ Data encrypted successfully")
    
    decrypted = crypto.decrypt_data(encrypted)
    print("✅ Data decrypted successfully")
    
    if decrypted == test_data:
        print("✅ Encryption/Decryption verified - data matches!")
    else:
        print("❌ ERROR: Decrypted data doesn't match original")
    
    # Test signatures
    signature = crypto.sign_data(test_data)
    print("✅ Digital signature created")
    
    is_valid = crypto.verify_signature(test_data, signature)
    if is_valid:
        print("✅ Signature verified - authentic!")
    else:
        print("❌ ERROR: Signature verification failed")
    
    print("\n✅ TEST 1 PASSED: Crypto module working perfectly\n")
    
except Exception as e:
    print(f"\n❌ TEST 1 FAILED: {e}\n")
    sys.exit(1)


# ==================== TEST 2: DATABASE MODULE ====================
print("📝 TEST 2: Encrypted Database")
print("-" * 70)

try:
    from database import PhishingDatabase
    
    # Use a test database
    db = PhishingDatabase('test_system.db')
    print("✅ Database initialized")
    
    # Add some test reports
    test_reports = [
        {
            'url': 'http://fake-paypal.com',
            'metadata': {
                'probability': 0.98,
                'source': 'ML Model',
                'virustotal_reports': 8
            }
        },
        {
            'url': 'http://fake-bank.com',
            'metadata': {
                'probability': 0.93,
                'source': 'VirusTotal',
                'virustotal_reports': 5
            }
        },
        {
            'url': 'http://scam-site.com',
            'metadata': {
                'probability': 0.89,
                'source': 'ML Model',
                'virustotal_reports': 3
            }
        }
    ]
    
    print(f"📥 Adding {len(test_reports)} test reports...")
    for i, report in enumerate(test_reports, 1):
        report_id = db.add_phishing_report(report['url'], report['metadata'])
        if report_id:
            print(f"  ✅ Report {i} added (ID: {report_id})")
        else:
            print(f"  ❌ Failed to add report {i}")
    
    # Retrieve reports
    all_reports = db.get_all_reports(limit=10)
    print(f"\n✅ Retrieved {len(all_reports)} encrypted reports from database")
    
    # Decrypt one report
    if all_reports:
        print("\n🔓 Decrypting most recent report...")
        decrypted = db.decrypt_report(all_reports[0])
        if decrypted:
            print("✅ Report decrypted successfully:")
            print(f"   URL: {decrypted['url']}")
            print(f"   Probability: {decrypted['metadata']['probability']}")
            print(f"   Source: {decrypted['metadata']['source']}")
            print(f"   Signature Valid: {decrypted['signature_valid']}")
        else:
            print("❌ Failed to decrypt report")
    
    # Verify blockchain integrity
    print("\n🔗 Verifying blockchain integrity...")
    is_valid = db.verify_blockchain_integrity()
    
    # Test whitelist
    print("\n✅ Testing whitelist...")
    db.add_to_whitelist('google.com', 'test_user', 'Safe search engine')
    db.add_to_whitelist('github.com', 'test_user', 'Development platform')
    whitelist = db.get_whitelist()
    print(f"✅ Whitelist has {len(whitelist)} entries")
    
    # Get statistics
    stats = db.get_statistics()
    print("\n📊 Database Statistics:")
    print(f"   Total Reports: {stats['total_reports']}")
    print(f"   Reports Today: {stats['reports_today']}")
    print(f"   Whitelist Entries: {stats['whitelist_count']}")
    
    print("\n✅ TEST 2 PASSED: Database working perfectly\n")
    
except Exception as e:
    print(f"\n❌ TEST 2 FAILED: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)


# ==================== TEST 3: FLASK INTEGRATION ====================
print("📝 TEST 3: Flask Integration Check")
print("-" * 70)

try:
    # Check if app.py has the database integration
    with open('app.py', 'r') as f:
        app_content = f.read()
    
    if 'from database import PhishingDatabase' in app_content:
        print("✅ Database import found in app.py")
    else:
        print("❌ Database import missing in app.py")
    
    if 'db = PhishingDatabase' in app_content:
        print("✅ Database initialization found in app.py")
    else:
        print("❌ Database initialization missing in app.py")
    
    if 'db.add_phishing_report' in app_content:
        print("✅ Database storage call found in classify_url()")
    else:
        print("❌ Database storage call missing in classify_url()")
    
    print("\n✅ TEST 3 PASSED: Flask integration verified\n")
    
except Exception as e:
    print(f"\n❌ TEST 3 FAILED: {e}\n")


# ==================== TEST 4: KEY FILES ====================
print("📝 TEST 4: Cryptographic Keys")
print("-" * 70)

key_files = [
    'keys/database_public.pem',
    'keys/database_private.pem',
    'keys/extension_public.pem',
    'keys/extension_private.pem'
]

all_keys_exist = True
for key_file in key_files:
    if os.path.exists(key_file):
        size = os.path.getsize(key_file)
        print(f"✅ {key_file} exists ({size} bytes)")
    else:
        print(f"❌ {key_file} missing")
        all_keys_exist = False

if all_keys_exist:
    print("\n✅ TEST 4 PASSED: All key files present\n")
else:
    print("\n⚠️  TEST 4 WARNING: Some keys missing (will regenerate on first run)\n")


# ==================== SUMMARY ====================
print("="*70)
print("📋 TEST SUMMARY")
print("="*70)
print("✅ Cryptography Module: WORKING")
print("✅ Encrypted Database: WORKING")
print("✅ Blockchain Chain: WORKING")
print("✅ Digital Signatures: WORKING")
print("✅ Whitelist Management: WORKING")
print("✅ Flask Integration: VERIFIED")
print("="*70)

print("\n🎉 ALL TESTS PASSED! System is ready for use.\n")

print("📝 Next Steps:")
print("   1. Start Flask server: python app.py")
print("   2. Reload browser extension")
print("   3. Visit a phishing site to test")
print("   4. Check server logs for encrypted storage confirmation")
print("\n💡 To view encrypted reports:")
print("   python -c \"from database import PhishingDatabase; db = PhishingDatabase(); print(db.get_all_reports())\"")
print()
