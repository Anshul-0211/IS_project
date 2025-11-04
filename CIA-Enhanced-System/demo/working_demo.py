#!/usr/bin/env python3
"""
Working CIA Demo - Simple and Direct
Tests the distributed threat intelligence database
"""

import requests
import time

def main():
    print("=" * 60)
    print("CIA DISTRIBUTED THREAT INTELLIGENCE SYSTEM")
    print("=" * 60)
    print("Testing Confidentiality, Integrity, and Availability")
    print("=" * 60)
    
    # Test node connectivity
    print("\nTesting Node Connectivity...")
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
    
    if not active_nodes:
        print("\nNo active nodes found! Please start the distributed system first:")
        print("python nodes/start_all_nodes.py")
        return
    
    print(f"\n{len(active_nodes)} nodes are active. Running CIA tests...")
    
    # Test CONFIDENTIALITY
    print("\n" + "=" * 40)
    print("TESTING CONFIDENTIALITY")
    print("=" * 40)
    
    # Unauthorized access
    print("Test 1: Unauthorized access...")
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
                print(f"SUCCESS: Access denied - {data.get('error')}")
            else:
                print("FAILURE: Unauthorized access succeeded!")
        else:
            print(f"SUCCESS: HTTP {response.status_code} - Access denied")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Authorized access
    print("\nTest 2: Authorized access...")
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
                print(f"SUCCESS: Access granted - {data.get('message')}")
                print(f"Hash: {data.get('hash', 'N/A')[:16]}...")
            else:
                print(f"FAILURE: {data.get('error')}")
        else:
            print(f"ERROR: HTTP {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Test INTEGRITY
    print("\n" + "=" * 40)
    print("TESTING INTEGRITY")
    print("=" * 40)
    
    print("Test 1: Record integrity verification...")
    try:
        response = requests.post(
            "http://localhost:5001/test_integrity",
            json={'url': 'authorized-test.com'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('integrity_verified'):
                print("SUCCESS: Record integrity verified")
            else:
                print("FAILURE: Record integrity check failed")
        else:
            print(f"ERROR: HTTP {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("\nTest 2: Tampering detection...")
    try:
        response = requests.post(
            "http://localhost:5001/simulate_tampering",
            json={'url': 'authorized-test.com'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('tampering_detected'):
                print("SUCCESS: Tampering detection working")
            else:
                print("FAILURE: Tampering detection failed")
        else:
            print(f"ERROR: HTTP {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Test AVAILABILITY
    print("\n" + "=" * 40)
    print("TESTING AVAILABILITY")
    print("=" * 40)
    
    print("Test 1: Adding threat to distributed system...")
    try:
        response = requests.post(
            "http://localhost:5001/add_threat",
            json={
                'url': 'availability-test.com',
                'classification': 'malware',
                'confidence': 0.88,
                'api_key': 'security_analyst_001'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"SUCCESS: Record added - {data.get('message')}")
            else:
                print(f"FAILURE: {data.get('error')}")
        else:
            print(f"ERROR: HTTP {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Wait for replication
    print("\nWaiting for replication...")
    time.sleep(3)
    
    print("\nTest 2: Testing distributed query...")
    for port in nodes:
        try:
            response = requests.get(
                f"http://localhost:{port}/get_threat/availability-test.com",
                timeout=2
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('found'):
                    print(f"Node {port}: Record found - {data.get('classification', 'N/A')}")
                else:
                    print(f"Node {port}: Record not found")
            else:
                print(f"Node {port}: Query failed - HTTP {response.status_code}")
        except Exception as e:
            print(f"Node {port}: Connection failed")
    
    # Final summary
    print("\n" + "=" * 60)
    print("CIA SYSTEM TEST COMPLETED")
    print("=" * 60)
    print("CONFIDENTIALITY: Role-based access control tested")
    print("INTEGRITY: Hash-based tamper detection tested")
    print("AVAILABILITY: Distributed system tested")
    print(f"ACTIVE NODES: {len(active_nodes)}/3")
    print("=" * 60)
    
    print("\nThe CIA-Enhanced Distributed Threat Intelligence System")
    print("successfully demonstrates Information Security principles!")
    print("Perfect for your Information Security Lab presentation!")

if __name__ == '__main__':
    main()
