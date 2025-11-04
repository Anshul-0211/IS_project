# 📧 How to Test Email Phishing Detection

## 🎯 Three Ways to Test

---

## Method 1: Automated Test Script (Easiest) ⭐

### **Quick Start**:
```bash
cd email-main
python test_email_phishing.py
```

### **What It Does**:
- Tests 6 sample emails automatically
- Shows detection results with colors
- Displays accuracy percentage
- Tests both legitimate and phishing emails

### **Sample Output**:
```
============================================================
          📧 EMAIL PHISHING DETECTION TEST
============================================================

Loading model and tokenizer...
✓ Model and tokenizer loaded successfully

============================================================
           Test 1: Legitimate Email 1: Meeting Reminder
============================================================

Subject: Team Meeting Tomorrow
Content: Hi team, just a reminder about our weekly meeting...

✓ LEGITIMATE EMAIL
   Confidence: 85.3%
✓ Correct detection
```

### **Interactive Mode**:
```bash
python test_email_phishing.py --interactive
```

Then enter your own emails to test!

---

## Method 2: GUI Application (Visual) 🖼️

### **Quick Start**:
```bash
cd email-main
python model.py
```

### **What It Does**:
- Opens a window with email form
- Enter recipient, subject, and content
- Click "Send Email" to check
- Shows detection result in popup
- Also demonstrates encryption

### **How to Use**:
1. Window opens automatically
2. Fill in:
   - **Recipient**: test@example.com (placeholder)
   - **Subject**: Your email subject
   - **Content**: Your email message
3. Click "Send Email"
4. See popup with:
   - Encrypted email (shows encryption feature)
   - Detection result (Phishing or Not)

### **Test Examples**:

**Legitimate Email**:
```
Subject: Project Update
Content: Hi team, the project is on track. Next meeting Friday.
Result: ✓ No Phishing Detected
```

**Phishing Email**:
```
Subject: URGENT: Account Compromised
Content: Click here immediately to secure your account!
Result: ⚠️ Phishing Detected
```

---

## Method 3: Flask API (For Integration) 🔌

### **Step 1: Start the Server**:
```bash
cd email-main
python app.py
```

Server runs on `http://localhost:5000`

### **Step 2: Test with Curl**:

**Test Legitimate Email**:
```bash
curl -X POST http://localhost:5000/check_phishing \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"Hi team, meeting tomorrow at 3 PM\"}"
```

**Expected Response**:
```json
{
  "is_phishing": false,
  "probability": 0.23
}
```

**Test Phishing Email**:
```bash
curl -X POST http://localhost:5000/check_phishing \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"URGENT! Your account has been compromised. Click here immediately!\"}"
```

**Expected Response**:
```json
{
  "is_phishing": true,
  "probability": 0.89
}
```

---

## 🧪 Sample Test Cases

### **Legitimate Emails** (Should Pass):

1. **Meeting Reminder**:
   ```
   Subject: Team Meeting
   Content: Reminder about our meeting tomorrow at 3 PM
   ```

2. **Project Update**:
   ```
   Subject: Weekly Update
   Content: Project is progressing well, next milestone on Friday
   ```

3. **Newsletter**:
   ```
   Subject: Monthly Newsletter
   Content: Welcome to our newsletter with tips and updates
   ```

### **Phishing Emails** (Should Detect):

1. **Account Compromise**:
   ```
   Subject: URGENT: Account Compromised
   Content: Your account has been hacked! Click here immediately to secure it!
   ```

2. **Prize Winner**:
   ```
   Subject: You've Won $1,000,000!
   Content: Congratulations! Click here to claim your prize. Enter your bank details.
   ```

3. **Verification Required**:
   ```
   Subject: Bank Account Verification
   Content: We detected suspicious activity. Verify your account immediately or it will be locked.
   ```

---

## 📊 Understanding Results

### **Probability Score**:
- **0.0 - 0.4**: Likely legitimate
- **0.4 - 0.6**: Uncertain (borderline)
- **0.6 - 1.0**: Likely phishing

### **Threshold**:
- Default threshold: **0.5**
- Scores ≥ 0.5 = Phishing
- Scores < 0.5 = Legitimate

---

## 🎯 For Your Demo

### **Recommended Demo Flow**:

1. **Start with GUI** (Most Visual):
   ```bash
   python model.py
   ```
   - Show the interface
   - Test a safe email
   - Test a phishing email
   - Show the difference

2. **Run Automated Tests**:
   ```bash
   python test_email_phishing.py
   ```
   - Show multiple tests at once
   - Display accuracy metrics
   - Professional demonstration

3. **Show API** (Optional):
   ```bash
   python app.py
   # In another terminal:
   curl -X POST http://localhost:5000/check_phishing \
     -H "Content-Type: application/json" \
     -d "{\"content\": \"URGENT! Click here now!\"}"
   ```
   - Show how it can be integrated
   - RESTful API demonstration

---

## 🔧 Troubleshooting

### **Error: Model not found**
```
FileNotFoundError: phishing_detection_model.h5
```
**Solution**: Make sure you're in the `email-main` directory:
```bash
cd email-main
python model.py
```

### **Error: Tokenizer not found**
```
FileNotFoundError: tokenizer.pkl
```
**Solution**: Run the training script first:
```bash
python index.py
```

### **Error: TensorFlow not installed**
```
ModuleNotFoundError: No module named 'tensorflow'
```
**Solution**: Install dependencies:
```bash
pip install tensorflow joblib scikit-learn
```

---

## 🎤 Demo Script

### **For Presentation**:

```
"Now let me demonstrate our email phishing detection system..."

[Open model.py]
"This is our LSTM neural network trained on 5,000+ emails"

[Show GUI]
"Here's a simple interface to test emails"

[Test legitimate email]
"First, a normal team meeting email..."
[Result: No Phishing]
"Correctly identified as safe"

[Test phishing email]
"Now, a suspicious email about account compromise..."
[Result: Phishing Detected]
"The model correctly identifies this as phishing!"

[Show test script]
"We can also run automated tests..."
[Run: python test_email_phishing.py]
"Multiple test cases, showing 90%+ accuracy"
```

---

## 📈 Technical Details

### **Model Architecture**:
- **Type**: LSTM Neural Network
- **Layers**: Embedding → LSTM(64) → LSTM(32) → Dense
- **Training**: 5,000+ spam/ham emails
- **Accuracy**: ~90% on test set

### **Features**:
- Text tokenization
- Sequence padding
- Binary classification (phishing/legitimate)
- Probability scoring

---

*Choose the method that works best for your demonstration!*


