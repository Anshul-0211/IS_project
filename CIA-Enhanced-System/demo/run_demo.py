#!/usr/bin/env python3
"""
One-Click Demo Runner for CIA-Enhanced System
Perfect for Information Security Lab presentations
"""

import subprocess
import time
import requests
import sys
import os

def print_banner():
    """Print demo banner"""
    print("=" * 80)
    print("🎓 INFORMATION SECURITY LAB DEMONSTRATION")
    print("=" * 80)
    print("🛡️ CIA-Enhanced Distributed Threat Intelligence System")
    print("Confidentiality • Integrity • Availability")
    print("=" * 80)

def check_system():
    """Check if system is ready"""
    print("🔍 Checking system status...")
    
    # Check if nodes are running
    nodes_ready = 0
    for port in [5001, 5002, 5003]:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                nodes_ready += 1
                print(f"✅ Node on port {port}: Ready")
            else:
                print(f"❌ Node on port {port}: Not responding")
        except:
            print(f"❌ Node on port {port}: Connection failed")
    
    if nodes_ready == 0:
        print("\n❌ No nodes are running! Starting distributed system...")
        return start_system()
    elif nodes_ready < 3:
        print(f"\n⚠️ Only {nodes_ready}/3 nodes running. System may work with reduced availability.")
        return True
    else:
        print(f"\n✅ All {nodes_ready} nodes are running perfectly!")
        return True

def start_system():
    """Start the distributed system"""
    print("🚀 Starting distributed threat intelligence database...")
    
    try:
        # Start all nodes
        process = subprocess.Popen([
            sys.executable, "nodes/start_all_nodes.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for nodes to start
        print("⏳ Initializing distributed nodes...")
        time.sleep(8)
        
        # Check if nodes are now running
        nodes_ready = 0
        for port in [5001, 5002, 5003]:
            try:
                response = requests.get(f"http://localhost:{port}/health", timeout=2)
                if response.status_code == 200:
                    nodes_ready += 1
            except:
                pass
        
        if nodes_ready > 0:
            print(f"✅ {nodes_ready} nodes started successfully!")
            return True
        else:
            print("❌ Failed to start nodes. Please check the error messages.")
            return False
            
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        return False

def run_demo():
    """Run the CIA demonstration"""
    print("\n🎪 Starting CIA Principles Demonstration...")
    print("This will show Confidentiality, Integrity, and Availability in action!")
    
    try:
        # Run the interactive demo
        subprocess.run([sys.executable, "demo/demo_script.py"])
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def show_menu():
    """Show demo menu options"""
    print("\n🎯 DEMO OPTIONS:")
    print("-" * 50)
    print("1. 🎪 Interactive CIA Demo (Recommended)")
    print("2. 🧪 Comprehensive System Test")
    print("3. 🔍 Quick System Check")
    print("4. 📊 Database Statistics")
    print("5. 🚀 Start All Nodes")
    print("6. ❌ Exit")
    print("-" * 50)

def run_system_test():
    """Run comprehensive system test"""
    print("\n🧪 Running comprehensive CIA system test...")
    try:
        subprocess.run([sys.executable, "demo/test_cia_system.py"])
    except Exception as e:
        print(f"❌ Error running system test: {e}")

def show_database_stats():
    """Show database statistics"""
    print("\n📊 Database Statistics:")
    print("-" * 50)
    
    for port in [5001, 5002, 5003]:
        try:
            response = requests.get(f"http://localhost:{port}/database_stats", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"Node {port}:")
                print(f"  • Records: {data.get('total_records', 0)}")
                print(f"  • Verified: {data.get('verified_records', 0)}")
                print(f"  • Integrity: {data.get('integrity_percentage', 0):.1f}%")
                print(f"  • Other Nodes: {data.get('other_nodes', 0)}")
                print()
            else:
                print(f"❌ Node {port}: Not responding")
        except:
            print(f"❌ Node {port}: Connection failed")

def main():
    """Main demo runner"""
    print_banner()
    
    print("🎓 Welcome to the CIA-Enhanced Phishing Detection System!")
    print("This system demonstrates Information Security principles:")
    print("🔒 CONFIDENTIALITY: Secure access control")
    print("🛡️ INTEGRITY: Tamper-proof data protection") 
    print("⚡ AVAILABILITY: High-availability distributed system")
    
    # Check system status
    if not check_system():
        print("\n❌ System not ready. Please check the error messages above.")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("\n🎯 Select an option (1-6): ").strip()
            
            if choice == '1':
                run_demo()
            elif choice == '2':
                run_system_test()
            elif choice == '3':
                check_system()
            elif choice == '4':
                show_database_stats()
            elif choice == '5':
                start_system()
            elif choice == '6':
                print("\n👋 Thank you for using the CIA-Enhanced System!")
                print("🛡️ Remember: Security is everyone's responsibility!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
