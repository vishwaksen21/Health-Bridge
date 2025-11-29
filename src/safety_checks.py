"""
Medical Safety Checks Module
QUICK WIN #4: Emergency detection and confidence warnings
"""

def check_emergency_keywords(user_input: str) -> dict:
    """
    QUICK WIN #4A: Emergency Detection
    
    Detects life-threatening symptoms that require immediate medical attention.
    
    Args:
        user_input: Raw user input text
        
    Returns:
        dict with 'is_emergency' (bool) and 'message' (str)
    """
    
    text_lower = user_input.lower().strip()
    
    # Critical emergency keywords
    emergency_keywords = [
        'chest pain',
        'heart attack',
        'severe chest pain',
        'crushing chest pain',
        'chest pressure',
        'heart feels like',  # covers "heart feels like it's being crushed"
        'stroke',
        'can\'t breathe',
        'cannot breathe',
        'difficulty breathing',
        'choking',
        'severe bleeding',
        'heavy bleeding',
        'bleeding heavily',
        'unconscious',
        'loss of consciousness',
        'passed out',
        'suicide',
        'suicidal',
        'kill myself',
        'end my life',
        'seizure',
        'convulsion',
        'anaphylaxis',
        'severe allergic reaction',
        'throat closing',
        'can\'t swallow',
        'severe burn',
        'severe trauma',
        'head injury',
        'severe head pain',
        'worst headache of my life',
        'sudden severe headache',
        'coughing blood',
        'coughing up blood',
        'vomiting blood',
        'blood in vomit',
        'blood in stool',
        'severe abdominal pain',
        'sudden vision loss',
        'sudden paralysis',
        'numbness on one side',
        'slurred speech',
        'confusion and fever',
        'stiff neck and fever',
        'severe dehydration'
    ]
    
    # Check for emergency keywords
    for keyword in emergency_keywords:
        if keyword in text_lower:
            return {
                'is_emergency': True,
                'message': """
╔═══════════════════════════════════════════════════════════════════╗
║                    🚨 MEDICAL EMERGENCY DETECTED 🚨                ║
╚═══════════════════════════════════════════════════════════════════╝

⚠️  Your symptoms may indicate a LIFE-THREATENING condition.

🏥 CALL EMERGENCY SERVICES IMMEDIATELY:
   
   • India: 102 / 108 / 112
   • US: 911
   • UK: 999
   • EU: 112
   
⏰ Time is critical. Do NOT:
   ✗ Wait to see if symptoms improve
   ✗ Drive yourself to the hospital
   ✗ Rely on this app for emergency medical advice
   
👉 Call emergency services NOW and follow dispatcher instructions.

═══════════════════════════════════════════════════════════════════
"""
            }
    
    return {'is_emergency': False, 'message': ''}


def check_confidence_threshold(confidence: float, threshold: float = 0.45) -> dict:
    """
    QUICK WIN #4B: Low Confidence Warning
    
    Warns users when the model's prediction is uncertain.
    
    Args:
        confidence: Model's confidence score (0.0 to 1.0)
        threshold: Minimum confidence threshold (default: 0.45)
        
    Returns:
        dict with 'show_warning' (bool) and 'message' (str)
    """
    
    if confidence < threshold:
        confidence_pct = int(confidence * 100)
        return {
            'show_warning': True,
            'message': f"""
╔═══════════════════════════════════════════════════════════════════╗
║                    ⚠️  LOW CONFIDENCE WARNING                      ║
╚═══════════════════════════════════════════════════════════════════╝

🔍 The system's confidence in this diagnosis is LOW ({confidence_pct}%)

This could mean:
  • Your symptoms don't clearly match a known condition
  • The description is too vague or incomplete
  • You may have a rare or complex condition

🏥 RECOMMENDATION: Consult a healthcare professional

A doctor can:
  ✓ Perform a physical examination
  ✓ Order appropriate diagnostic tests
  ✓ Provide accurate diagnosis and treatment
  
⚕️  Do NOT rely solely on this prediction for medical decisions.

═══════════════════════════════════════════════════════════════════
"""
        }
    
    return {'show_warning': False, 'message': ''}


def add_medical_disclaimer() -> str:
    """
    Standard medical disclaimer for all outputs.
    
    Returns:
        Formatted disclaimer text
    """
    return """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚕️  MEDICAL DISCLAIMER

This is an AI-powered informational tool only.

✓ Always consult a qualified healthcare professional
✓ Do not use for diagnosis or treatment decisions  
✓ Herbal remedies can interact with medications
✓ Individual results may vary
✓ If symptoms persist or worsen, seek immediate medical care

This tool does NOT replace professional medical advice, diagnosis, 
or treatment. Always seek the advice of your physician or other 
qualified health provider with questions about a medical condition.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def check_all_safety_measures(user_input: str, confidence: float) -> dict:
    """
    Run all safety checks in one call.
    
    Args:
        user_input: User's symptom description
        confidence: Model's confidence score
        
    Returns:
        dict with:
            - 'emergency': emergency check result
            - 'low_confidence': confidence check result
            - 'disclaimer': standard disclaimer
            - 'should_proceed': bool (False if emergency detected)
    """
    
    emergency_check = check_emergency_keywords(user_input)
    confidence_check = check_confidence_threshold(confidence)
    
    return {
        'emergency': emergency_check,
        'low_confidence': confidence_check,
        'disclaimer': add_medical_disclaimer(),
        'should_proceed': not emergency_check['is_emergency']
    }
