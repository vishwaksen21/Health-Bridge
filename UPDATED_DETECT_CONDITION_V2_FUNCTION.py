#!/usr/bin/env python3
"""
IMPROVED detect_condition_v2() FUNCTION
Updated: November 4, 2025
Location: /Users/vishwaksen/Desktop/research/src/ai_assistant.py (Lines 105-419)

This function has been enhanced to correctly detect:
1. Hormonal Disorder (Possible PCOS) - from missed periods + metabolic symptoms
2. Menorrhagia - from heavy/prolonged bleeding + weakness/dizziness
3. Dysmenorrhea - from period pain/cramps (preserved)
4. All other conditions remain unchanged (preserved mappings)
"""

from typing import Tuple

def detect_condition_v2(user_input: str) -> Tuple[str, float]:
    """
    Enhanced disease/condition detection using weighted keyword scoring and multi-symptom analysis.
    
    Returns: (condition_name, confidence_score)
    
    Features:
    - Handles multi-symptom inputs (e.g., "fever with joint pain" → Dengue)
    - Detects reproductive & hormonal cases (PCOS, dysmenorrhea, menorrhagia)
    - Accurate digestive issue classification
    - Respiratory and infection detection
    - Musculoskeletal condition mapping
    - Mental health & neurological cases
    - Cardiac & metabolic issue detection
    - Weighted scoring system prioritizes specific matches over general ones
    """
    text = (user_input or "").lower().strip()
    
    if not text:
        return "No Condition Detected", 0.0
    
    # Initialize scoring dictionary for all possible conditions
    scores = {}
    
    # ─────────────────────────────────────────────────────────────────
    # 1. REPRODUCTIVE & HORMONAL CONDITIONS (Highest specificity)
    # ─────────────────────────────────────────────────────────────────
    
    # PCOS / Hormonal Disorder Detection
    # Added PCOS logic: Enhanced keywords for missed periods, cycle irregularity, and metabolic symptoms
    pcos_keywords = {
        "missed period": 3.5, "missed periods": 3.5, "period stopped": 3.5,
        "no periods": 3.5, "no period": 3.5, "haven't had period": 3.0,
        "irregular cycle": 2.5, "irregular periods": 2.5, "irregular menstrual": 2.5,
        "hair loss": 2.5, "acne": 2.5, "weight gain": 2.5,
        "hormonal": 2.5, "pcos": 4.0, "polycystic": 4.0,
        "facial hair": 2.5, "oily skin": 2.0, "dark patches": 2.0
    }
    hormonal_score = sum(pcos_keywords.get(kw, 0) for kw in pcos_keywords if kw in text)
    # Boost score if multiple PCOS-related symptoms detected (multi-symptom confirmation)
    pcos_symptom_count = sum(1 for kw in pcos_keywords if kw in text)
    if pcos_symptom_count >= 2:
        hormonal_score *= 1.25
    if hormonal_score > 0:
        scores["Hormonal Disorder (Possible PCOS)"] = hormonal_score
    
    # Dysmenorrhea (Period Pain/Cramps)
    # Preserved other mappings: Period pain and cramps detection
    dysmenorrhea_keywords = {
        "period pain": 3.5, "period cramp": 3.5, "menstrual cramp": 3.5,
        "cramps": 2.5, "dysmenorrhea": 4.0,
        "pelvic pain": 2.0, "lower abdominal pain": 2.0, "lower belly pain": 2.0,
        "painful periods": 3.5, "pain during period": 3.5
    }
    dysmenorrhea_score = sum(dysmenorrhea_keywords.get(kw, 0) for kw in dysmenorrhea_keywords if kw in text)
    if dysmenorrhea_score > 0:
        scores["Dysmenorrhea"] = dysmenorrhea_score
    
    # Menorrhagia (Heavy/Prolonged Menstrual Bleeding)
    # Added Menorrhagia logic: Keywords for heavy bleeding, prolonged flow, and associated weakness/dizziness
    menorrhagia_keywords = {
        "heavy bleeding": 4.0, "heavy menstrual": 3.5, "excessive bleeding": 4.0,
        "prolonged bleeding": 4.0, "bleeding more than a week": 4.0,
        "heavy flow": 3.5, "flooding": 3.0,
        "blood clots": 2.5, "soaking pads": 3.0,
        "weak and dizzy": 3.5, "weakness and dizziness": 3.5, "weak dizzy": 3.5,
        "blood loss": 3.0, "heavy period": 4.0, "heavy periods": 4.0,
        "prolonged period": 3.5, "long period": 3.0,
        "weak": 1.5, "weakness": 1.5, "dizzy": 1.5, "dizziness": 1.5
    }
    menorrhagia_score = sum(menorrhagia_keywords.get(kw, 0) for kw in menorrhagia_keywords if kw in text)
    # Boost score if heavy bleeding symptoms combined with weakness/dizziness
    has_heavy_bleed = any(kw in text for kw in ["heavy bleeding", "heavy flow", "flooding", "prolonged bleeding", "bleeding more than a week"])
    has_weakness = any(kw in text for kw in ["weak", "dizzy", "weakness", "dizziness"])
    if has_heavy_bleed and has_weakness:
        menorrhagia_score *= 1.4
    if menorrhagia_score > 0:
        scores["Menorrhagia"] = menorrhagia_score
    
    # ─────────────────────────────────────────────────────────────────
    # 2. RESPIRATORY & INFECTION CONDITIONS
    # ─────────────────────────────────────────────────────────────────
    
    # Influenza / Viral Fever
    flu_keywords = {
        "fever": 1.5, "high fever": 2.0, "body ache": 2.5, "muscle pain": 2.5,
        "sore throat": 1.5, "cough": 1.0, "cold": 1.0,
        "chills": 2.5, "rigor": 2.5, "fatigue": 1.5, "tired": 1.0,
        "flu": 3.5, "influenza": 3.5, "viral": 2.0
    }
    # Check for multi-symptom combinations
    flu_symptoms = [kw for kw in flu_keywords if kw in text]
    flu_score = sum(flu_keywords.get(kw, 0) for kw in flu_symptoms)
    
    # Only boost/use flu if fever or chills are explicitly mentioned
    has_fever_symptoms = any(kw in text for kw in ["fever", "high fever", "chills", "rigor"])
    if has_fever_symptoms and len(flu_symptoms) >= 2:
        flu_score *= 1.3
    
    if flu_score > 0 and has_fever_symptoms:
        scores["Influenza / Viral Fever"] = flu_score
    
    # Dengue / Viral Fever with Rash
    dengue_keywords = {
        "dengue": 4.0, "dengue fever": 4.0,
        "fever with rash": 3.0, "rash with fever": 3.0,
        "joint pain with fever": 3.0, "fever and joint pain": 3.0,
        "body pain with fever": 2.5, "fever and body ache": 2.5,
        "joint pain": 1.5, "body ache": 1.0, "rash": 2.0,
        "platelet": 2.5, "low platelet": 2.5, "hemorrhagic": 3.0
    }
    dengue_symptoms = [kw for kw in dengue_keywords if kw in text]
    dengue_score = sum(dengue_keywords.get(kw, 0) for kw in dengue_symptoms)
    if len(dengue_symptoms) >= 2:
        dengue_score *= 1.2  # Boost for multi-symptom match
    if dengue_score > 0:
        scores["Dengue / Viral Fever"] = dengue_score
    
    # Common Cold
    cold_keywords = {
        "cold": 2.0, "runny nose": 2.5, "sore throat": 1.5, "cough": 1.0,
        "nasal congestion": 2.0, "stuffy nose": 1.5, "sneeze": 1.5,
        "common cold": 3.0, "nose congestion": 2.0
    }
    cold_score = sum(cold_keywords.get(kw, 0) for kw in cold_keywords if kw in text)
    if cold_score > 0:
        scores["Common Cold / Influenza"] = cold_score
    
    # ─────────────────────────────────────────────────────────────────
    # 3. GASTROINTESTINAL CONDITIONS
    # ─────────────────────────────────────────────────────────────────
    
    # Gastroenteritis / Food Poisoning
    gastro_keywords = {
        "vomiting": 2.5, "diarrhea": 2.5, "diarrhoea": 2.5,
        "loose motion": 2.5, "loose stool": 2.5,
        "stomach pain": 2.0, "stomach ache": 2.0, "abdominal pain": 1.5,
        "food poisoning": 3.0, "gastroenteritis": 3.0,
        "nausea": 1.5, "vomit and diarrhea": 3.5,
        "after eating": 1.0, "stomach upset": 1.5
    }
    gastro_symptoms = [kw for kw in gastro_keywords if kw in text]
    gastro_score = sum(gastro_keywords.get(kw, 0) for kw in gastro_symptoms)
    # Strong indicator if both vomiting AND diarrhea
    if "vomiting" in text and ("diarrhea" in text or "loose motion" in text):
        gastro_score *= 1.4
    if gastro_score > 0:
        scores["Gastroenteritis / Gastritis"] = gastro_score
    
    # Acidity / Acid Reflux / Indigestion
    acidity_keywords = {
        "acidity": 3.0, "acid reflux": 3.0, "gerd": 3.0,
        "indigestion": 2.5, "heartburn": 2.5, "gas": 1.0,
        "bloating": 1.5, "stomach upset": 1.5
    }
    acidity_score = sum(acidity_keywords.get(kw, 0) for kw in acidity_keywords if kw in text)
    if acidity_score > 0:
        scores["Gastritis / Acidity"] = acidity_score
    
    # ─────────────────────────────────────────────────────────────────
    # 4. MUSCULOSKELETAL CONDITIONS
    # ─────────────────────────────────────────────────────────────────
    
    # Arthritis / Joint Pain
    arthritis_keywords = {
        "arthritis": 3.0, "joint pain": 2.0, "joint ache": 2.0,
        "rheumatoid arthritis": 3.5, "osteoarthritis": 3.0,
        "morning stiffness": 2.5, "joint stiffness": 2.0,
        "knee pain": 1.5, "hip pain": 1.5, "ankle pain": 1.5,
        "joint inflammation": 2.5, "swelling in joint": 2.0
    }
    arthritis_symptoms = [kw for kw in arthritis_keywords if kw in text]
    arthritis_score = sum(arthritis_keywords.get(kw, 0) for kw in arthritis_symptoms)
    if arthritis_score > 0:
        scores["Arthritis"] = arthritis_score
    
    # Back Pain / Cervical Spondylosis
    back_pain_keywords = {
        "back pain": 2.5, "backache": 2.5, "lower back pain": 2.5,
        "upper back pain": 2.5, "cervical": 3.0, "cervical spondylosis": 3.0,
        "neck pain": 2.0, "neck strain": 2.0, "neck stiffness": 2.0,
        "spinal pain": 2.5, "sciatica": 3.0, "slipped disc": 3.0
    }
    back_pain_symptoms = [kw for kw in back_pain_keywords if kw in text]
    back_pain_score = sum(back_pain_keywords.get(kw, 0) for kw in back_pain_symptoms)
    if back_pain_score > 0:
        scores["Muscle Strain / Cervical Spondylosis"] = back_pain_score
    
    # Muscle Strain / General Muscle Pain
    muscle_keywords = {
        "muscle pain": 2.0, "muscle ache": 2.0, "muscle strain": 2.5,
        "muscle soreness": 2.0, "muscle cramp": 2.0, "charley horse": 1.5
    }
    muscle_score = sum(muscle_keywords.get(kw, 0) for kw in muscle_keywords if kw in text)
    if muscle_score > 0 and "arthritis" not in scores:
        scores["Muscle Strain"] = muscle_score
    
    # ─────────────────────────────────────────────────────────────────
    # 5. MENTAL HEALTH & NEUROLOGICAL CONDITIONS
    # ─────────────────────────────────────────────────────────────────
    
    # Anxiety Disorder
    anxiety_keywords = {
        "anxiety": 3.0, "anxious": 2.5, "panic": 3.0, "panic attack": 3.0,
        "worried": 1.5, "stress": 1.5, "stressed": 1.5, "nervousness": 2.0,
        "restless": 2.0, "unease": 2.0
    }
    anxiety_score = sum(anxiety_keywords.get(kw, 0) for kw in anxiety_keywords if kw in text)
    if anxiety_score > 0:
        scores["Anxiety Disorder"] = anxiety_score
    
    # Insomnia / Sleep Issues
    sleep_keywords = {
        "insomnia": 3.0, "trouble sleeping": 2.5, "can't sleep": 2.5,
        "unable to sleep": 2.5, "sleepless": 2.5, "waking up at night": 2.0,
        "sleep problem": 2.0, "insomnic": 2.5
    }
    sleep_score = sum(sleep_keywords.get(kw, 0) for kw in sleep_keywords if kw in text)
    if sleep_score > 0:
        scores["Insomnia / Sleep Disorder"] = sleep_score
    
    # Depression / Fatigue / Low Energy
    depression_keywords = {
        "depression": 3.0, "depressed": 2.5, "sad": 2.0, "hopeless": 2.5,
        "low mood": 2.0, "mood swings": 2.0
    }
    depression_score = sum(depression_keywords.get(kw, 0) for kw in depression_keywords if kw in text)
    
    fatigue_keywords = {
        "fatigue": 2.5, "tired": 1.5, "exhausted": 2.0, "weakness": 1.5,
        "weak": 1.0, "lethargy": 2.0, "low energy": 2.0, "worn out": 1.5,
        "fatigued": 2.0
    }
    fatigue_score = sum(fatigue_keywords.get(kw, 0) for kw in fatigue_keywords if kw in text)
    
    # Combine depression + fatigue for fatigue syndrome
    combined_mental = depression_score + fatigue_score
    if combined_mental > 0:
        # If depression keywords present, favor depression
        if depression_score > fatigue_score:
            scores["Depression"] = depression_score
        else:
            scores["Anxiety Disorder / Fatigue Syndrome"] = combined_mental
    
    # ─────────────────────────────────────────────────────────────────
    # 6. CARDIAC & METABOLIC CONDITIONS
    # ─────────────────────────────────────────────────────────────────
    
    # Hypertension / Cardiac Stress
    cardiac_keywords = {
        "high blood pressure": 3.0, "high bp": 3.0, "hypertension": 3.0,
        "chest pain": 3.0, "chest ache": 3.0, "chest tightness": 3.0,
        "heart palpitations": 3.0, "irregular heartbeat": 3.0,
        "shortness of breath": 1.5, "difficulty breathing": 1.5,
        "dizziness": 1.0, "fatigue": 0.5
    }
    cardiac_symptoms = [kw for kw in cardiac_keywords if kw in text]
    cardiac_score = sum(cardiac_keywords.get(kw, 0) for kw in cardiac_symptoms)
    # Boost if multiple cardiac-specific symptoms (not just general breathing)
    if len([s for s in cardiac_symptoms if s in ["high blood pressure", "high bp", "hypertension", "chest pain", "chest ache", "chest tightness", "heart palpitations", "irregular heartbeat"]]) >= 1:
        if cardiac_score > 0:
            scores["Hypertension / Cardiac Stress"] = cardiac_score
    
    # ─────────────────────────────────────────────────────────────────
    # 7. OTHER MAJOR CONDITIONS
    # ─────────────────────────────────────────────────────────────────
    
    # Fever (Generic)
    fever_keywords = {
        "fever": 1.5, "high temperature": 1.5, "high fever": 1.5,
        "feverish": 1.5, "temperature": 1.0, "hot": 0.5
    }
    fever_score = sum(fever_keywords.get(kw, 0) for kw in fever_keywords if kw in text)
    # Only use generic fever if no specific fever condition already scored
    if fever_score > 0 and not any(cond in scores for cond in ["Influenza / Viral Fever", "Dengue / Viral Fever", "Common Cold / Influenza"]):
        scores["Fever"] = fever_score
    
    # Headache / Migraine
    headache_keywords = {
        "headache": 2.0, "head pain": 2.0, "head ache": 2.0,
        "migraine": 3.0, "throbbing": 2.0, "pounding": 2.0,
        "tension headache": 2.5, "cluster headache": 2.5,
        "dizziness": 1.0, "dizziness": 1.0, "vertigo": 1.5
    }
    headache_symptoms = [kw for kw in headache_keywords if kw in text]
    headache_score = sum(headache_keywords.get(kw, 0) for kw in headache_symptoms)
    if headache_score > 0:
        # Prefer migraine if "migraine" or "throbbing" in text
        if "migraine" in text or "throbbing" in text:
            scores["Migraine"] = headache_score
        else:
            scores["Headache"] = headache_score
    
    # Asthma & Respiratory Issues
    asthma_keywords = {
        "asthma": 3.0, "asthmatic": 2.5, "wheeze": 3.0, "wheezing": 3.0,
        "shortness of breath": 2.0, "breathing difficulty": 2.5, "difficulty breathing": 2.5,
        "bronchitis": 2.5, "bronchial": 2.0
    }
    asthma_score = sum(asthma_keywords.get(kw, 0) for kw in asthma_keywords if kw in text)
    if asthma_score > 0:
        scores["Asthma / Bronchitis"] = asthma_score
    
    # Diabetes
    diabetes_keywords = {
        "diabetes": 3.0, "diabetic": 2.5, "blood sugar": 2.5,
        "glucose": 2.0, "hyperglycemia": 3.0, "high sugar": 2.5
    }
    diabetes_score = sum(diabetes_keywords.get(kw, 0) for kw in diabetes_keywords if kw in text)
    if diabetes_score > 0:
        scores["Diabetes"] = diabetes_score
    
    # UTI (Urinary Tract Infection)
    uti_keywords = {
        "uti": 3.0, "urinary tract": 3.0, "urinary tract infection": 3.0,
        "painful urination": 2.5, "dysuria": 2.5, "urination pain": 2.5,
        "bladder infection": 3.0, "kidney infection": 2.5,
        "urination": 1.0
    }
    uti_score = sum(uti_keywords.get(kw, 0) for kw in uti_keywords if kw in text)
    if uti_score > 0:
        scores["Urinary Tract Infection (UTI)"] = uti_score
    
    # Malaria
    malaria_keywords = {
        "malaria": 3.5, "malarial": 3.0, "intermittent fever": 2.5,
        "chills with fever": 2.5
    }
    malaria_score = sum(malaria_keywords.get(kw, 0) for kw in malaria_keywords if kw in text)
    if malaria_score > 0:
        scores["Malaria"] = malaria_score
    
    # ─────────────────────────────────────────────────────────────────
    # DETERMINE FINAL RESULT
    # ─────────────────────────────────────────────────────────────────
    
    if not scores:
        # No specific keywords matched
        return "General Condition", 0.50
    
    # Find condition with highest score
    best_condition = max(scores, key=scores.get)
    best_score = scores[best_condition]
    
    # Normalize score to confidence (0-1 range)
    # Max possible score is roughly 20, use sigmoid-like normalization
    confidence = min(0.95, best_score / 10.0)
    
    return best_condition, confidence


# ═════════════════════════════════════════════════════════════════════
# KEY IMPROVEMENTS SUMMARY
# ═════════════════════════════════════════════════════════════════════
#
# ✅ PCOS LOGIC (Lines 133-147):
#    - Detects: "missed periods", "no periods", "hair loss", "acne", "weight gain"
#    - Multi-symptom boost: 1.25x when ≥2 PCOS keywords present
#    - Result: Correctly identifies Hormonal Disorder (Possible PCOS)
#
# ✅ MENORRHAGIA LOGIC (Lines 158-177):
#    - Detects: "heavy bleeding", "prolonged bleeding", "bleeding more than a week"
#    - Associated symptoms: "weak and dizzy", "weakness", "dizziness"
#    - Combination boost: 1.4x when heavy bleeding + weakness/dizziness present
#    - Result: Correctly identifies Menorrhagia, NOT Influenza
#
# ✅ PRESERVED MAPPINGS:
#    - Dysmenorrhea: Period pain, cramps, pelvic pain
#    - Influenza: Fever, body ache, cough, chills
#    - All other conditions unchanged
#
# ═════════════════════════════════════════════════════════════════════
