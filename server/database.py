"""
Database Module for Secure Phishing Detection System
Implements blockchain-like storage with encryption
"""

import sqlite3
import json
from datetime import datetime
from crypto_utils import CryptoManager
import hashlib


class PhishingDatabase:
    """Secure database for storing encrypted phishing reports"""
    
    def __init__(self, db_path='phishing_database.db'):
        self.db_path = db_path
        self.crypto = CryptoManager()
        print(f"[Database] Initialized: {db_path}")
        self.init_database()
    
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    
    
    def init_database(self):
        """Initialize database tables"""
        print("[Database] Creating tables...")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Phishing Reports Table (Encrypted)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phishing_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                encrypted_url TEXT NOT NULL,
                encrypted_metadata TEXT NOT NULL,
                signature TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                reported_by TEXT DEFAULT 'extension',
                block_hash TEXT,
                previous_hash TEXT
            )
        ''')
        
        # Whitelist Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS whitelist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE NOT NULL,
                added_by TEXT NOT NULL,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                reason TEXT
            )
        ''')
        
        # Access Log (Audit Trail)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                success BOOLEAN,
                details TEXT
            )
        ''')
        
        # Authorized Users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'viewer',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        ''')
        
        # ==================== DATABASE MIGRATION ====================
        # Add email column to existing users table if it doesn't exist
        try:
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'email' not in columns:
                print("[Database] 🔄 Migrating: Adding email column to users table...")
                cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')
                print("[Database] ✅ Migration complete: email column added")
        except Exception as e:
            print(f"[Database] ⚠️  Migration check: {e}")
        
        conn.commit()
        conn.close()
        print("[Database] ✅ Tables created successfully")
    
    
    # ==================== PHISHING REPORTS ====================
    
    def add_phishing_report(self, url, metadata):
        """
        Add encrypted phishing report with blockchain-like linking
        
        Args:
            url: The phishing URL
            metadata: Dict with probability, source, virustotal_reports, etc.
        """
        print(f"[Database] Adding phishing report for: {url}")
        
        try:
            # Prepare data package
            data_package = {
                'url': url,
                'metadata': metadata,
                'timestamp': datetime.now().isoformat()
            }
            
            # Encrypt the URL separately (for indexing/searching)
            encrypted_url = self.crypto.encrypt_data(url)
            
            # Encrypt metadata
            encrypted_metadata = self.crypto.encrypt_data(metadata)
            
            # Create digital signature
            signature = self.crypto.sign_data(data_package)
            
            # Get previous block hash for blockchain linking
            previous_hash = self.get_last_block_hash()
            
            # Create current block hash
            block_data = {
                'encrypted_url': encrypted_url,
                'encrypted_metadata': encrypted_metadata,
                'timestamp': datetime.now().isoformat(),
                'previous_hash': previous_hash
            }
            block_hash = self.crypto.hash_data(block_data)
            
            # Insert into database
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO phishing_reports 
                (encrypted_url, encrypted_metadata, signature, block_hash, previous_hash)
                VALUES (?, ?, ?, ?, ?)
            ''', (encrypted_url, encrypted_metadata, signature, block_hash, previous_hash))
            
            report_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"[Database] ✅ Report added successfully (ID: {report_id})")
            print(f"[Database] Block hash: {block_hash[:32]}...")
            
            return report_id
            
        except Exception as e:
            print(f"[Database] ❌ Error adding report: {e}")
            return None
    
    
    def get_last_block_hash(self):
        """Get the hash of the last block for blockchain linking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT block_hash FROM phishing_reports 
            ORDER BY id DESC LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result['block_hash']
        else:
            # Genesis block
            return '0' * 64
    
    
    def get_all_reports(self, limit=100, offset=0):
        """Get all encrypted phishing reports with pagination"""
        print(f"[Database] Fetching reports (limit: {limit}, offset: {offset})...")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM phishing_reports 
            ORDER BY id DESC LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        reports = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        print(f"[Database] ✅ Found {len(reports)} reports")
        return reports
    
    
    def get_report_by_id(self, report_id):
        """Get a specific report by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM phishing_reports WHERE id = ?
        ''', (report_id,))
        
        report = cursor.fetchone()
        conn.close()
        
        if report:
            return dict(report)
        return None
    
    
    def decrypt_report(self, report):
        """Decrypt an encrypted phishing report"""
        print(f"[Database] Decrypting report ID: {report['id']}")
        
        try:
            # Decrypt URL
            decrypted_url = self.crypto.decrypt_data(report['encrypted_url'])
            
            # Decrypt metadata
            decrypted_metadata = self.crypto.decrypt_data(report['encrypted_metadata'])
            
            # Verify signature
            data_package = {
                'url': decrypted_url,
                'metadata': decrypted_metadata,
                'timestamp': report['timestamp']
            }
            
            is_valid = self.crypto.verify_signature(
                data_package,
                report['signature']
            )
            
            result = {
                'id': report['id'],
                'url': decrypted_url,
                'metadata': decrypted_metadata,
                'timestamp': report['timestamp'],
                'signature_valid': is_valid,
                'block_hash': report['block_hash'],
                'previous_hash': report['previous_hash']
            }
            
            print(f"[Database] ✅ Report decrypted (Signature valid: {is_valid})")
            return result
            
        except Exception as e:
            print(f"[Database] ❌ Error decrypting report: {e}")
            return None
    
    
    def verify_blockchain_integrity(self):
        """Verify the integrity of the blockchain"""
        print("[Database] 🔍 Verifying blockchain integrity...")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, block_hash, previous_hash, encrypted_url, 
                   encrypted_metadata, timestamp
            FROM phishing_reports 
            ORDER BY id ASC
        ''')
        
        reports = cursor.fetchall()
        conn.close()
        
        if not reports:
            print("[Database] ℹ️  No reports to verify")
            return True
        
        # Verify each block
        previous_hash = '0' * 64  # Genesis
        errors = []
        
        for report in reports:
            report = dict(report)
            
            # Check if previous hash matches
            if report['previous_hash'] != previous_hash:
                error = f"Block {report['id']}: Previous hash mismatch!"
                errors.append(error)
                print(f"[Database] ❌ {error}")
            
            # Recalculate block hash
            block_data = {
                'encrypted_url': report['encrypted_url'],
                'encrypted_metadata': report['encrypted_metadata'],
                'timestamp': report['timestamp'],
                'previous_hash': report['previous_hash']
            }
            calculated_hash = self.crypto.hash_data(block_data)
            
            if calculated_hash != report['block_hash']:
                error = f"Block {report['id']}: Hash mismatch (tampered)!"
                errors.append(error)
                print(f"[Database] ❌ {error}")
            
            previous_hash = report['block_hash']
        
        if errors:
            print(f"[Database] ❌ Blockchain verification FAILED: {len(errors)} errors")
            return False
        else:
            print(f"[Database] ✅ Blockchain integrity verified: All {len(reports)} blocks valid")
            return True
    
    
    # ==================== WHITELIST MANAGEMENT ====================
    
    def add_to_whitelist(self, domain, added_by, reason=''):
        """Add domain to whitelist"""
        print(f"[Database] Adding to whitelist: {domain}")
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO whitelist (domain, added_by, reason)
                VALUES (?, ?, ?)
            ''', (domain, added_by, reason))
            
            conn.commit()
            conn.close()
            
            print(f"[Database] ✅ Domain whitelisted")
            return True
            
        except sqlite3.IntegrityError:
            print(f"[Database] ⚠️  Domain already whitelisted")
            return False
        except Exception as e:
            print(f"[Database] ❌ Error adding to whitelist: {e}")
            return False
    
    
    def get_whitelist(self):
        """Get all whitelisted domains"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM whitelist ORDER BY added_at DESC
        ''')
        
        whitelist = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return whitelist
    
    
    def remove_from_whitelist(self, domain):
        """Remove domain from whitelist"""
        print(f"[Database] Removing from whitelist: {domain}")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM whitelist WHERE domain = ?
        ''', (domain,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted > 0:
            print(f"[Database] ✅ Domain removed from whitelist")
            return True
        else:
            print(f"[Database] ⚠️  Domain not found in whitelist")
            return False
    
    
    # ==================== ACCESS LOGGING ====================
    
    def log_access(self, username, action, method='', ip_address=None, action_type='', details=''):
        """Log access attempts for audit trail"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # If action_type is provided, use it; otherwise use action
        final_action = action_type if action_type else action
        
        cursor.execute('''
            INSERT INTO access_log 
            (username, action, success, ip_address, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, final_action, True, ip_address, details))
        
        conn.commit()
        conn.close()
    
    
    def get_access_logs(self, limit=100):
        """Get access logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM access_log 
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return logs
    
    
    def get_audit_logs(self, limit=100, offset=0):
        """Get audit logs with offset for pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, action, timestamp, ip_address, details
            FROM access_log 
            ORDER BY timestamp DESC LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        logs = cursor.fetchall()
        conn.close()
        
        return logs
    
    
    # ==================== USER MANAGEMENT ====================
    
    def create_user(self, username, password, email='', role='admin'):
        """Create a new user with hashed password"""
        import bcrypt
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Insert user with email
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, role)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, email, role))
            
            conn.commit()
            print(f"[Database] ✅ User '{username}' created successfully")
            return True
            
        except sqlite3.IntegrityError:
            print(f"[Database] ❌ User '{username}' already exists")
            return False
        except Exception as e:
            print(f"[Database] ❌ Error creating user: {e}")
            return False
        finally:
            conn.close()
    
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        import bcrypt
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, password_hash, email FROM users WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        password_hash = result['password_hash']
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            return {
                'username': result['username'],
                'email': result['email'] or ''
            }
        else:
            return None
    
    
    def get_all_users(self):
        """Get all users (excluding passwords)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, email, role, created_at, last_login 
            FROM users
        ''')
        
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return users

    
    
    # ==================== STATISTICS ====================
    
    def get_statistics(self):
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total reports
        cursor.execute('SELECT COUNT(*) as count FROM phishing_reports')
        total_reports = cursor.fetchone()['count']
        
        # Reports today
        cursor.execute('''
            SELECT COUNT(*) as count FROM phishing_reports 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        reports_today = cursor.fetchone()['count']
        
        # Whitelist count
        cursor.execute('SELECT COUNT(*) as count FROM whitelist')
        whitelist_count = cursor.fetchone()['count']
        
        # Total users
        cursor.execute('SELECT COUNT(*) as count FROM users')
        user_count = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_reports': total_reports,
            'reports_today': reports_today,
            'whitelist_count': whitelist_count,
            'user_count': user_count
        }


# ==================== TESTING ====================

def test_database():
    """Test database functionality"""
    print("\n" + "="*60)
    print("🧪 TESTING DATABASE MODULE")
    print("="*60 + "\n")
    
    # Initialize database
    db = PhishingDatabase('test_phishing.db')
    
    # Test adding reports
    print("\n📝 Adding test phishing reports...")
    
    test_reports = [
        {
            'url': 'http://phishing-site1.com',
            'metadata': {
                'probability': 0.95,
                'source': 'ML Model',
                'virustotal_reports': 5
            }
        },
        {
            'url': 'http://phishing-site2.com',
            'metadata': {
                'probability': 0.87,
                'source': 'VirusTotal',
                'virustotal_reports': 3
            }
        },
        {
            'url': 'http://phishing-site3.com',
            'metadata': {
                'probability': 0.92,
                'source': 'ML Model',
                'virustotal_reports': 7
            }
        }
    ]
    
    for report in test_reports:
        db.add_phishing_report(report['url'], report['metadata'])
    
    # Get all reports
    print("\n📊 Fetching all reports...")
    reports = db.get_all_reports()
    print(f"Found {len(reports)} encrypted reports")
    
    # Decrypt first report
    print("\n🔓 Decrypting first report...")
    decrypted = db.decrypt_report(reports[0])
    if decrypted:
        print(json.dumps(decrypted, indent=2))
    
    # Verify blockchain
    print("\n🔗 Verifying blockchain integrity...")
    is_valid = db.verify_blockchain_integrity()
    
    # Test whitelist
    print("\n✅ Testing whitelist...")
    db.add_to_whitelist('google.com', 'admin', 'Trusted site')
    db.add_to_whitelist('github.com', 'admin', 'Development platform')
    whitelist = db.get_whitelist()
    print(f"Whitelist has {len(whitelist)} entries")
    
    # Get statistics
    print("\n📈 Database statistics...")
    stats = db.get_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n" + "="*60)
    print("✅ DATABASE TESTS COMPLETE")
    print("="*60 + "\n")


if __name__ == '__main__':
    test_database()
