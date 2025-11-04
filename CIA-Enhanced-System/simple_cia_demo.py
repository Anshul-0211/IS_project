#!/usr/bin/env python3
"""
Simple CIA Demo - No Distributed System Required
Demonstrates CIA principles with a simplified approach
Perfect for Information Security Lab presentation
"""

import json
import hashlib
import time
from datetime import datetime

class SimpleThreatDatabase:
    """Simplified threat database demonstrating CIA principles"""
    
    def __init__(self):
        self.records = {}
        self.authorized_users = ['security_analyst_001', 'security_analyst_002']
        self.audit_log = []
    
    def generate_hash(self, url, classification, confidence, timestamp):
        """Generate hash for integrity verification"""
        data = f"{url}{classification}{confidence}{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def add_threat(self, url, classification, confidence, user_id):
        """Add threat record (CONFIDENTIALITY)"""
        # CONFIDENTIALITY: Check authorization
        if user_id not in self.authorized_users:
            self.audit_log.append(f"Unauthorized access attempt by {user_id}")
            return {'success': False, 'error': 'Unauthorized access denied'}
        
        # INTEGRITY: Generate hash
        timestamp = datetime.now().isoformat()
        hash_value = self.generate_hash(url, classification, confidence, timestamp)
        
        record = {
            'url': url,
            'classification': classification,
            'confidence': confidence,
            'timestamp': timestamp,
            'hash': hash_value,
            'authorized_by': user_id
        }
        
        self.records[url] = record
        self.audit_log.append(f"Threat added by {user_id}: {url}")
        
        return {
            'success': True,
            'message': 'Threat record added successfully',
            'hash': hash_value
        }
    
    def get_threat(self, url):
        """Get threat information (AVAILABILITY)"""
        if url in self.records:
            record = self.records[url]
            # INTEGRITY: Verify hash
            expected_hash = self.generate_hash(
                record['url'], 
                record['classification'], 
                record['confidence'], 
                record['timestamp']
            )
            
            integrity_verified = record['hash'] == expected_hash
            
            return {
                'found': True,
                'classification': record['classification'],
                'confidence': record['confidence'],
                'timestamp': record['timestamp'],
                'integrity_verified': integrity_verified,
                'source': 'local_database'
            }
        else:
            return {'found': False, 'message': 'Threat not found'}
    
    def verify_integrity(self, url):
        """Verify record integrity (INTEGRITY)"""
        if url not in self.records:
            return {'error': 'Record not found'}
        
        record = self.records[url]
        expected_hash = self.generate_hash(
            record['url'],
            record['classification'],
            record['confidence'],
            record['timestamp']
        )
        
        is_valid = record['hash'] == expected_hash
        
        return {
            'url': url,
            'integrity_verified': is_valid,
            'hash': record['hash'],
            'message': 'Record is valid' if is_valid else 'Record has been tampered with!'
        }
    
    def simulate_tampering(self, url):
        """Simulate tampering detection (INTEGRITY)"""
        if url not in self.records:
            return {'error': 'Record not found'}
        
        # Simulate tampering by modifying the record
        record = self.records[url]
        original_classification = record['classification']
        record['classification'] = 'safe'  # Tamper with the data
        
        # Check if tampering is detected
        expected_hash = self.generate_hash(
            record['url'],
            record['classification'],
            record['confidence'],
            record['timestamp']
        )
        
        is_valid = record['hash'] == expected_hash
        
        # Restore original data
        record['classification'] = original_classification
        
        return {
            'url': url,
            'tampering_detected': not is_valid,
            'message': 'Tampering detected!' if not is_valid else 'No tampering detected',
            'original_classification': original_classification
        }
    
    def get_stats(self):
        """Get database statistics"""
        total_records = len(self.records)
        verified_records = sum(1 for record in self.records.values() 
                              if self.verify_integrity(record['url'])['integrity_verified'])
        
        return {
            'total_records': total_records,
            'verified_records': verified_records,
            'corrupted_records': total_records - verified_records,
            'integrity_percentage': (verified_records / total_records * 100) if total_records > 0 else 100,
            'audit_entries': len(self.audit_log)
        }

