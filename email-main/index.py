# phishing_model_training.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import tensorflow as tf

# Load your dataset (ensure it's saved in CSV format)
data = pd.read_csv("spam.csv")  # replace with your actual CSV filename
texts = data['Message'].values
labels = data['Category'].apply(lambda x: 1 if x == 'spam' else 0).values  # 1 for spam, 0 for ham

# Hyperparameters
max_words = 10000    # Vocabulary size
max_len = 200        # Max length of a sequence
embedding_dim = 128  # Embedding layer output dimension

# Tokenize and pad the sequences
tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# Split the data
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

# Build the LSTM model
model = Sequential([
    Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_len),
    LSTM(64, return_sequences=True),
    Dropout(0.5),
    LSTM(32),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))

# Save model and tokenizer
model.save('phishing_detection_model.h5')
joblib.dump(tokenizer, 'tokenizer.pkl')
print("Model and tokenizer saved successfully.")
