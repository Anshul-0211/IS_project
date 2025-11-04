import numpy as np
import pandas as pd
from cryptography.fernet import Fernet
from tensorflow import keras
from tkinter import *
from tkinter import messagebox  # Import messagebox for popups

# --- Generate a key for encryption ---
key = Fernet.generate_key()
cipher = Fernet(key)

# Load the trained neural network model
model = keras.models.load_model('phishing_detection_model.h5')

# Load tokenizer if you trained your model with tokenization
import pickle
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# --- Function to check if the email content is phishing ---
def check_for_phishing(subject, content):
    combined_text = f"{subject} {content}"
    
    # Tokenize and pad the input
    sequences = tokenizer.texts_to_sequences([combined_text])
    padded_sequences = keras.preprocessing.sequence.pad_sequences(sequences, maxlen=100)  # Adjust maxlen as per your model's input shape

    prediction = model.predict(padded_sequences)
    
    # Assuming that your model outputs a probability
    return "Phishing Detected" if prediction[0][0] > 0.5 else "No Phishing Detected"  # Adjust threshold if needed

# --- Function to encrypt data ---
def encrypt_data(data):
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()

# --- UI Setup for Simulating Phishing Detection ---
def send_email():
    # Get email content from the UI
    recipient = recipient_entry.get()
    subject = subject_entry.get()
    content = content_text.get("1.0", END)

    # Simulate phishing detection
    phishing_result = check_for_phishing(subject, content)

    # Encrypt email details
    encrypted_recipient = encrypt_data(recipient)
    encrypted_subject = encrypt_data(subject)
    encrypted_content = encrypt_data(content)

    # Create the message to display in the popup
    popup_message = (
        f"Encrypted Email to: {encrypted_recipient}\n"
        f"Encrypted Subject: {encrypted_subject}\n"
        f"Encrypted Content: {encrypted_content}\n"
        f"Detection Result: {phishing_result}"
    )

    # Show the popup with the encrypted information and phishing result
    messagebox.showinfo("Email Submission Result", popup_message)

# Set up the UI
root = Tk()
root.title("Simulated Phishing Email Detector")

# Recipient email details
Label(root, text="Recipient Email (Placeholder):").grid(row=0, column=0)
recipient_entry = Entry(root, width=40)
recipient_entry.grid(row=0, column=1)
recipient_entry.insert(0, "test@placeholder.com")  # Using a placeholder email

# Email subject
Label(root, text="Subject:").grid(row=1, column=0)
subject_entry = Entry(root, width=40)
subject_entry.grid(row=1, column=1)

# Email content
Label(root, text="Content:").grid(row=2, column=0)
content_text = Text(root, height=10, width=40)
content_text.grid(row=2, column=1)

# Send button
send_button = Button(root, text="Send Email", command=send_email)
send_button.grid(row=3, column=1)

root.mainloop()
