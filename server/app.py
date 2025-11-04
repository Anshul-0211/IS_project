from flask import Flask, request, jsonify, render_template
import joblib
import requests
import base64
import pandas as pd
from urllib.parse import urlparse
import tkinter as tk  # Add tkinter for popup messages
from tkinter import messagebox
from flask_cors import CORS
import os
import threading
from database import PhishingDatabase
import jwt
from datetime import datetime, timedelta
from functools import wraps
import bcrypt

os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)
CORS(app)

# Secret key for JWT
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-2024'  # Change this in production!

# Initialize encrypted database
db = PhishingDatabase('phishing_database.db')
print("[App] ✅ Encrypted database initialized")

# Load the saved pipeline model with both TF-IDF and domain features
pipeline = joblib.load('phishing_detection_pipeline.pkl')

# VirusTotal API key and base URL
VIRUSTOTAL_API_KEY = '60ceea3b530d3895b0c6964c774a5c683f98d9d4e294927867ca9117cbf30643'  # Replace with your actual API key
VIRUSTOTAL_URL = 'https://www.virustotal.com/api/v3/urls'

# ==================== AUTHENTICATION ====================

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
            
            # Log access
            db.log_access(current_user, request.path, request.method, request.remote_addr)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint - returns JWT token"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Verify user credentials
    user = db.verify_user(username, password)
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate JWT token
    token = jwt.encode({
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    # Log the login
    db.log_access(username, '/api/auth/login', 'POST', request.remote_addr, 'login')
    
    return jsonify({
        'token': token,
        'user': {
            'username': username,
            'email': user.get('email')
        }
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user (admin only in production)"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    try:
        success = db.create_user(username, password, email)
        if success:
            return jsonify({'message': 'User created successfully'})
        else:
            return jsonify({'error': 'User already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== REPORTS API ====================

@app.route('/api/reports', methods=['GET'])
@token_required
def get_reports(current_user):
    """Get all encrypted reports"""
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    reports = db.get_all_reports(limit=limit, offset=offset)
    
    return jsonify({
        'reports': reports,
        'count': len(reports)
    })

@app.route('/api/reports/<int:report_id>', methods=['GET'])
@token_required
def get_report(current_user, report_id):
    """Get single encrypted report"""
    reports = db.get_all_reports(limit=1000)  # Get all and filter
    report = next((r for r in reports if r['id'] == report_id), None)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    return jsonify(report)

@app.route('/api/reports/<int:report_id>/decrypt', methods=['POST'])
@token_required
def decrypt_report(current_user, report_id):
    """Decrypt a specific report"""
    reports = db.get_all_reports(limit=1000)
    report = next((r for r in reports if r['id'] == report_id), None)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    # Decrypt the report
    decrypted = db.decrypt_report(report)
    
    if not decrypted:
        return jsonify({'error': 'Failed to decrypt report'}), 500
    
    # Log decrypt action
    db.log_access(current_user, f'/api/reports/{report_id}/decrypt', 'POST', 
                  request.remote_addr, 'decrypt_report', f'Report ID: {report_id}')
    
    return jsonify(decrypted)

@app.route('/api/reports/search', methods=['GET'])
@token_required
def search_reports(current_user):
    """Search reports (requires decryption)"""
    query = request.args.get('q', '')
    # Note: This is limited as we need to decrypt to search
    # For production, consider maintaining a searchable index
    return jsonify({'message': 'Search requires decryption', 'query': query})

@app.route('/api/reports/export', methods=['GET'])
@token_required
def export_reports(current_user):
    """Export reports as CSV"""
    import csv
    from io import StringIO
    
    reports = db.get_all_reports(limit=1000)
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Timestamp', 'Block Hash', 'Previous Hash'])
    
    for report in reports:
        writer.writerow([
            report['id'],
            report['timestamp'],
            report['block_hash'][:16] + '...',
            report['previous_hash'][:16] + '...' if report['previous_hash'] else 'N/A'
        ])
    
    # Log export action
    db.log_access(current_user, '/api/reports/export', 'GET', 
                  request.remote_addr, 'export_data', f'Exported {len(reports)} reports')
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename=phishing_reports_{datetime.now().strftime("%Y%m%d")}.csv'
    }

# ==================== WHITELIST API ====================

@app.route('/api/whitelist', methods=['GET'])
@token_required
def get_whitelist_api(current_user):
    """Get all whitelisted domains"""
    whitelist_data = db.get_whitelist()
    return jsonify({'whitelist': whitelist_data})

@app.route('/api/whitelist', methods=['POST'])
@token_required
def add_whitelist_api(current_user):
    """Add domain to whitelist"""
    data = request.get_json()
    domain = data.get('domain')
    reason = data.get('reason', '')
    
    if not domain:
        return jsonify({'error': 'Domain required'}), 400
    
    success = db.add_to_whitelist(domain, current_user, reason)
    
    if success:
        # Log whitelist addition
        db.log_access(current_user, '/api/whitelist', 'POST', 
                      request.remote_addr, 'add_whitelist', f'Domain: {domain}')
        return jsonify({'message': 'Domain added to whitelist'})
    else:
        return jsonify({'error': 'Failed to add domain'}), 500

@app.route('/api/whitelist/<domain>', methods=['DELETE'])
@token_required
def remove_whitelist_api(current_user, domain):
    """Remove domain from whitelist"""
    success = db.remove_from_whitelist(domain)
    
    if success:
        # Log whitelist removal
        db.log_access(current_user, f'/api/whitelist/{domain}', 'DELETE', 
                      request.remote_addr, 'remove_whitelist', f'Domain: {domain}')
        return jsonify({'message': 'Domain removed from whitelist'})
    else:
        return jsonify({'error': 'Failed to remove domain'}), 500

@app.route('/api/whitelist/check/<domain>', methods=['GET'])
@token_required
def check_whitelist_api(current_user, domain):
    """Check if domain is whitelisted"""
    whitelist_data = db.get_whitelist()
    is_whitelisted = any(item['domain'] == domain for item in whitelist_data)
    return jsonify({'is_whitelisted': is_whitelisted})

# ==================== STATISTICS API ====================

@app.route('/api/stats/overview', methods=['GET'])
@token_required
def get_stats_overview(current_user):
    """Get overview statistics"""
    stats = db.get_statistics()
    
    # Add additional calculated stats
    stats['threats_change'] = 12  # Mock data - calculate real change
    stats['today_change'] = 8
    stats['database_size'] = f"{os.path.getsize('phishing_database.db') / (1024*1024):.2f} MB"
    
    # Recent activity (mock data)
    stats['recent_activity'] = [
        {
            'type': 'threat',
            'message': 'New phishing site detected',
            'timestamp': datetime.now().isoformat()
        },
        {
            'type': 'whitelist',
            'message': 'Domain added to whitelist',
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    return jsonify(stats)

@app.route('/api/stats/trends', methods=['GET'])
@token_required
def get_stats_trends(current_user):
    """Get trends data for charts"""
    days = request.args.get('days', 7, type=int)
    
    # Mock trend data - in production, query from database
    trends = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i-1)).strftime('%m/%d')
        trends.append({
            'date': date,
            'count': 5 + (i * 2)  # Mock data
        })
    
    return jsonify(trends)

@app.route('/api/stats/top-threats', methods=['GET'])
@token_required
def get_top_threats(current_user):
    """Get top threat domains"""
    limit = request.args.get('limit', 10, type=int)
    
    # Mock data - in production, aggregate from decrypted reports
    top_threats = [
        {'domain': 'fake-paypal.com', 'count': 15},
        {'domain': 'phishing-bank.com', 'count': 12},
        {'domain': 'scam-site.net', 'count': 9},
        {'domain': 'malicious-link.com', 'count': 7},
        {'domain': 'fake-login.org', 'count': 5},
    ]
    
    return jsonify(top_threats[:limit])

# ==================== AUDIT LOGS API ====================

@app.route('/api/audit', methods=['GET'])
@token_required
def get_audit_logs(current_user):
    """Get audit logs"""
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    logs = db.get_audit_logs(limit=limit, offset=offset)
    
    # Format logs for frontend
    formatted_logs = []
    for log in logs:
        formatted_logs.append({
            'username': log[1],
            'action': log[2],
            'timestamp': log[3],
            'ip_address': log[4],
            'description': f"{log[1]} performed {log[2]}",
            'details': log[5] if len(log) > 5 else None
        })
    
    return jsonify({'logs': formatted_logs})

@app.route('/api/audit/export', methods=['GET'])
@token_required
def export_audit_logs(current_user):
    """Export audit logs as CSV"""
    import csv
    from io import StringIO
    
    logs = db.get_audit_logs(limit=1000)
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Username', 'Action', 'Timestamp', 'IP Address', 'Details'])
    
    for log in logs:
        writer.writerow(log)
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename=audit_logs_{datetime.now().strftime("%Y%m%d")}.csv'
    }

# ==================== USERS API ====================

@app.route('/api/users', methods=['GET'])
@token_required
def get_users(current_user):
    """Get all users (admin only)"""
    users = db.get_all_users()
    return jsonify({'users': users})



# Function to check if a URL's domain is in the database whitelist
def is_in_whitelist(url):
    """Check if URL is in database whitelist"""
    try:
        domain = urlparse(url).netloc
        # Remove www. prefix for consistent matching
        domain = domain.replace('www.', '')
        
        # Get whitelist from database
        whitelist_data = db.get_whitelist()
        
        # Check if domain matches any whitelisted domain
        for item in whitelist_data:
            whitelist_domain = item['domain'].replace('www.', '')
            if whitelist_domain in domain or domain in whitelist_domain:
                print(f"[Whitelist] ✅ Domain {domain} is whitelisted (matched: {whitelist_domain})")
                return True
        
        print(f"[Whitelist] ❌ Domain {domain} is NOT whitelisted")
        return False
        
    except Exception as e:
        print(f"[Whitelist] ⚠️  Error checking whitelist: {e}")
        return False

def show_popup(stats):
    """Display detailed statistics in a popup message"""
    try:
        # Only attempt GUI popups on the main thread; otherwise skip to avoid 500s
        if threading.current_thread().name != 'MainThread':
            print(
                "[Popup Skipped] Non-main thread. Stats:",
                {
                    'url': stats.get('url'),
                    'source': stats.get('source'),
                    'probability': stats.get('probability'),
                    'virustotal_reports': stats.get('virustotal_reports'),
                    'is_whitelisted': stats.get('is_whitelisted'),
                    'is_phishing': stats.get('is_phishing')
                }
            )
            return

        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window

        # Create the message with detailed statistics
        message = f"URL: {stats['url']}\n"
        message += f"Source: {stats['source']}\n"
        message += f"Phishing Probability: {stats['probability']:.2f}\n"
        message += f"Malicious Reports (VirusTotal): {stats['virustotal_reports']}\n"
        message += f"Is Whitelisted: {stats['is_whitelisted']}\n"
        message += f"Is Phishing: {stats['is_phishing']}\n"

        # Show the popup with the message
        messagebox.showinfo("Phishing Detection Alert", message)
        root.destroy()
    except Exception as e:
        # Never let UI issues break the API response path
        print(f"[Popup Error] {e}")

# Check VirusTotal for known threats
def check_virustotal(url):
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    
    response = requests.get(f"{VIRUSTOTAL_URL}/{url_id}", headers=headers)
    
    if response.status_code == 200:
        json_response = response.json()
        malicious_count = json_response['data']['attributes']['last_analysis_stats']['malicious']
        print(f"[VirusTotal] URL: {url}, Malicious Reports: {malicious_count}")
        return malicious_count
    elif response.status_code == 404:
        print(f"[VirusTotal] URL not found in VirusTotal database: {url}")
        return 0  # Safe if not found in VirusTotal
    else:
        print(f"[VirusTotal] Error checking URL: {url}, Status Code: {response.status_code}")
        return 0  # Assume safe if an error occurs

# Classify URL with a threshold, VirusTotal, and whitelist check
def classify_url_with_threshold(url, threshold=0.7):
    is_whitelisted = is_in_whitelist(url)
    if is_whitelisted:
        print(f"[Whitelist] URL: {url} classified as LEGITIMATE")
        # Ensure native Python types for JSON serialization
        return {
            'is_phishing': False,
            'source': 'Whitelist',
            'url': url,
            'is_whitelisted': bool(True)
        }

    # Step 1: Run the model first
    domain = urlparse(url).netloc  # Extract the domain for model input

    # Create a DataFrame to match the input format used during training
    input_data = pd.DataFrame([[url, domain]], columns=['url', 'domain'])

    # Get probability for the 'phishing' class
    prob = pipeline.predict_proba(input_data)[0][1]
    is_phishing = bool(prob >= threshold)
    source = "ML Model (Threshold Applied)"

    print(f"[Model] URL: {url}, Probability: {prob:.2f}, Classified as: {'PHISHING' if is_phishing else 'LEGITIMATE'}")

    # Step 2: Check VirusTotal after running the model
    malicious_count = int(check_virustotal(url))

    # Now, we need to display the popup with both model result and VirusTotal result
    show_popup({
        'url': url,
        'source': source,
        'probability': float(prob),
        'virustotal_reports': malicious_count,
        'is_whitelisted': bool(is_whitelisted),
        'is_phishing': bool(is_phishing)
    })

    # If VirusTotal flags as malicious, return that info first
    if malicious_count > 0:
        print(f"[Result] URL: {url} classified as PHISHING (Source: VirusTotal)")
        return {
            'is_phishing': True,
            'source': 'VirusTotal',
            'url': url,
            'virustotal_reports': malicious_count,
            'is_whitelisted': bool(is_whitelisted),
            'probability': float(prob)
        }

    # Otherwise, return the model result
    return {
        'is_phishing': bool(is_phishing),
        'source': source,
        'url': url,
        'probability': float(prob),
        'virustotal_reports': malicious_count,
        'is_whitelisted': bool(is_whitelisted)
    }

@app.route('/classify_url', methods=['POST'])
def classify_url():
    # Be forgiving with malformed headers or JSON encoding
    # 1) Try regular JSON parse (silent=True avoids exceptions)
    data = request.get_json(silent=True)

    # 2) Fallback: try to parse raw body as JSON
    if data is None:
        try:
            import json as _json
            raw = request.data.decode('utf-8') if request.data else ''
            data = _json.loads(raw) if raw else {}
        except Exception:
            data = {}

    url = (data or {}).get('url')

    if not url:
        print("[Error] No URL provided in request or invalid JSON body.")
        return jsonify({
            'error': 'Invalid request. Provide JSON like {"url": "https://example.com"} with Content-Type: application/json.'
        }), 400

    print(f"[Check Start] URL: {url}", flush=True)

    result = classify_url_with_threshold(url)
    
    # Store phishing reports in encrypted database
    if result['is_phishing']:
        print("[Database] Storing encrypted phishing report...")
        try:
            metadata = {
                'probability': result.get('probability', 0),
                'source': result.get('source', 'Unknown'),
                'virustotal_reports': result.get('virustotal_reports', 0),
                'is_whitelisted': result.get('is_whitelisted', False)
            }
            report_id = db.add_phishing_report(url, metadata)
            print(f"[Database] ✅ Report stored with ID: {report_id}")
        except Exception as e:
            print(f"[Database] ❌ Error storing report: {e}")

    if result['is_phishing']:
        # Render the warning page if phishing is detected
        print("Showing warning page")
        return render_template('warning.html'), 403

    return jsonify(result)
    
# Hardcoded ransomware detection
@app.route('/check_ransomware_file', methods=['POST'])
def check_ransomware_file():
    file_data = request.files['file']
    file_path = os.path.join("temp", file_data.filename)
    file_data.save(file_path)
    
    # Hardcoded ransomware detection
    if file_data.filename == "ransomware_sample.txt":
        with open(file_path, 'r') as file:
            content = file.read()
            if "Your files have been encrypted" in content:
                os.remove(file_path)
                # Render the warning page if this is the specific ransomware file
                return render_template('warning.html'), 403

    # Cleanup if file is safe
    os.remove(file_path)
    return jsonify({'is_ransomware': False, 'source': 'Hardcoded Check'})

if __name__ == '__main__':
    os.makedirs("temp", exist_ok=True)  # Create temp directory if it doesn't exist
    app.run(port=5000, debug=True)