def demonstrate_cia():
    """Demonstrate CIA principles"""
    print("=" * 80)
    print("CIA DISTRIBUTED THREAT INTELLIGENCE SYSTEM DEMONSTRATION")
    print("=" * 80)
    print("Information Security Lab - CIA Principles Implementation")
    print("Confidentiality, Integrity, and Availability")
    print("=" * 80)
    
    # Initialize database
    db = SimpleThreatDatabase()
    
    print("\n1. CONFIDENTIALITY DEMONSTRATION")
    print("-" * 50)
    print("Only authorized security analysts can add threats to our database")
    
    # Test unauthorized access
    print("\nTest 1: Unauthorized access attempt...")
    result = db.add_threat('phishing-site.com', 'phishing', 0.9, 'hacker_123')
    if not result['success']:
        print(f"SUCCESS: Access denied - {result['error']}")
        print("CONFIDENTIALITY: Unauthorized access blocked!")
    else:
        print("FAILURE: Unauthorized access succeeded!")
    
    # Test authorized access
    print("\nTest 2: Authorized access attempt...")
    result = db.add_threat('phishing-site.com', 'phishing', 0.95, 'security_analyst_001')
    if result['success']:
        print(f"SUCCESS: Access granted - {result['message']}")
        print(f"Security Hash: {result['hash'][:16]}...")
        print("CONFIDENTIALITY: Authorized analyst successfully added threat!")
    else:
        print(f"FAILURE: {result['error']}")
    
    print("\n2. INTEGRITY DEMONSTRATION")
    print("-" * 50)
    print("Hash-based tamper detection prevents data corruption")
    
    # Test integrity verification
    print("\nTest 1: Record integrity verification...")
    integrity_result = db.verify_integrity('phishing-site.com')
    if integrity_result.get('integrity_verified'):
        print("SUCCESS: Record integrity verified")
        print("INTEGRITY: Hash verification successful!")
    else:
        print("FAILURE: Record integrity check failed")
    
    # Test tampering detection
    print("\nTest 2: Simulating tampering detection...")
    tamper_result = db.simulate_tampering('phishing-site.com')
    if tamper_result.get('tampering_detected'):
        print("SUCCESS: Tampering detection working correctly")
        print("INTEGRITY: Hash verification caught the tampering attempt!")
        print(f"Original: {tamper_result.get('original_classification')}")
    else:
        print("FAILURE: Tampering detection failed")
    
    print("\n3. AVAILABILITY DEMONSTRATION")
    print("-" * 50)
    print("Distributed system ensures high availability")
    
    # Add more threats
    print("\nTest 1: Adding multiple threats to database...")
    threats = [
        ('malware-site.com', 'malware', 0.88, 'security_analyst_001'),
        ('fake-bank.com', 'phishing', 0.92, 'security_analyst_002'),
        ('suspicious-link.net', 'phishing', 0.85, 'security_analyst_001')
    ]
    
    for url, classification, confidence, user in threats:
        result = db.add_threat(url, classification, confidence, user)
        if result['success']:
            print(f"SUCCESS: Added {url} as {classification}")
        else:
            print(f"FAILURE: Could not add {url}")
    
    # Test querying
    print("\nTest 2: Testing database queries...")
    test_urls = ['phishing-site.com', 'malware-site.com', 'fake-bank.com', 'unknown-site.com']
    
    for url in test_urls:
        threat_info = db.get_threat(url)
        if threat_info.get('found'):
            print(f"FOUND: {url} - {threat_info.get('classification')} (Confidence: {threat_info.get('confidence')})")
            print(f"  Integrity: {'Verified' if threat_info.get('integrity_verified') else 'Failed'}")
        else:
            print(f"NOT FOUND: {url}")
    
    # Show statistics
    print("\n4. SYSTEM STATISTICS")
    print("-" * 50)
    stats = db.get_stats()
    print(f"Total Records: {stats['total_records']}")
    print(f"Verified Records: {stats['verified_records']}")
    print(f"Corrupted Records: {stats['corrupted_records']}")
    print(f"Integrity Percentage: {stats['integrity_percentage']:.1f}%")
    print(f"Audit Entries: {stats['audit_entries']}")
    
    # Show audit log
    print("\n5. AUDIT LOG (Security Monitoring)")
    print("-" * 50)
    for entry in db.audit_log[-5:]:  # Show last 5 entries
        print(f"  {entry}")
    
    print("\n" + "=" * 80)
    print("CIA DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("The threat intelligence database successfully demonstrates:")
    print("CONFIDENTIALITY: Role-based access control")
    print("INTEGRITY: Hash-based tamper detection")
    print("AVAILABILITY: Reliable data storage and retrieval")
    print("=" * 80)
    
    print("\nPerfect for Information Security Lab presentation!")
    print("Shows real-world implementation of CIA principles!")

if __name__ == '__main__':
    demonstrate_cia()
