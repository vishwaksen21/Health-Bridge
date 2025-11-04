"""
Enhanced Disease Predictor with Travel Context Awareness
Improves on basic model by detecting patterns, context, and asking clarifying questions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from symptom_predictor import predict_disease as base_predict
from typing import Dict, List, Tuple

# Common symptom patterns - expanded to handle frequent queries
TRAVEL_PATTERNS = {
    # Travel/Exertion related
    "general_malaise": {
        "keywords": ["not feeling", "not well", "unwell", "tired", "weak", "proper", "trek", "trekking", "exhausted", "fatigue", "worn out"],
        "likely_diseases": ["Typhoid", "Malaria", "Dengue", "Typhus"],
        "severity": "🔴 HIGH",
        "clarification": "Do you have fever, body ache, or headache?"
    },
    
    # High fever (VERY COMMON)
    "high_fever": {
        "keywords": ["fever", "high fever", "temperature", "hot", "burning", "feverish", "temp", "degree", "fevr", "feber"],
        "likely_diseases": ["Malaria", "Dengue", "Typhoid", "Influenza"],
        "severity": "🔴 HIGH",
        "clarification": "How high is your temperature (°F/°C)? Any chills? Body ache?"
    },
    
    # Cough & Cold (VERY COMMON)
    "cough_cold": {
        "keywords": ["cough", "cold", "sneezing", "sneeze", "runny nose", "nasal", "stuffy", "sore throat", "throat", "hoarse", "rough", "coough", "colud", "sneze", "nosee"],
        "likely_diseases": ["Common Cold", "Pharyngitis", "Rhinitis", "Laryngitis"],
        "severity": "� LOW",
        "clarification": "Dry cough or wet? Any phlegm color? When started?"
    },
    
    # Headache (VERY COMMON)
    "headache": {
        "keywords": ["headache", "head pain", "head", "migraine", "tension", "migrane", "headeache", "ache in head", "dizziness", "dizzy", "vertigo"],
        "likely_diseases": ["Migraine", "Tension Headache", "Hypertension", "Sinusitis"],
        "severity": "� MODERATE",
        "clarification": "Throbbing or constant? One side or both? Nausea? Sensitivity to light?"
    },
    
    # Body Ache (VERY COMMON)
    "body_ache": {
        "keywords": ["ache", "muscle", "pain", "body ache", "body pain", "joint", "limb", "back pain", "back ache", "shoulder", "knee", "ankle", "wrist", "elbow", "mussel", "bady", "acke", "painn"],
        "likely_diseases": ["Influenza", "Dengue", "Malaria", "Rheumatoid Arthritis"],
        "severity": "🟡 MODERATE",
        "clarification": "Where exactly? Constant or intermittent? Fever? Swelling?"
    },
    
    # Stomach/Digestive (VERY COMMON)
    "digestive_issues": {
        "keywords": ["stomach", "belly", "diarrhea", "loose", "motion", "constipation", "vomiting", "nausea", "gastric", "acidity", "acid reflux", "stomuch", "bellly", "stomache", "diarea", "vomit"],
        "likely_diseases": ["Gastroenteritis", "Acid Reflux", "Appendicitis", "Crohn's Disease"],
        "severity": "� MODERATE",
        "clarification": "Constant or cramping? Any blood? Fever? When did it start?"
    },
    
    # Food Poisoning (VERY COMMON)
    "food_poisoning": {
        "keywords": ["poison", "food", "ate", "eaten", "contaminated", "spoiled", "restaurant", "restarant", "food poison", "sick after food", "vomiting after food", "diarrhea after food"],
        "likely_diseases": ["Food Poisoning", "Gastroenteritis", "E. coli", "Salmonella"],
        "severity": "� MODERATE",
        "clarification": "When did you eat? Vomiting? Diarrhea? Fever? Abdominal pain?"
    },
    
    # Flu/Viral (VERY COMMON)
    "flu_viral": {
        "keywords": ["flu", "viral", "infection", "virus", "sick", "sickness", "ill", "illness", "malaise", "fatigue", "weakness", "weak", "tired", "weakness", "flue", "infectionn", "viruss"],
        "likely_diseases": ["Influenza", "Viral Fever", "COVID-19", "Viral Infection"],
        "severity": "🟡 MODERATE",
        "clarification": "Sudden onset? Chills? Body ache? Sore throat? Cough?"
    },
    
    # Malaria/Dengue pattern
    "malaria_dengue": {
        "keywords": ["mosquito", "mosqu", "malaria", "dengue", "dengeu", "malaria fever", "dengue fever", "viral fever", "intermittent fever"],
        "likely_diseases": ["Malaria", "Dengue", "Chikungunya", "Yellow Fever"],
        "severity": "🔴 HIGH",
        "clarification": "High fever with chills? Joint pain? Headache? Rash?"
    },
    
    # Respiratory (COMMON)
    "respiratory": {
        "keywords": ["cough", "throat", "breathing", "chest", "respiratory", "lungs", "shortness of breath", "asthma", "asthmatic", "wheezing", "wheeze", "astma", "bronc"],
        "likely_diseases": ["Bronchitis", "Pneumonia", "Tuberculosis", "Asthma"],
        "severity": "🟡 MODERATE",
        "clarification": "Dry or wet cough? High fever? Shortness of breath?"
    },
    
    # Skin issues (COMMON)
    "skin_issues": {
        "keywords": ["rash", "skin", "itch", "itching", "irritation", "allergic", "allergy", "allreged", "dermatitis", "hive", "scabies", "acne", "pimple", "scar", "rassy", "itcch"],
        "likely_diseases": ["Urticaria", "Dermatitis", "Scabies", "Psoriasis"],
        "severity": "� MODERATE",
        "clarification": "Where on body? Painful or just itchy? Red or white bumps? When started?"
    },
    
    # Traveller's Diarrhea
    "traveller_diarrhea": {
        "keywords": ["diarrhea", "travel", "abroad", "trip", "journey", "destination", "diarea", "loose motion", "loose stool", "watery"],
        "likely_diseases": ["Traveller's Diarrhea", "Gastroenteritis", "Cholera", "Typhoid"],
        "severity": "� MODERATE",
        "clarification": "Duration? Frequency? Fever? Blood in stool? When did travel happen?"
    },
    
    # Thyroid (NEW - handles typo and thyroid keywords)
    "thyroid": {
        "keywords": ["thyroid", "tyroid", "throid", "thyriod", "hypothyroid", "hyperthyroid", "thyroid issue", "thyroid problem", "thyroid disease", "gland"],
        "likely_diseases": ["Hypothyroidism", "Hyperthyroidism", "Thyroid"],
        "severity": "🟡 MODERATE",
        "clarification": "Weight gain or loss? Fatigue? Temperature sensitivity? Hair loss?"
    },
    
    # Joint/Musculoskeletal pain (NEW - IMPORTANT)
    "joint_pain": {
        "keywords": ["frozen shoulder", "shoulder pain", "shoulder", "knee pain", "knee", "joint pain", "joint", "arthritis", "osteoarthritis", "rheumatoid", "ligament", "tendon", "inflammation", "stiffness", "mobility", "range of motion", "frozen", "lock", "click"],
        "likely_diseases": ["Arthritis", "Osteoarthritis", "Rheumatoid Arthritis", "Joint Pain"],
        "severity": "🟡 MODERATE",
        "clarification": "Which joints? Duration? Swelling? Stiffness? Morning vs evening? Worse with movement?"
    },
}

TRAVEL_INDICATORS = ["travel", "trip", "abroad", "visit", "tourist", "flight", "airport", 
                     "trek", "trekking", "hiking", "hiking trip", "expedition", "vacation",
                     "overseas", "international", "journey", "adventure"]

def detect_travel_context(symptoms: str) -> bool:
    """Check if user mentions travel."""
    symptoms_lower = symptoms.lower()
    return any(indicator in symptoms_lower for indicator in TRAVEL_INDICATORS)

def find_matching_pattern(symptoms: str) -> Tuple[str, Dict]:
    """Find best matching travel/context pattern with priority ordering."""
    symptoms_lower = symptoms.lower()
    best_pattern = None
    best_match_count = 0
    
    # Priority order: more specific patterns first
    priority_patterns = [
        "joint_pain",      # Joint/musculoskeletal pain (NEW - HIGH PRIORITY)
        "cough_cold",      # Throat-related
        "respiratory",     # Breathing-related
        "thyroid",         # Thyroid-related
        "flu_viral",       # Viral indicators
        "digestive_issues", # GI-related
        "body_ache",       # Muscle pain
        "headache",        # Headache
        "high_fever",      # Generic fever
        "skin_issues",     # Skin-related
        "general_malaise", # Generic malaise
        "food_poisoning",  # Food-related
        "traveller_diarrhea", # Travel+diarrhea
        "malaria_dengue",  # Travel diseases
    ]
    
    for pattern_name in priority_patterns:
        if pattern_name not in TRAVEL_PATTERNS:
            continue
        pattern_data = TRAVEL_PATTERNS[pattern_name]
        match_count = sum(1 for keyword in pattern_data["keywords"] 
                         if keyword in symptoms_lower)
        if match_count > best_match_count:
            best_match_count = match_count
            best_pattern = (pattern_name, pattern_data)
    
    return best_pattern if best_pattern and best_match_count > 0 else (None, {})

def predict_disease_enhanced(prompt: str, model_path: str = "data/symptom_model.pkl") -> Dict:
    """
    Enhanced disease prediction with:
    - Travel context awareness
    - Pattern matching for vague symptoms
    - Clarification prompts
    - Alternative diagnoses
    
    Returns:
        Dict with: disease, confidence, pattern, alternatives, clarification, explanation
    """
    
    # First: Get base model prediction
    base_disease, base_confidence = base_predict(prompt, model_path)
    
    # Second: Detect travel context
    has_travel = detect_travel_context(prompt)
    
    # Third: Find matching pattern
    pattern_name, pattern_data = find_matching_pattern(prompt)
    
    # Fourth: Build enhanced response
    result = {
        "primary_disease": base_disease,
        "confidence": base_confidence,
        "pattern_detected": pattern_name,
        "has_travel_context": has_travel,
        "alternatives": [],
        "severity": "🟢 LOW",
        "clarification_needed": False,
        "clarification_question": "",
        "explanation": "",
        "is_vague_symptom": base_confidence < 0.7
    }
    
    # If vague symptom AND travel pattern found, override with pattern
    if base_confidence < 0.75 and pattern_name:
        result["primary_disease"] = pattern_data["likely_diseases"][0]
        result["confidence"] = 0.75  # Pattern-matched confidence
        result["alternatives"] = pattern_data["likely_diseases"][1:3]
        result["severity"] = pattern_data["severity"]
        result["clarification_needed"] = True
        result["clarification_question"] = pattern_data["clarification"]
        result["override_reason"] = "Vague symptom with strong travel pattern match"
        result["explanation"] = f"""
