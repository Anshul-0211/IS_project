import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from tkinter import *
from tkinter import messagebox  # Import messagebox for popups
from cryptography.fernet import Fernet

# --- Generate a key for encryption ---
key = Fernet.generate_key()
cipher = Fernet(key)

# --- Email Phishing Detection Model Setup ---
emails = ["Your account has been compromised, click here to secure it", 
          "Free voucher for shopping, claim now", 
          "Meeting at 3 PM tomorrow at office", 
          "Get 50% off your purchase", 
          "Please confirm your bank details to proceed with the transfer", 
          "Weekly team meeting reminder"]
labels = [1, 1, 0, 1, 1, 0]  # 1 = phishing, 0 = non-phishing

# Split the data
X_train, X_test, y_train, y_test = train_test_split(emails, labels, test_size=0.2)

# Build a TF-IDF Vectorizer and Naive Bayes classifier pipeline
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# --- Simulated Email Sending and Phishing Detection ---

# Function to check if the email content is phishing
def check_for_phishing(content):
    prediction = model.predict([content])[0]
    return "Phishing Detected" if prediction == 1 else "No Phishing Detected"

# Function to encrypt data
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
    phishing_result = check_for_phishing(content)

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
