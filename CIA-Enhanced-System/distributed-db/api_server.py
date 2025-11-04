#!/usr/bin/env python3
"""
API Server for Distributed Threat Intelligence Database
Provides REST API endpoints for CIA demonstration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add the distributed-db directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from threat_intelligence_db import initialize_database, get_database

app = Flask(__name__)
CORS(app)

# Configuration
NODE_ID = os.getenv('NODE_ID', 'node_1')
PORT = int(os.getenv('PORT', 5001))
AUTHORIZED_KEYS = [
    'security_analyst_001',
    'security_analyst_002', 
    'admin_key_123'
]

# Initialize database
threat_db = initialize_database(NODE_ID, PORT, AUTHORIZED_KEYS)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'node_id': NODE_ID,
        'port': PORT,
        'records_count': len(threat_db.records)
    })

@app.route('/add_threat', methods=['POST'])
def add_threat():
    """
    Add new threat record (CONFIDENTIALITY demo)
    Only authorized security analysts can add threats
    """
    try:
        data = request.get_json()
        
        # Required fields
        url = data.get('url')
        classification = data.get('classification', 'phishing')
        confidence = data.get('confidence', 0.9)
        api_key = data.get('api_key')
        source = data.get('source', 'manual')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not api_key:
            return jsonify({'error': 'API key is required for security'}), 401
        
        # Add threat record
        result = threat_db.add_threat_record(url, classification, confidence, api_key, source)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_threat/<path:url>', methods=['GET'])
def get_threat(url):
    """
    Get threat information (AVAILABILITY demo)
    Checks local cache first, then queries other nodes
    """
    try:
        result = threat_db.get_threat_info(url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/replicate_record', methods=['POST'])
def replicate_record():
    """
    Replicate record from other nodes (AVAILABILITY)
    Internal endpoint for node-to-node communication
    """
    try:
        record = request.get_json()
        
        # INTEGRITY: Verify record integrity before accepting
        if threat_db.verify_integrity(record):
            threat_db.records[record['url']] = record
            threat_db.save_database()
            
            return jsonify({
                'success': True,
                'message': 'Record replicated successfully',
                'integrity_verified': True
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Record integrity verification failed',
                'integrity_verified': False
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/database_stats', methods=['GET'])
def database_stats():
    """Get database statistics for monitoring"""
    try:
        stats = threat_db.get_database_stats()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cia_demo', methods=['GET'])
def cia_demo():
    """
    CIA Principles demonstration endpoint
    Shows how Confidentiality, Integrity, and Availability are implemented
    """
    try:
        cia_info = threat_db.demonstrate_cia_principles()
        return jsonify(cia_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_node', methods=['POST'])
def add_node():
    """Add another node to the distributed network"""
    try:
        data = request.get_json()
        node_id = data.get('node_id')
        port = data.get('port')
        
        if not node_id or not port:
            return jsonify({'error': 'node_id and port are required'}), 400
        
        threat_db.add_node(node_id, port)
        
        return jsonify({
            'success': True,
            'message': f'Node {node_id} added to network',
            'network_nodes': threat_db.other_nodes
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_integrity', methods=['POST'])
def test_integrity():
    """
    INTEGRITY demo: Test tamper detection
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or url not in threat_db.records:
            return jsonify({'error': 'URL not found in database'}), 404
        
        record = threat_db.records[url]
        is_valid = threat_db.verify_integrity(record)
        
        return jsonify({
            'url': url,
            'integrity_verified': is_valid,
            'hash': record.get('hash'),
            'message': 'Record is valid' if is_valid else 'Record has been tampered with!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/simulate_tampering', methods=['POST'])
def simulate_tampering():
    """
    INTEGRITY demo: Simulate data tampering to show detection
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or url not in threat_db.records:
            return jsonify({'error': 'URL not found in database'}), 404
        
        # Simulate tampering by modifying the record
        record = threat_db.records[url]
        original_classification = record['classification']
        record['classification'] = 'safe'  # Tamper with the data
        
        # Check if tampering is detected
        is_valid = threat_db.verify_integrity(record)
        
        # Restore original data
        record['classification'] = original_classification
        
        return jsonify({
            'url': url,
            'tampering_detected': not is_valid,
            'message': 'Tampering detected! Hash verification failed.' if not is_valid else 'No tampering detected',
            'original_classification': original_classification
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"Starting Threat Intelligence Database Node: {NODE_ID}")
    print(f"Port: {PORT}")
    print(f"Authorized Keys: {AUTHORIZED_KEYS}")
    print(f"Database file: {threat_db.db_file}")
    
    app.run(host='0.0.0.0', port=PORT, debug=True)