🔍 **PATTERN DETECTED: {pattern_name.replace('_', ' ').title()}**

⚠️ Your input is vague but matches a known pattern.
The most likely condition is **{result['primary_disease']}**.

Alternative possibilities: {', '.join(result['alternatives'])}
Severity: {result['severity']}

📌 **To provide better diagnosis, please tell me:**
{result['clarification_question']}
"""
    elif pattern_name and has_travel:
        # Travel + pattern match even with higher base confidence
        result["primary_disease"] = pattern_data["likely_diseases"][0]
        result["confidence"] = max(0.75, base_confidence * 0.9)  # Adjust confidence
        result["alternatives"] = pattern_data["likely_diseases"][1:3]
        result["severity"] = pattern_data["severity"]
        result["clarification_needed"] = False
        result["override_reason"] = "Travel context with matching pattern"
    elif pattern_name:
        # Pattern matched but no travel - use pattern if base is generic/wrong
        # Check if base model returned a non-specific disease that pattern matches better
        generic_diseases = ["Diabetes", "Heart Disease", "Acne", "Fever", "Cough", "Chest Pain", "Inflammation", "Allergy", "Influenza", "Viral Fever"]
        # Also check if pattern suggests more specific/relevant disease than base model
        mismatched_diseases = ["Malaria", "Dengue", "Typhoid", "Influenza"]  # Severe diseases often over-predicted
        
        if (base_disease in generic_diseases or base_disease in mismatched_diseases) and pattern_data["likely_diseases"]:
            # Override with pattern-matched disease for better specificity
            result["primary_disease"] = pattern_data["likely_diseases"][0]
            result["confidence"] = 0.75
            result["alternatives"] = pattern_data["likely_diseases"][1:3]
            result["severity"] = pattern_data["severity"]
            result["clarification_needed"] = True
            result["clarification_question"] = pattern_data["clarification"]
            result["override_reason"] = "Pattern match provides better diagnosis than base model result"
        else:
            result["alternatives"] = pattern_data["likely_diseases"][1:3]
            result["severity"] = pattern_data["severity"]
            result["explanation"] = f"Your symptoms suggest a {pattern_name.replace('_', ' ')} pattern."
    
    return result

def format_enhanced_prediction(result: Dict) -> str:
    """Format the enhanced prediction for display."""
    
    output = f"""
