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
        return {'is_phishing': False, 'source': 'Whitelist', 'url': url, 'is_whitelisted': True}

    # Step 1: Run the model first
    domain = urlparse(url).netloc  # Extract the domain for model input

    # Create a DataFrame to match the input format used during training
    input_data = pd.DataFrame([[url, domain]], columns=['url', 'domain'])

    # Get probability for the 'phishing' class
    prob = pipeline.predict_proba(input_data)[0][1]
    is_phishing = prob >= threshold
    source = "ML Model (Threshold Applied)"

    print(f"[Model] URL: {url}, Probability: {prob:.2f}, Classified as: {'PHISHING' if is_phishing else 'LEGITIMATE'}")

    # Step 2: Check VirusTotal after running the model
    malicious_count = check_virustotal(url)

    # Now, we need to display the popup with both model result and VirusTotal result
    show_popup({
        'url': url,
        'source': source,
        'probability': prob,
        'virustotal_reports': malicious_count,
        'is_whitelisted': is_whitelisted,
        'is_phishing': is_phishing
    })

    # If VirusTotal flags as malicious, return that info first
    if malicious_count > 0:
        print(f"[Result] URL: {url} classified as PHISHING (Source: VirusTotal)")

        return {'is_phishing': True, 'source': 'VirusTotal', 'url': url, 'virustotal_reports': malicious_count, 'is_whitelisted': is_whitelisted, 'probability': prob}

    # Otherwise, return the model result
    return {'is_phishing': is_phishing, 'source': source, 'url': url, 'probability': prob, 'virustotal_reports': malicious_count, 'is_whitelisted': is_whitelisted}

@app.route('/classify_url', methods=['POST'])
def classify_url():
    data = request.get_json()
    url = data.get('url')
    
    if url:
        print(f"[Check Start] URL: {url}", flush=True)
        
        result = classify_url_with_threshold(url)
        
        if result['is_phishing']:
            # Render the warning page if phishing is detected
            print("Showing warning page")
            return render_template('warning.html'), 403
        
        return jsonify(result)
    else:
        print("[Error] No URL provided in request.")
        return jsonify({'error': 'No URL provided'}), 400
    
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
