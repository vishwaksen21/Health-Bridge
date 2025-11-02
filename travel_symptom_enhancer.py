"""
Travel-Related Illness Detector
Handles vague symptoms common in travelers and returns context-aware recommendations
"""

from typing import List, Tuple

TRAVEL_SYMPTOM_PATTERNS = {
    # Pattern: (keywords, likely_diseases, severity)
    "traveller's_diarrhea": {
        "keywords": ["diarrhea", "loose", "stomach", "gastric", "toilet", "bathroom"],
        "diseases": ["Traveller's Diarrhea", "Gastroenteritis", "Gerd", "Typhoid"],
        "severity": "HIGH",
        "symptoms_to_ask": ["stomach pain", "vomiting", "fever", "blood in stool"]
    },
    "malaria": {
        "keywords": ["fever", "chills", "sweating", "fatigue", "headache", "body ache"],
        "diseases": ["Malaria", "Dengue", "Typhoid", "Typhus"],
        "severity": "CRITICAL",
        "symptoms_to_ask": ["high fever", "shivering", "muscle pain", "joint pain"]
    },
    "food_poisoning": {
        "keywords": ["food", "ate", "ate something", "bad food", "feeling", "not proper"],
        "diseases": ["Food Poisoning", "Gastroenteritis", "Gerd", "Typhoid"],
        "severity": "HIGH",
        "symptoms_to_ask": ["nausea", "vomiting", "stomach pain", "diarrhea"]
    },
    "general_malaise": {
        "keywords": ["not feeling", "not feeling proper", "not well", "unwell", "tired", "weak", "trek", "trekking", "exhausted", "fatigue"],
        "diseases": ["Typhoid", "Malaria", "Dengue", "Tuberculosis"],
        "severity": "HIGH",
        "symptoms_to_ask": ["fever", "headache", "body ache", "fatigue"]
    },
    "respiratory": {
        "keywords": ["cough", "throat", "respiratory", "breathing", "chest"],
        "diseases": ["Bronchitis", "Pneumonia", "Tuberculosis", "Asthma"],
        "severity": "MODERATE",
        "symptoms_to_ask": ["high fever", "cough with phlegm", "shortness of breath"]
    }
}

def detect_travel_pattern(symptoms: str) -> Tuple[List[str], str, List[str], str]:
    """
    Detect travel-related symptom patterns and suggest further questions.
    
    Args:
        symptoms: User input text
        
    Returns:
        Tuple of (likely_diseases, severity, follow_up_questions, pattern_name)
    """
    
    symptoms_lower = symptoms.lower()
    matched_pattern = None
    best_match_count = 0
    
    # Find best matching pattern
    for pattern_name, pattern_data in TRAVEL_SYMPTOM_PATTERNS.items():
        match_count = sum(1 for keyword in pattern_data["keywords"] 
                         if keyword in symptoms_lower)
        
        if match_count > best_match_count:
            best_match_count = match_count
            matched_pattern = (pattern_name, pattern_data)
    
    if matched_pattern:
        pattern_name, pattern_data = matched_pattern
        return (
            pattern_data["diseases"],
            pattern_data["severity"],
            pattern_data["symptoms_to_ask"],
            pattern_name
        )
    
    # Fallback: if no specific pattern matched but user mentions travel
    if "travel" in symptoms_lower:
        return (
            ["Typhoid", "Malaria", "Dengue", "Typhus"],
            "MODERATE",
            ["fever", "diarrhea", "headache", "body ache", "fatigue"],
            "generic_travel"
        )
    
    return ([], "UNKNOWN", [], None)

def create_clarification_prompt(pattern_name: str, follow_up_questions: List[str]) -> str:
    """Create a friendly clarification prompt for the user."""
    
    if pattern_name == "general_malaise":
        return f"""
🔍 **CLARIFICATION NEEDED**

Your symptoms suggest a general malaise, which could be several conditions common in travelers.

To help diagnose better, please tell me:
• Do you have a fever? (temperature > 100°F / 37.8°C)
• Any body aches or joint pain?
• Headache or dizziness?
• Nausea, vomiting, or stomach issues?
• Cough or respiratory symptoms?

⏰ **When did symptoms start?** (after travel, during, or after returning home?)
"""
    
    elif pattern_name == "traveller's_diarrhea":
        return f"""
🔍 **LIKELY: Traveller's Diarrhea**

Please confirm:
• How frequent is the diarrhea? (mild, moderate, severe)
• Any blood or mucus in stool?
• Abdominal pain level?
• Fever present?
• How long has this been going on?

⚠️ **URGENT**: If you see blood in stool or have severe dehydration → Seek medical attention immediately
"""
    
    else:
        questions_text = "\n• ".join(follow_up_questions)
        return f"""
🔍 **NEED MORE DETAILS**

To narrow down diagnosis, please tell me:
• {questions_text}

When did these symptoms start?
"""

def enhance_prediction_with_travel_context(
    original_disease: str,
    confidence: float,
    user_input: str
) -> Tuple[str, float, List[str], str]:
    """
    Override or enhance original prediction if travel pattern detected.
    
    Args:
        original_disease: Disease predicted by main model
        confidence: Confidence of original prediction
        user_input: User's original input
        
    Returns:
        Tuple of (disease, confidence, suggestions, explanation)
    """
    
    diseases, severity, follow_up_qs, pattern = detect_travel_pattern(user_input)
    
    # If strong travel pattern detected and confidence low, override
    if pattern and confidence < 0.7 and diseases:
        # Use top disease from pattern with adjusted confidence
        new_disease = diseases[0]
        new_confidence = 0.75  # Pattern-based confidence
        
        explanation = f"""
✅ **Travel Pattern Detected**

Your symptoms match a **{pattern.replace('_', ' ').title()}** pattern.

Most likely diagnosis: **{new_disease}** (Pattern-based, {new_confidence*100:.0f}% confidence)
Alternative possibilities: {", ".join(diseases[1:3])}

Severity Level: 🔴 {severity}
"""
        
        return new_disease, new_confidence, follow_up_qs, explanation
    
    return original_disease, confidence, [], ""


if __name__ == "__main__":
    # Test cases
    test_cases = [
        "i have been travelling for longtime, now i'm not feeling proper",
        "i ate something bad and now have loose motion",
        "high fever and chills after coming back from africa",
        "cough and throat pain during business trip",
    ]
    
    print("🧳 TRAVEL SYMPTOM PATTERN DETECTION TEST\n")
    print("=" * 70)
    
    for test_input in test_cases:
        print(f"\n📝 Input: {test_input}")
        diseases, severity, questions, pattern = detect_travel_pattern(test_input)
        prompt = create_clarification_prompt(pattern, questions)
        
        print(f"   ✓ Pattern: {pattern}")
        print(f"   ✓ Diseases: {diseases}")
        print(f"   ✓ Severity: {severity}")
        print(f"   ✓ Questions to ask: {questions[:2]}")
        print(prompt)
        print("-" * 70)