╔════════════════════════════════════════════════════════════════╗
║           🏥 ENHANCED DIAGNOSIS ANALYSIS                      ║
╚════════════════════════════════════════════════════════════════╝

📋 PRIMARY DIAGNOSIS
───────────────────────────────────────────────────────────────
Disease: {result['primary_disease']}
Confidence: {result['confidence']*100:.1f}%
Severity: {result['severity']}

📊 PATTERN ANALYSIS
───────────────────────────────────────────────────────────────
Pattern Detected: {result['pattern_detected'] or 'None (Using ML Model)'}
Travel Context: {'✓ Yes' if result['has_travel_context'] else '✗ No'}
Symptom Clarity: {'⚠️ Vague - Pattern-based' if result['is_vague_symptom'] else '✓ Clear'}

🔄 ALTERNATIVE DIAGNOSES
───────────────────────────────────────────────────────────────
"""
    
    if result['alternatives']:
        for i, alt in enumerate(result['alternatives'], 1):
            output += f"{i}. {alt}\n"
    else:
        output += "None identified\n"
    
    if result['clarification_needed']:
        output += f"""
⚠️ CLARIFICATION NEEDED
───────────────────────────────────────────────────────────────
{result['clarification_question']}

Please provide more details so we can refine the diagnosis.
"""
    
    if result['explanation']:
        output += f"""
📝 EXPLANATION
───────────────────────────────────────────────────────────────
{result['explanation']}
"""
    
    output += "\n💡 NEXT STEPS\n───────────────────────────────────────────────────────────────\n"
    
    if result['severity'].startswith('🔴 CRITICAL'):
        output += "🚨 **SEEK IMMEDIATE MEDICAL ATTENTION** - Contact a doctor or hospital now.\n"
    elif result['severity'].startswith('🔴 HIGH'):
        output += "⚠️ Schedule a medical consultation soon.\n"
    else:
        output += "ℹ️ Monitor symptoms. If they worsen, seek medical advice.\n"
    
    return output


# Test the enhanced predictor
if __name__ == "__main__":
    test_inputs = [
        "i have been travelling for longtime, now i'm not feeling proper",
        "high fever and body ache",
        "loose motion after eating street food",
        "cough and fever",
    ]
    
    print("🧳 ENHANCED SYMPTOM PREDICTOR - TEST RESULTS\n")
    print("=" * 70)
    
    for test_input in test_inputs:
        print(f"\n📝 Input: '{test_input}'\n")
        result = predict_disease_enhanced(test_input)
        print(format_enhanced_prediction(result))
        print("=" * 70)
