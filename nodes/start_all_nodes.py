#!/usr/bin/env python3
"""
Start All Distributed Nodes for CIA Demonstration
This script starts all 3 nodes of the distributed threat intelligence database
"""

import subprocess
import time
import sys
import os

def start_node(node_script, node_name, port):
    """Start a single node"""
    try:
        print(f"Starting {node_name} on port {port}...")
        process = subprocess.Popen([
            sys.executable, node_script
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give the node time to start
        time.sleep(2)
        
        if process.poll() is None:
            print(f"✅ {node_name} started successfully on port {port}")
            return process
        else:
            print(f"❌ Failed to start {node_name}")
            return None
    except Exception as e:
        print(f"❌ Error starting {node_name}: {e}")
        return None

def main():
    print("=" * 80)
    print("🚀 STARTING DISTRIBUTED THREAT INTELLIGENCE DATABASE")
    print("=" * 80)
    print("This will start 3 nodes to demonstrate CIA principles:")
    print("• CONFIDENTIALITY: Role-based access control")
    print("• INTEGRITY: Hash-based tamper detection") 
    print("• AVAILABILITY: Distributed across multiple nodes")
    print("=" * 80)
    print()
    
    # Start all nodes
    processes = []
    
    # Node 1
    p1 = start_node("start_node_1.py", "Node 1 (Primary)", 5001)
    if p1:
        processes.append(("Node 1", p1))
    
    # Node 2  
    p2 = start_node("start_node_2.py", "Node 2 (Secondary)", 5002)
    if p2:
        processes.append(("Node 2", p2))
    
    # Node 3
    p3 = start_node("start_node_3.py", "Node 3 (Tertiary)", 5003)
    if p3:
        processes.append(("Node 3", p3))
    
    print()
    print("=" * 80)
    print("📊 DISTRIBUTED SYSTEM STATUS")
    print("=" * 80)
    
    for name, process in processes:
        if process.poll() is None:
            print(f"✅ {name}: Running")
        else:
            print(f"❌ {name}: Stopped")
    
    print()
    print("🌐 API Endpoints Available:")
    print("• Node 1: http://localhost:5001")
    print("• Node 2: http://localhost:5002") 
    print("• Node 3: http://localhost:5003")
    print()
    print("🔧 Test the system:")
    print("• Run: python demo/test_cia_system.py")
    print("• Or: python demo/demo_script.py")
    print()
    print("Press Ctrl+C to stop all nodes")
    print("=" * 80)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if any process has died
            for name, process in processes:
                if process.poll() is not None:
                    print(f"⚠️ {name} has stopped unexpectedly")
                    
    except KeyboardInterrupt:
        print("\n🛑 Stopping all nodes...")
        
        for name, process in processes:
            try:
                process.terminate()
                print(f"✅ {name} stopped")
            except:
                print(f"❌ Error stopping {name}")
        
        print("All nodes stopped. Goodbye!")

if __name__ == '__main__':
    main()
