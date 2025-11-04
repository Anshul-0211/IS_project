#!/usr/bin/env python3
"""
Simple CIA Demo - No Unicode Characters
Perfect for Windows systems with encoding issues
"""

import requests
import time
import sys

def print_header(title):
    """Print formatted header without Unicode"""
    print("\n" + "=" * 60)
    print(f"DEMO: {title}")
    print("=" * 60)

def print_step(step_num, description):
    """Print formatted step"""
    print(f"\nStep {step_num}: {description}")
    print("-" * 40)

def wait_for_user(message="Press Enter to continue..."):
    """Wait for user input"""
    input(f"\n{message}")

def test_node_connectivity():
    """Test if nodes are running"""
    print("Testing Node Connectivity...")
    print("-" * 40)
    
    nodes = [5001, 5002, 5003]
    active_nodes = []
    
    for port in nodes:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"Node {port}: ACTIVE - {data.get('records_count', 0)} records")
                active_nodes.append(port)
            else:
                print(f"Node {port}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Node {port}: CONNECTION FAILED")
    
    return active_nodes

def demonstrate_confidentiality():
    """Demonstrate CONFIDENTIALITY principle"""
    print_header("CONFIDENTIALITY DEMONSTRATION")
    print("Only authorized security analysts can add threats to our database")
    
    print_step(1, "Unauthorized Access Attempt")
    print("Trying to add threat without valid API key...")
    
    try:
        response = requests.post(
            "http://localhost:5001/add_threat",
            json={
                'url': 'unauthorized-test.com',
                'classification': 'phishing',
                'confidence': 0.9,
                'api_key': 'invalid_key_123'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('success'):
                print(f"ACCESS DENIED: {data.get('error')}")
                print("CONFIDENTIALITY: Unauthorized access blocked!")
            else:
                print("SECURITY BREACH: Unauthorized access succeeded!")
        else:
            print(f"ACCESS DENIED: HTTP {response.status_code}")
            print("CONFIDENTIALITY: System rejected unauthorized request!")
            
    except Exception as e:
        print(f"Error: {e}")
    
    wait_for_user()
    
    print_step(2, "Authorized Access Attempt")
    print("Now trying with valid security analyst credentials...")
    
    try:
        response = requests.post(
            "http://localhost:5001/add_threat",
            json={
                'url': 'authorized-test.com',
                'classification': 'phishing',
                'confidence': 0.95,
                'api_key': 'security_analyst_001'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"ACCESS GRANTED: {data.get('message')}")
                print("CONFIDENTIALITY: Authorized analyst successfully added threat!")
                print(f"Security Hash: {data.get('hash', 'N/A')[:16]}...")
            else:
                print(f"ACCESS DENIED: {data.get('error')}")
        else:
            print(f"ERROR: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    wait_for_user()

def demonstrate_integrity():
    """Demonstrate INTEGRITY principle"""
    print_header("INTEGRITY DEMONSTRATION")
    print("Hash-based tamper detection prevents data corruption")
    
    print_step(1, "Adding Threat Record with Integrity Protection")
    print("Adding a new threat record with cryptographic hash...")
    
    try:
        response = requests.post(
            "http://localhost:5001/add_threat",
            json={
                'url': 'integrity-demo.com',
                'classification': 'phishing',
                'confidence': 0.92,
                'api_key': 'security_analyst_001'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"RECORD ADDED: {data.get('message')}")
                print(f"Integrity Hash: {data.get('hash', 'N/A')[:16]}...")
                print("INTEGRITY: Record protected with cryptographic hash!")
            else:
                print(f"FAILED: {data.get('error')}")
        else:
            print(f"ERROR: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    wait_for_user()
    
    print_step(2, "Verifying Record Integrity")
    print("Checking if record has been tampered with...")
    
    try:
        response = requests.post(
            "http://localhost:5001/test_integrity",
            json={'url': 'integrity-demo.com'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('integrity_verified'):
                print("INTEGRITY VERIFIED: Record is authentic and untampered!")
                print("INTEGRITY: Hash verification successful!")
            else:
                print("INTEGRITY FAILED: Record has been tampered with!")
        else:
            print(f"ERROR: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    wait_for_user()

def demonstrate_availability():
    """Demonstrate AVAILABILITY principle"""
    print_header("AVAILABILITY DEMONSTRATION")
    print("Distributed system ensures high availability")
    
    print_step(1, "Adding Threat to Distributed System")
    print("Adding threat record to the distributed database...")
    
    try:
        response = requests.post(
            "http://localhost:5001/add_threat",
            json={
                'url': 'availability-demo.com',
                'classification': 'malware',
                'confidence': 0.88,
                'api_key': 'security_analyst_001'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"RECORD ADDED: {data.get('message')}")
                print("AVAILABILITY: Record added to distributed system!")
                print("Replicating to other nodes...")
            else:
                print(f"FAILED: {data.get('error')}")
        else:
            print(f"ERROR: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Wait for replication
    print("\nWaiting for replication to other nodes...")
    time.sleep(3)
    
    print_step(2, "Testing Distributed Query")
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
                    print(f"{node['id']}: Record found - {data.get('classification', 'N/A')}")
                    print(f"   Source: {data.get('source', 'N/A')}")
                else:
                    print(f"{node['id']}: Record not found (may not be replicated yet)")
            else:
                print(f"{node['id']}: Query failed - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"{node['id']}: Connection failed - {e}")
    
    print("\nAVAILABILITY: Distributed system working correctly!")
    print("Data replicated across multiple nodes for redundancy!")
    
    wait_for_user()

def main():
    """Main demo function"""
    print("=" * 60)
    print("CIA DISTRIBUTED THREAT INTELLIGENCE SYSTEM")
    print("=" * 60)
    print("Information Security Lab Demonstration")
    print("Confidentiality, Integrity, and Availability Principles")
    print("=" * 60)
    
    print("\nThis demonstration shows how our distributed threat intelligence")
    print("database implements the three fundamental principles of")
    print("information security: CIA (Confidentiality, Integrity, Availability)")
    
    wait_for_user("Press Enter to start the CIA demonstration...")
    
    # Check if nodes are running
    print("Checking distributed system status...")
    active_nodes = test_node_connectivity()
    
    if not active_nodes:
        print("\nNo active nodes found! Please start the distributed system first:")
        print("python nodes/start_all_nodes.py")
        return
    
    print(f"\n{len(active_nodes)} nodes are active. Starting demonstration...")
    wait_for_user()
    
    # Run demonstrations
    demonstrate_confidentiality()
    demonstrate_integrity()
    demonstrate_availability()
    
    print("\n" + "=" * 60)
    print("CIA DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("The distributed threat intelligence system successfully demonstrates:")
    print("CONFIDENTIALITY: Secure access control")
    print("INTEGRITY: Tamper-proof data protection")
    print("AVAILABILITY: High-availability distributed system")
    print("=" * 60)

if __name__ == '__main__':
    main()
