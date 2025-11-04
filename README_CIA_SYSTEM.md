# 🛡️ CIA-Enhanced Phishing Detection System

## Distributed Threat Intelligence Database with CIA Principles

This system demonstrates **Confidentiality, Integrity, and Availability** principles in a distributed threat intelligence database for phishing detection.

---

## 🎯 System Overview

### **CIA Principles Implementation**

#### 🔒 **CONFIDENTIALITY**
- **Role-based access control** - Only authorized security analysts can add/modify threats
- **API key authentication** - Secure access with cryptographic keys
- **Permission-based authorization** - Different access levels for different roles
- **Audit logging** - All actions tracked for security monitoring

#### 🛡️ **INTEGRITY** 
- **Hash-based tamper detection** - SHA-256 hashes prevent data corruption
- **Cryptographic verification** - Any modification is immediately detected
- **Chain of trust** - Records linked with previous hashes
- **Automatic corruption detection** - System alerts on data tampering

#### ⚡ **AVAILABILITY**
- **Distributed architecture** - Multiple nodes ensure high availability
- **Automatic replication** - Data synchronized across all nodes
- **Failover capability** - System continues if nodes fail
- **Load balancing** - Queries distributed across available nodes

---

## 🚀 Quick Start

### **1. Start the System**
```bash
# Quick start (recommended)
python demo/quick_start.py

# Or start manually
python nodes/start_all_nodes.py
```

### **2. Run CIA Demonstration**
```bash
# Interactive demo (best for presentations)
python demo/demo_script.py

# Comprehensive system test
python demo/test_cia_system.py
```

### **3. Test Individual Components**
```bash
# Test specific nodes
python nodes/start_node_1.py  # Port 5001
python nodes/start_node_2.py  # Port 5002  
python nodes/start_node_3.py  # Port 5003
```

---

## 🏗️ System Architecture

### **Distributed Database Structure**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Node 1        │    │   Node 2        │    │   Node 3        │
│   Port: 5001    │◄──►│   Port: 5002    │◄──►│   Port: 5003    │
│   Primary       │    │   Secondary     │    │   Tertiary      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Browser        │
                    │   Extension      │
                    │   (Client)       │
                    └─────────────────┘
```

### **Data Flow**
1. **User visits URL** → Browser extension intercepts
2. **Extension queries** → Distributed database
3. **Database checks** → Local cache first, then other nodes
4. **Response returned** → Allow/block based on threat intelligence
5. **New threats added** → Replicated across all nodes

---

## 🔧 API Endpoints

### **Threat Management**
```bash
# Add new threat (requires authorization)
POST /add_threat
{
    "url": "phishing-site.com",
    "classification": "phishing", 
    "confidence": 0.95,
    "api_key": "security_analyst_001"
}

# Get threat information
GET /get_threat/{url}

# Test record integrity
POST /test_integrity
{
    "url": "phishing-site.com"
}
```

### **System Management**
```bash
# Health check
GET /health

# Database statistics
GET /database_stats

# CIA principles demo
GET /cia_demo

# Add node to network
POST /add_node
{
    "node_id": "node_4",
    "port": 5004
}
```

---

## 🎪 Demonstration Scenarios

### **Scenario 1: CONFIDENTIALITY Demo**
```
1. Try adding threat without API key → ACCESS DENIED
2. Try adding threat with invalid key → ACCESS DENIED  
3. Add threat with valid analyst key → ACCESS GRANTED
4. Show role-based permissions working
```

### **Scenario 2: INTEGRITY Demo**
```
1. Add threat record with hash protection
2. Verify record integrity → SUCCESS
3. Simulate tampering attempt → DETECTED
4. Show hash verification working
```

### **Scenario 3: AVAILABILITY Demo**
```
1. Add threat to Node 1
2. Query from Node 2 → FOUND
3. Query from Node 3 → FOUND
4. Stop Node 1 → System continues working
5. Show distributed redundancy
```

---

## 🔐 Security Features

### **Authentication & Authorization**
- **API Key System**: Cryptographic keys for secure access
- **Role-based Access**: Different permissions for different analysts
- **Session Tracking**: Monitor analyst activity
- **Audit Logging**: Complete action history

### **Data Protection**
- **Hash Verification**: SHA-256 integrity checking
- **Tamper Detection**: Automatic corruption alerts
- **Encrypted Communication**: HTTPS between nodes
- **Secure Storage**: Encrypted database files

### **High Availability**
- **Distributed Nodes**: Multiple redundant servers
- **Automatic Replication**: Data synced across nodes
- **Failover Support**: Continues if nodes fail
- **Load Distribution**: Queries spread across nodes

---

## 📊 Monitoring & Statistics

### **Database Statistics**
```bash
GET /database_stats
```
Returns:
- Total records count
- Verified records count  
- Corrupted records count
- Integrity percentage
- Active nodes count

### **Health Monitoring**
```bash
GET /health
```
Returns:
- Node status
- Record count
- System health
- Uptime information

---

## 🎓 Educational Value

### **Information Security Concepts**
- **CIA Triad**: Complete implementation of security principles
- **Distributed Systems**: High availability and fault tolerance
- **Cryptographic Security**: Hash functions and integrity checking
- **Access Control**: Role-based security models
- **Threat Intelligence**: Collaborative security information sharing

### **Real-World Applications**
- **Enterprise Security**: Corporate threat intelligence sharing
- **Government Agencies**: National security information exchange
- **Security Research**: Collaborative threat analysis
- **Incident Response**: Rapid threat information distribution

---

## 🛠️ Technical Implementation

### **Technologies Used**
- **Backend**: Python Flask
- **Database**: JSON-based distributed storage
- **Cryptography**: SHA-256 hashing
- **Networking**: HTTP REST APIs
- **Authentication**: API key system

### **Key Components**
- **ThreatIntelligenceDB**: Core database class
- **AuthenticationSystem**: Security and access control
- **DistributedNodes**: Multi-node architecture
- **CIA Demonstrator**: Interactive demo system

---

## 🚀 Getting Started

### **Prerequisites**
```bash
pip install flask requests flask-cors
```

### **Installation**
1. Clone the repository
2. Navigate to CIA-Enhanced-System directory
3. Run `python demo/quick_start.py`
4. Follow the interactive demonstration

### **Testing**
```bash
# Test the system
python demo/test_cia_system.py

# Run interactive demo
python demo/demo_script.py

# Check system health
curl http://localhost:5001/health
```

---

## 🎯 Perfect for Information Security Labs

This system demonstrates:
- ✅ **CIA Principles** in real-world application
- ✅ **Distributed Systems** architecture
- ✅ **Cryptographic Security** implementation
- ✅ **Access Control** mechanisms
- ✅ **Threat Intelligence** sharing
- ✅ **High Availability** design

**Ideal for**: Information Security courses, cybersecurity labs, and security research demonstrations.

---

## 📞 Support

For questions or issues:
1. Check the demo scripts for examples
2. Review the API documentation
3. Run the test suite to verify functionality
4. Check node connectivity and health

**Happy Learning! 🎓🛡️**
