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

os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)
CORS(app)

# Load the saved pipeline model with both TF-IDF and domain features
pipeline = joblib.load('phishing_detection_pipeline.pkl')

# VirusTotal API key and base URL
VIRUSTOTAL_API_KEY = '60ceea3b530d3895b0c6964c774a5c683f98d9d4e294927867ca9117cbf30643'  # Replace with your actual API key
VIRUSTOTAL_URL = 'https://www.virustotal.com/api/v3/urls'

# Whitelist of known popular legitimate sites to reduce false positives
whitelist = ["google.com", "github.com", "microsoft.com", "gmail.com"]

# Function to check if a URL's domain is in the whitelist
def is_in_whitelist(url):
    domain = urlparse(url).netloc
    return any(whitelist_domain in domain for whitelist_domain in whitelist)

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
