# app.py

from flask import Flask, request, jsonify
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

app = Flask(__name__)

# Load trained model and tokenizer
model = tf.keras.models.load_model('phishing_detection_model.h5')
tokenizer = joblib.load('tokenizer.pkl')

# Configuration for text preprocessing
max_len = 200

def detect_phishing(text):
    # Preprocess input text
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')
    
    # Get model prediction
    prob = model.predict(padded_sequence)[0][0]
    is_phishing = prob >= 0.5  # Default threshold at 0.5, can be adjusted

    return is_phishing, prob

@app.route('/check_phishing', methods=['POST'])
def check_phishing():
    data = request.get_json()
    content = data.get('content', '')

    if content:
        is_phishing, prob = detect_phishing(content)
        response = {
            'is_phishing': is_phishing,
            'probability': float(prob)
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'No content provided'}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
