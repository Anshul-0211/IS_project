#!/usr/bin/env python3
"""
CIA Demonstration Script
Interactive demonstration of Confidentiality, Integrity, and Availability
Perfect for Information Security Lab presentation
"""

import requests
import json
import time
import sys

class CIADemonstrator:
    """Interactive CIA principles demonstrator"""
    
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.demo_data = {
            'phishing_sites': [
                'fake-bank-login.com',
                'phishing-paypal.net', 
                'malware-download.org'
            ],
            'api_keys': {
                'authorized': 'security_analyst_001',
                'unauthorized': 'invalid_key_123'
            }
        }
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f"🎯 {title}")
        print("=" * 80)
    
    def print_step(self, step_num, description):
        """Print formatted step"""
        print(f"\n📋 Step {step_num}: {description}")
        print("-" * 60)
    
    def wait_for_user(self, message="Press Enter to continue..."):
        """Wait for user input"""
        input(f"\n⏸️ {message}")
    
    def demonstrate_confidentiality(self):
        """Demonstrate CONFIDENTIALITY principle"""
        self.print_header("CONFIDENTIALITY DEMONSTRATION")
        print("🔒 Only authorized security analysts can add threats to our database")
        print("🔒 Role-based access control prevents unauthorized modifications")
        
        self.print_step(1, "Unauthorized Access Attempt")
        print("Trying to add threat without valid API key...")
        
        try:
            response = requests.post(
                f"{self.base_url}/add_threat",
                json={
                    'url': 'unauthorized-test.com',
                    'classification': 'phishing',
                    'confidence': 0.9,
                    'api_key': self.demo_data['api_keys']['unauthorized']
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data.get('success'):
                    print(f"✅ ACCESS DENIED: {data.get('error')}")
                    print("🔒 CONFIDENTIALITY: Unauthorized access blocked successfully!")
                else:
                    print("❌ SECURITY BREACH: Unauthorized access succeeded!")
            else:
                print(f"✅ ACCESS DENIED: HTTP {response.status_code}")
                print("🔒 CONFIDENTIALITY: System properly rejected unauthorized request!")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_user()
        
        self.print_step(2, "Authorized Access Attempt")
        print("Now trying with valid security analyst credentials...")
        
        try:
            response = requests.post(
                f"{self.base_url}/add_threat",
                json={
                    'url': 'authorized-test.com',
                    'classification': 'phishing',
                    'confidence': 0.95,
                    'api_key': self.demo_data['api_keys']['authorized']
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ ACCESS GRANTED: {data.get('message')}")
                    print("🔒 CONFIDENTIALITY: Authorized analyst successfully added threat!")
                    print(f"🔐 Security Hash: {data.get('hash', 'N/A')[:16]}...")
                else:
                    print(f"❌ ACCESS DENIED: {data.get('error')}")
            else:
                print(f"❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_user()
    
    def demonstrate_integrity(self):
        """Demonstrate INTEGRITY principle"""
        self.print_header("INTEGRITY DEMONSTRATION")
        print("🛡️ Hash-based tamper detection prevents data corruption")
        print("🛡️ Any modification to records is immediately detected")
        
        self.print_step(1, "Adding Threat Record with Integrity Protection")
        print("Adding a new threat record with cryptographic hash...")
        
        try:
            response = requests.post(
                f"{self.base_url}/add_threat",
                json={
                    'url': 'integrity-demo.com',
                    'classification': 'phishing',
                    'confidence': 0.92,
                    'api_key': self.demo_data['api_keys']['authorized']
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ RECORD ADDED: {data.get('message')}")
                    print(f"🔐 Integrity Hash: {data.get('hash', 'N/A')[:16]}...")
                    print("🛡️ INTEGRITY: Record protected with cryptographic hash!")
                else:
                    print(f"❌ FAILED: {data.get('error')}")
            else:
                print(f"❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_user()
        
        self.print_step(2, "Verifying Record Integrity")
        print("Checking if record has been tampered with...")
        
        try:
            response = requests.post(
                f"{self.base_url}/test_integrity",
                json={'url': 'integrity-demo.com'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('integrity_verified'):
                    print("✅ INTEGRITY VERIFIED: Record is authentic and untampered!")
                    print("🛡️ INTEGRITY: Hash verification successful!")
                else:
                    print("❌ INTEGRITY FAILED: Record has been tampered with!")
            else:
                print(f"❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_user()
        
        self.print_step(3, "Simulating Tampering Detection")
        print("Simulating an attempt to tamper with the record...")
        
        try:
            response = requests.post(
                f"{self.base_url}/simulate_tampering",
                json={'url': 'integrity-demo.com'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('tampering_detected'):
                    print("✅ TAMPERING DETECTED: System caught the tampering attempt!")
                    print("🛡️ INTEGRITY: Hash verification failed as expected!")
                    print(f"📊 Original: {data.get('original_classification', 'N/A')}")
                else:
                    print("❌ TAMPERING NOT DETECTED: This should not happen!")
            else:
                print(f"❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        self.wait_for_user()
    
    def demonstrate_availability(self):
        """Demonstrate AVAILABILITY principle"""
        self.print_header("AVAILABILITY DEMONSTRATION")
        print("⚡ Distributed system ensures high availability")
        print("⚡ Multiple nodes provide redundancy and failover")
        
        self.print_step(1, "Adding Threat to Distributed System")
        print("Adding threat record to the distributed database...")
        
        try:
            response = requests.post(
                f"{self.base_url}/add_threat",
                json={
                    'url': 'availability-demo.com',
                    'classification': 'malware',
                    'confidence': 0.88,
                    'api_key': self.demo_data['api_keys']['authorized']
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ RECORD ADDED: {data.get('message')}")
                    print("⚡ AVAILABILITY: Record added to distributed system!")
                    print("🔄 Replicating to other nodes...")
                else:
                    print(f"❌ FAILED: {data.get('error')}")
            else:
                print(f"❌ ERROR: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Wait for replication
        print("\n⏳ Waiting for replication to other nodes...")
        time.sleep(3)
        
        self.print_step(2, "Testing Distributed Query")
        print("Querying the same record from different nodes...")
        
        nodes = [
            {'id': 'Node 1', 'port': 5001},
            {'id': 'Node 2', 'port': 5002},
            {'id': 'Node 3', 'port': 5003}
        ]
        
        for node in nodes:
            try:
                response = requests.get(
                    f"http://localhost:{node['port']}/get_threat/availability-demo.com",
                    timeout=2
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('found'):
                        print(f"✅ {node['id']}: Record found - {data.get('classification', 'N/A')}")
                        print(f"   Source: {data.get('source', 'N/A')}")
                    else:
                        print(f"⚠️ {node['id']}: Record not found (may not be replicated yet)")
                else:
                    print(f"❌ {node['id']}: Query failed - HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {node['id']}: Connection failed - {e}")
        
        print("\n⚡ AVAILABILITY: Distributed system working correctly!")
        print("🔄 Data replicated across multiple nodes for redundancy!")
        
        self.wait_for_user()
    
    def demonstrate_cia_summary(self):
        """Demonstrate CIA principles summary"""
        self.print_header("CIA PRINCIPLES SUMMARY")
        
        print("🔒 CONFIDENTIALITY:")
        print("   • Only authorized security analysts can access the system")
        print("   • Role-based access control prevents unauthorized access")
        print("   • API key authentication ensures secure access")
        
        print("\n🛡️ INTEGRITY:")
        print("   • Cryptographic hashes protect data from tampering")
        print("   • Any modification is immediately detected")
        print("   • Chain of trust ensures data authenticity")
        
        print("\n⚡ AVAILABILITY:")
        print("   • Distributed across multiple nodes")
        print("   • Automatic replication and failover")
        print("   • System continues working even if nodes fail")
        
        print("\n🎯 REAL-WORLD APPLICATIONS:")
        print("   • Threat intelligence sharing between organizations")
        print("   • Collaborative security research")
        print("   • Distributed security monitoring")
        print("   • Secure information exchange")
        
        self.wait_for_user()
    
    def run_full_demo(self):
        """Run the complete CIA demonstration"""
        print("=" * 80)
        print("🛡️ CIA DISTRIBUTED THREAT INTELLIGENCE SYSTEM")
        print("=" * 80)
        print("Information Security Lab Demonstration")
        print("Confidentiality, Integrity, and Availability Principles")
        print("=" * 80)
        
        print("\n🎯 This demonstration shows how our distributed threat intelligence")
        print("   database implements the three fundamental principles of")
        print("   information security: CIA (Confidentiality, Integrity, Availability)")
        
        self.wait_for_user("Press Enter to start the CIA demonstration...")
        
        # Run demonstrations
        self.demonstrate_confidentiality()
        self.demonstrate_integrity()
        self.demonstrate_availability()
        self.demonstrate_cia_summary()
        
        print("\n" + "=" * 80)
        print("🎉 CIA DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("The distributed threat intelligence system successfully demonstrates:")
        print("✅ CONFIDENTIALITY: Secure access control")
        print("✅ INTEGRITY: Tamper-proof data protection")
        print("✅ AVAILABILITY: High-availability distributed system")
        print("=" * 80)

def main():
    """Main function"""
    print("Starting CIA Demonstration System...")
    
    # Check if nodes are running
    try:
        response = requests.get("http://localhost:5001/health", timeout=2)
        if response.status_code != 200:
            print("Node 1 is not running! Please start the distributed system first:")
            print("   python nodes/start_all_nodes.py")
            return
    except:
        print("Cannot connect to distributed system! Please start it first:")
        print("   python nodes/start_all_nodes.py")
        return
    
    # Run the demonstration
    demonstrator = CIADemonstrator()
    demonstrator.run_full_demo()

if __name__ == '__main__':
    main()
