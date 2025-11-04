#!/usr/bin/env python3
"""
Working Distributed CIA Demo
Simplified version that works without complex dependencies
"""

import json
import hashlib
import time
import threading
from datetime import datetime
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

class DistributedThreatDatabase:
    """Simplified distributed threat database"""
    
    def __init__(self, node_id, port):
        self.node_id = node_id
        self.port = port
        self.records = {}
        self.authorized_users = ['security_analyst_001', 'security_analyst_002']
        self.other_nodes = []
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
    
    def generate_hash(self, url, classification, confidence, timestamp):
        """Generate hash for integrity verification"""
        data = f"{url}{classification}{confidence}{timestamp}{self.node_id}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def add_threat(self, url, classification, confidence, user_id):
        """Add threat record"""
        if user_id not in self.authorized_users:
            return {'success': False, 'error': 'Unauthorized access denied'}
        
        timestamp = datetime.now().isoformat()
        hash_value = self.generate_hash(url, classification, confidence, timestamp)
        
        record = {
            'url': url,
            'classification': classification,
            'confidence': confidence,
            'timestamp': timestamp,
            'hash': hash_value,
            'authorized_by': user_id,
            'node_id': self.node_id
        }
        
        self.records[url] = record
        return {'success': True, 'message': 'Threat added successfully', 'hash': hash_value}
    
    def get_threat(self, url):
        """Get threat information"""
        if url in self.records:
            record = self.records[url]
            expected_hash = self.generate_hash(
                record['url'], record['classification'], 
                record['confidence'], record['timestamp']
            )
            integrity_verified = record['hash'] == expected_hash
            
            return {
                'found': True,
                'classification': record['classification'],
                'confidence': record['confidence'],
                'timestamp': record['timestamp'],
                'integrity_verified': integrity_verified,
                'source': 'local_cache',
                'node_id': self.node_id
            }
        else:
            # Check other nodes
            for node in self.other_nodes:
                try:
                    response = requests.get(f"http://localhost:{node['port']}/get_threat/{url}", timeout=1)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('found'):
                            # Replicate to local database
                            self.records[url] = data
                            return data
                except:
                    continue
            
            return {'found': False, 'message': 'Threat not found in distributed database'}
    
    def verify_integrity(self, url):
        """Verify record integrity"""
        if url not in self.records:
            return {'error': 'Record not found'}
        
        record = self.records[url]
        expected_hash = self.generate_hash(
            record['url'], record['classification'],
            record['confidence'], record['timestamp']
        )
        
        is_valid = record['hash'] == expected_hash
        return {
            'url': url,
            'integrity_verified': is_valid,
            'hash': record['hash'],
            'message': 'Record is valid' if is_valid else 'Record has been tampered with!'
        }
    
    def simulate_tampering(self, url):
        """Simulate tampering detection"""
        if url not in self.records:
            return {'error': 'Record not found'}
        
        record = self.records[url]
        original_classification = record['classification']
        record['classification'] = 'safe'  # Tamper with data
        
        expected_hash = self.generate_hash(
            record['url'], record['classification'],
            record['confidence'], record['timestamp']
        )
        
        is_valid = record['hash'] == expected_hash
        record['classification'] = original_classification  # Restore
        
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
            'node_id': self.node_id,
            'total_records': total_records,
            'verified_records': verified_records,
            'corrupted_records': total_records - verified_records,
            'integrity_percentage': (verified_records / total_records * 100) if total_records > 0 else 100,
            'other_nodes': len(self.other_nodes)
        }
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({
                'status': 'healthy',
                'node_id': self.node_id,
                'port': self.port,
                'records_count': len(self.records)
            })
        
        @self.app.route('/add_threat', methods=['POST'])
        def add_threat():
            data = request.get_json()
            result = self.add_threat(
                data.get('url'),
                data.get('classification', 'phishing'),
                data.get('confidence', 0.9),
                data.get('api_key')
            )
            return jsonify(result)
        
        @self.app.route('/get_threat/<path:url>', methods=['GET'])
        def get_threat(url):
            return jsonify(self.get_threat(url))
        
        @self.app.route('/test_integrity', methods=['POST'])
        def test_integrity():
            data = request.get_json()
            return jsonify(self.verify_integrity(data.get('url')))
        
        @self.app.route('/simulate_tampering', methods=['POST'])
        def simulate_tampering():
            data = request.get_json()
            return jsonify(self.simulate_tampering(data.get('url')))
        
        @self.app.route('/database_stats', methods=['GET'])
        def database_stats():
            return jsonify(self.get_stats())
    
    def run(self):
        """Run the Flask app"""
        print(f"Starting {self.node_id} on port {self.port}")
        self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False)

def start_node(node_id, port):
    """Start a single node"""
    db = DistributedThreatDatabase(node_id, port)
    
    # Add other nodes (simplified - just for demo)
    if node_id == 'node_1':
        db.other_nodes = [{'node_id': 'node_2', 'port': 5002}, {'node_id': 'node_3', 'port': 5003}]
    elif node_id == 'node_2':
        db.other_nodes = [{'node_id': 'node_1', 'port': 5001}, {'node_id': 'node_3', 'port': 5003}]
    elif node_id == 'node_3':
        db.other_nodes = [{'node_id': 'node_1', 'port': 5001}, {'node_id': 'node_2', 'port': 5002}]
    
    db.run()

def main():
    """Main function to start distributed nodes"""
    print("=" * 80)
    print("STARTING DISTRIBUTED THREAT INTELLIGENCE DATABASE")
    print("=" * 80)
    print("This will start 3 nodes to demonstrate CIA principles:")
    print("CONFIDENTIALITY: Role-based access control")
    print("INTEGRITY: Hash-based tamper detection")
    print("AVAILABILITY: Distributed across multiple nodes")
    print("=" * 80)
    
    # Start nodes in separate threads
    threads = []
    
    # Node 1
    t1 = threading.Thread(target=start_node, args=('node_1', 5001))
    t1.daemon = True
    t1.start()
    threads.append(t1)
    
    # Node 2
    t2 = threading.Thread(target=start_node, args=('node_2', 5002))
    t2.daemon = True
    t2.start()
    threads.append(t2)
    
    # Node 3
    t3 = threading.Thread(target=start_node, args=('node_3', 5003))
    t3.daemon = True
    t3.start()
    threads.append(t3)
    
    print("\nWaiting for nodes to start...")
    time.sleep(5)
    
    print("\nTesting node connectivity...")
    for port in [5001, 5002, 5003]:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"Node {port}: ACTIVE - {data.get('records_count', 0)} records")
            else:
                print(f"Node {port}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Node {port}: CONNECTION FAILED")
    
    print("\n" + "=" * 80)
    print("DISTRIBUTED SYSTEM STATUS")
    print("=" * 80)
    print("API Endpoints Available:")
    print("Node 1: http://localhost:5001")
    print("Node 2: http://localhost:5002")
    print("Node 3: http://localhost:5003")
    print("\nTest the system:")
    print("python demo/working_demo.py")
    print("=" * 80)
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all nodes...")
        print("All nodes stopped. Goodbye!")

if __name__ == '__main__':
    main()
