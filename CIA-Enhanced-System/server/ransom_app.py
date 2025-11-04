import random
import tkinter as tk
from tkinter import filedialog

def load_file(file_path):
    """Reads a local file and returns its content as a list of lines."""
    try:
        # Try UTF-8 first (most common)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read().splitlines()  # Reading lines for matching
        return content
    except FileNotFoundError:
        return None
    except Exception as e:
        # If UTF-8 fails, try with latin-1 (handles all byte values)
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read().splitlines()
            return content
        except Exception as e2:
            print(f"Error reading file: {e2}")
            return None

def simulate_ml_model_response(keyword, content_snippet):
    """Simulate an ML model response for a detected keyword in the content."""
    # Randomly assign a confidence score between 0.5 and 1 (since the model is probabilistic)
    confidence = random.uniform(0.5, 1.0)
    # Simulate classification of the severity (high, medium, low) based on the confidence
    if confidence > 0.8:
        severity = "High"
    elif confidence > 0.6:
        severity = "Medium"
    else:
        severity = "Low"
    
    # Simulate the output of an ML model analyzing the keyword occurrence and context
    return {
        "keyword": keyword,
        "content_snippet": content_snippet,
        "confidence": round(confidence, 2),
        "severity": severity
    }

def check_for_ransomware(content, ransomware_keywords):
    """Checks if any of the ransomware keywords are present in the content."""
    matches = []
    for line in content:
        for keyword in ransomware_keywords:
            if keyword.lower() in line.lower():
                # Simulate ML model finding a snippet of content around the keyword
                start_index = max(line.lower().find(keyword) - 30, 0)  # Get some context before the match
                end_index = min(line.lower().find(keyword) + len(keyword) + 30, len(line))  # And after the match
                content_snippet = line[start_index:end_index]
                
                # Simulate model processing this match
                model_response = simulate_ml_model_response(keyword, content_snippet)
                matches.append(model_response)
    return matches

def select_file():
    """Opens a file dialog to select a file."""
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text Files", "*.txt")])
    if file_path:
        print(f"File selected: {file_path}")
        main(file_path)  # Proceed with the selected file
    else:
        print("No file selected. Please select a file to proceed.")

def main(file_path):
    # List of common ransomware keywords or phrases (this can be extended)
    ransomware_keywords = [
        "ransomware", "decrypt", "bitcoin", "pay", "unlock", "cryptolocker", "cryptowall",
        "files encrypted", "your files are locked", "pay to decrypt", "payment required"
    ]
    
    # Load the file content
    print(f"Attempting to load file: {file_path}")  # Debug statement
    content = load_file(file_path)
    
    if content is None:
        print(f"File '{file_path}' not found.")
        return
    
    print(f"File loaded successfully. Content length: {len(content)} lines.")  # Debug statement
    
    # Check for ransomware keywords in the file content
    matches = check_for_ransomware(content, ransomware_keywords)
    
    if matches:
        print("Potential ransomware detected in the following sections:\n")
        for match in matches:
            print(f"---\nDetected pattern: {match['keyword']}")
            print(f"Context snippet: {match['content_snippet']}")
            print(f"Confidence: {match['confidence'] * 100}%")
            print(f"Threat Severity: {match['severity']}\n")
    else:
        print("No ransomware-related patterns found.")

# Create the Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Show the file selection dialog when the program starts
select_file()
