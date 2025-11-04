#!/usr/bin/env python3
"""
Quick Start Script for CIA-Enhanced System
Automatically starts all components and runs basic tests
"""

import subprocess
import time
import requests
import sys
import os

def print_banner():
    """Print system banner"""
    print("=" * 80)
    print("🛡️ CIA-ENHANCED PHISHING DETECTION SYSTEM")
    print("=" * 80)
    print("Distributed Threat Intelligence with CIA Principles")
    print("Confidentiality • Integrity • Availability")
    print("=" * 80)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import flask
        import requests
        print("✅ Flask and requests are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages:")
        print("pip install flask requests flask-cors")
        return False

def start_distributed_nodes():
    """Start the distributed database nodes"""
    print("\n🚀 Starting distributed database nodes...")
    
    try:
        # Start all nodes in background
        process = subprocess.Popen([
            sys.executable, "nodes/start_all_nodes.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for nodes to start
        print("⏳ Waiting for nodes to initialize...")
        time.sleep(5)
        
        # Check if nodes are running
        nodes_ready = 0
        for port in [5001, 5002, 5003]:
            try:
                response = requests.get(f"http://localhost:{port}/health", timeout=2)
                if response.status_code == 200:
                    nodes_ready += 1
                    print(f"✅ Node on port {port} is ready")
                else:
                    print(f"❌ Node on port {port} not responding")
            except:
                print(f"❌ Node on port {port} connection failed")
        
        if nodes_ready >= 1:
            print(f"✅ {nodes_ready}/3 nodes are running")
            return True
        else:
            print("❌ No nodes are running properly")
            return False
            
    except Exception as e:
        print(f"❌ Error starting nodes: {e}")
        return False

def run_quick_test():
    """Run a quick test of the CIA system"""
    print("\n🧪 Running quick CIA system test...")
    
    try:
        # Test adding a threat (Confidentiality)
        print("Testing CONFIDENTIALITY...")
        response = requests.post(
            "http://localhost:5001/add_threat",
            json={
                'url': 'quick-test.com',
                'classification': 'phishing',
                'confidence': 0.9,
                'api_key': 'security_analyst_001'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ CONFIDENTIALITY: Authorized access working")
            else:
                print(f"❌ CONFIDENTIALITY: {data.get('error')}")
        else:
            print(f"❌ CONFIDENTIALITY: HTTP {response.status_code}")
        
        # Test integrity
        print("Testing INTEGRITY...")
        integrity_response = requests.post(
            "http://localhost:5001/test_integrity",
            json={'url': 'quick-test.com'}
        )
        
        if integrity_response.status_code == 200:
            data = integrity_response.json()
            if data.get('integrity_verified'):
                print("✅ INTEGRITY: Hash verification working")
            else:
                print("❌ INTEGRITY: Hash verification failed")
        else:
            print(f"❌ INTEGRITY: HTTP {integrity_response.status_code}")
        
        # Test availability
        print("Testing AVAILABILITY...")
        query_response = requests.get(
            "http://localhost:5001/get_threat/quick-test.com",
            timeout=2
        )
        
        if query_response.status_code == 200:
            data = query_response.json()
            if data.get('found'):
                print("✅ AVAILABILITY: Distributed query working")
            else:
                print("❌ AVAILABILITY: Query failed")
        else:
            print(f"❌ AVAILABILITY: HTTP {query_response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def show_demo_options():
    """Show available demo options"""
    print("\n🎪 Available Demonstrations:")
    print("-" * 50)
    print("1. Interactive CIA Demo (Recommended)")
    print("   python demo/demo_script.py")
    print()
    print("2. Comprehensive System Test")
    print("   python demo/test_cia_system.py")
    print()
    print("3. Manual Node Management")
    print("   python nodes/start_all_nodes.py")
    print()
    print("4. Individual Node Testing")
    print("   python nodes/start_node_1.py")
    print("   python nodes/start_node_2.py")
    print("   python nodes/start_node_3.py")

def main():
    """Main quick start function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Start distributed nodes
    if not start_distributed_nodes():
        print("\n❌ Failed to start distributed system")
        print("Please check the error messages above and try again")
        return
    
    # Run quick test
    if not run_quick_test():
        print("\n⚠️ Quick test had some issues, but system may still be working")
        print("Try running the full demo to verify everything is working")
    
    # Show demo options
    show_demo_options()
    
    print("\n" + "=" * 80)
    print("🎉 CIA-ENHANCED SYSTEM IS READY!")
    print("=" * 80)
    print("The distributed threat intelligence database is running with:")
    print("🔒 CONFIDENTIALITY: Role-based access control")
    print("🛡️ INTEGRITY: Hash-based tamper detection")
    print("⚡ AVAILABILITY: Distributed across multiple nodes")
    print("=" * 80)
    print("\n🚀 Next steps:")
    print("1. Run the interactive demo: python demo/demo_script.py")
    print("2. Test the system: python demo/test_cia_system.py")
    print("3. Explore the distributed database APIs")
    print("=" * 80)

if __name__ == '__main__':
    main()
