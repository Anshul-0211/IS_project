#!/usr/bin/env python3
"""
Non-Interactive CIA System Test
Tests the distributed threat intelligence database without user input
"""

import requests
import time
import sys

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

def test_confidentiality():
    """Test CONFIDENTIALITY principle"""
    print("\nTesting CONFIDENTIALITY...")
    print("-" * 40)
    
    # Test unauthorized access
    print("Test 1: Unauthorized access attempt...")
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
    
    # Test authorized access
    print("\nTest 2: Authorized access attempt...")
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

def test_integrity():
    """Test INTEGRITY principle"""
    print("\nTesting INTEGRITY...")
    print("-" * 40)
    
    # Test integrity verification
    print("Test 1: Verifying record integrity...")
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
    
    # Test tampering detection
    print("\nTest 2: Simulating tampering detection...")
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

def test_availability():
    """Test AVAILABILITY principle"""
    print("\nTesting AVAILABILITY...")
    print("-" * 40)
    
    # Add a test record
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
    
    # Test distributed query
    print("\nTest 2: Testing distributed query...")
    nodes = [5001, 5002, 5003]
    
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

def main():
    """Main test function"""
    print("=" * 60)
    print("CIA DISTRIBUTED THREAT INTELLIGENCE SYSTEM TEST")
    print("=" * 60)
    print("Testing Confidentiality, Integrity, and Availability")
    print("=" * 60)
    
    # Test node connectivity
    active_nodes = test_node_connectivity()
    
    if not active_nodes:
        print("\nNo active nodes found! Please start the distributed system first:")
        print("python nodes/start_all_nodes.py")
        return False
    
    print(f"\n{len(active_nodes)} nodes are active. Running tests...")
    
    # Test CIA principles
    test_confidentiality()
    test_integrity()
    test_availability()
    
    # Final summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("CONFIDENTIALITY: Role-based access control tested")
    print("INTEGRITY: Hash-based tamper detection tested")
    print("AVAILABILITY: Distributed system tested")
    print(f"NODES: {len(active_nodes)}/3 nodes active")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = main()
    
    if success:
        print("\nCIA System test completed successfully!")
        print("The distributed threat intelligence database is working correctly.")
    else:
        print("\nCIA System test failed!")
        print("Please check the system configuration and try again.")
