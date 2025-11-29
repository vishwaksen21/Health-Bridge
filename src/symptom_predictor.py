import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV  # QUICK WIN #3: Probability calibration
import joblib
import re
import os

# ---------- Text Cleaning ----------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ---------- Dataset Preprocessing ----------
def preprocess_kaggle_dataset(data_path):
    df = pd.read_csv(data_path)

    # Check if already in correct format (symptom_text, disease)
    if 'symptom_text' in df.columns and 'disease' in df.columns:
        print(f"✅ Dataset already in correct format")
        df['symptom_text'] = df['symptom_text'].apply(clean_text)
        df = df[df['symptom_text'].str.strip().str.len() > 0]
        print(f"✅ Preprocessed {len(df)} rows | {df['disease'].nunique()} unique diseases")
        return df[['symptom_text', 'disease']]
    
    # Find label column (for Kaggle format datasets)
    label_col = None
    for col in df.columns:
        if col.lower().strip() == "prognosis":
            label_col = col
            break
    if not label_col:
        raise ValueError("❌ Dataset must have either ('symptom_text', 'disease') or 'prognosis' column!")

    # Symptom columns = all except prognosis
    symptom_cols = [c for c in df.columns if c != label_col]

    # Convert each row to readable text: take column names where value != 0
    def row_to_text(row):
        active = [symptom_cols[i].replace('_', ' ')
                  for i, val in enumerate(row[symptom_cols].values)
                  if str(val).strip() != '0']
        return ' '.join(active)

    df['symptom_text'] = df.apply(row_to_text, axis=1)
    df.rename(columns={label_col: 'disease'}, inplace=True)

    # Clean & remove empties
    df['symptom_text'] = df['symptom_text'].apply(clean_text)
    df = df[df['symptom_text'].str.strip().str.len() > 0]

    print(f"✅ Preprocessed {len(df)} rows | {df['disease'].nunique()} unique diseases")
    return df[['symptom_text', 'disease']]

# ---------- Model Training ----------
def train_symptom_model(data_path="data/symptom_disease.csv", out_path="data/symptom_model.pkl"):
    df = preprocess_kaggle_dataset(data_path)

    # QUICK WIN #2: Bigrams to capture multi-word phrases ("chest pain", "sore throat")
    vectorizer = TfidfVectorizer(
        max_features=8000,  # Increased from 5000 for better coverage
        ngram_range=(1, 2),  # Captures single words + bigrams
        stop_words='english'
    )
    X = vectorizer.fit_transform(df['symptom_text'])
    y = df['disease']

    # QUICK WIN #1: Class balancing to handle imbalanced disease distribution
    base_model = LogisticRegression(
        max_iter=1000,  # Increased iterations for convergence
        class_weight='balanced',  # Automatically adjust weights inversely proportional to class frequencies
        random_state=42
    )
    
    # QUICK WIN #3: Probability calibration using Platt scaling
    # This makes confidence scores more reliable and better calibrated
    print("🔧 Applying probability calibration (Platt scaling)...")
    model = CalibratedClassifierCV(
        base_model,
        method='sigmoid',  # Platt scaling - fits sigmoid to map scores to probabilities
        cv=5,  # 5-fold cross-validation for calibration
        n_jobs=-1  # Use all CPU cores
    )
    model.fit(X, y)
    print("✅ Model calibrated successfully!")

    os.makedirs("data", exist_ok=True)
    joblib.dump((vectorizer, model), out_path)
    print(f"✅ Symptom → Disease model trained and saved to {out_path}")

# ---------- Prediction ----------
def predict_disease(prompt, model_path="data/symptom_model.pkl"):
    """
    Predict disease from user input.
    Handles both symptom descriptions and direct disease names.
    Includes fuzzy matching for typos.
    
    Args:
        prompt: User input (symptoms or disease name)
        model_path: Path to trained model
    
    Returns:
        Tuple of (disease, confidence)
    """
    
    from difflib import SequenceMatcher
    
    vectorizer, model = joblib.load(model_path)
    prompt_clean = clean_text(prompt)
    
    # Step 1: Try to match against known disease names directly
    # This handles cases like "I have diabetes", "type 2 diabetes", etc.
    known_diseases = [
        'diabetes', 'fever', 'cancer', 'inflammation',
        'heart disease', 'asthma', 'depression', 'covid', 
        'bronchitis', 'malaria', 'impetigo', 'gerd', 'dengue',
        'bronchial asthma', 'gastric', 'hepatitis', 'pneumonia',
        'thyroid', 'migraine', 'arthritis', 'eczema', 'psoriasis',
        'acne', 'hypertension', 'high blood pressure', 'low blood pressure',
        'hypotension', 'jaundice', 'chickenpox', 'measles', 'mumps',
        'chest pain', 'heart attack', 'shortness of breath', 'cough',
        'cold', 'flu', 'diarrhea', 'constipation', 'headache',
        'nausea', 'vomiting', 'weakness', 'fatigue', 'anxiety'
    ]
    
    prompt_lower = prompt_clean.lower()
    
    # Check for exact disease name matches
    for known_disease in known_diseases:
        if known_disease in prompt_lower:
            # Found a direct match - boost confidence
            return known_disease.title(), 0.95
    
    # Step 2: Fuzzy matching for typos (e.g., "diabities" → "diabetes")
    # Split prompt into words and try to match each word against known diseases
    words = prompt_lower.split()
    best_match = None
    best_ratio = 0.7  # Threshold for similarity
    
    for word in words:
        for known_disease in known_diseases:
            # Calculate similarity between word and disease
            ratio = SequenceMatcher(None, word, known_disease).ratio()
            
            # Also check if word contains disease or disease contains word
            if known_disease in word or word in known_disease:
                ratio = 0.95
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = known_disease
    
    if best_match:
        # Found a fuzzy match
        return best_match.title(), round(best_ratio, 3)
    
    # Step 3: If no direct or fuzzy match, use the ML model for symptom-based prediction
    X = vectorizer.transform([prompt_clean])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X).max()
    
    # QUICK WIN #4: Low confidence warning
    # If model is uncertain (confidence < 0.45), flag it for user awareness
    confidence = round(proba, 3)
    
    return pred, confidence

# ---------- Main ----------
if __name__ == "__main__":
    train_symptom_model()
    test_prompt = "I have cough and fever with throat pain"
    disease, confidence = predict_disease(test_prompt)
    print(f"🧠 Predicted Disease: {disease} (confidence {confidence})")
