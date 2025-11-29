#!/usr/bin/env python3
"""
Max-Expanded Standalone Terminal AI Health Assistant
- Combines herbal suggestions + pharmaceutical suggestions
- Large lookup dictionaries and embedded sample data if CSVs missing
- Keeps original logic intact; adds robustness, logging, TTS, and AI-insight fallback
"""

import os
import sys
import json
import time
import math
import datetime
from typing import Dict, List, Tuple, Set

# Optional imports; handle gracefully
try:
    import pandas as pd
except Exception:
    pd = None

try:
    import numpy as np
except Exception:
    np = None

# gensim / joblib optional for embeddings-based suggestions (kept but handled)
try:
    from gensim.models import KeyedVectors
except Exception:
    KeyedVectors = None

try:
    import joblib
except Exception:
    joblib = None

# Try to import pyttsx3 for TTS (optional)
try:
    import pyttsx3
    TTS_AVAILABLE = True
except Exception:
    pyttsx3 = None
    TTS_AVAILABLE = False

# Try to import Azure LLM client (optional)
try:
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    HAS_LLM = True
except Exception:
    HAS_LLM = False

# Preserve your import logic for symptom predictors and drug DB (fallback safe)
USE_ENHANCED = False
try:
    from .enhanced_symptom_predictor import predict_disease_enhanced
    USE_ENHANCED = True
except Exception:
    try:
        from enhanced_symptom_predictor import predict_disease_enhanced
        USE_ENHANCED = True
    except Exception:
        try:
            from .symptom_predictor import predict_disease
            USE_ENHANCED = False
        except Exception:
            try:
                from symptom_predictor import predict_disease
            except Exception:
                # Fallback simple predictor if module missing
                def predict_disease(text: str):
                    # Very simple heuristic fallback (keyword match)
                    text_l = (text or "").lower()
                    if any(k in text_l for k in ["cough", "sore throat", "runny", "congest"]):
                        return "Common Cold", 0.6
                    if any(k in text_l for k in ["fever", "chills", "rigor"]):
                        return "Fever", 0.6
                    if any(k in text_l for k in ["headache", "migraine", "throbb"]):
                        return "Headache", 0.6
                    if any(k in text_l for k in ["diarr", "loose motion", "loose stool", "vomit"]):
                        return "Gastroenteritis", 0.75
                    if any(k in text_l for k in ["breath", "wheez", "asthma"]):
                        return "Asthma", 0.6
                    return "General Symptom", 0.5
                USE_ENHANCED = False

# Drug DB fallback flag - attempt import as user original
HAS_DRUG_DB = False
try:
    from .drug_database import DrugDatabase
    HAS_DRUG_DB = True
except Exception:
    try:
        from drug_database import DrugDatabase
        HAS_DRUG_DB = True
    except Exception:
        HAS_DRUG_DB = False

# ------------------------------------------------------------------------------------
# ENHANCED condition detection (v2) with weighted scoring and multi-symptom support
# ------------------------------------------------------------------------------------
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
    # Added PCOS logic: Suppress Dysmenorrhea if PCOS indicators (missed periods + metabolic symptoms) are present
    dysmenorrhea_keywords = {
        "period pain": 3.5, "period cramp": 3.5, "menstrual cramp": 3.5,
        "cramps": 2.5, "dysmenorrhea": 4.0,
        "pelvic pain": 2.0, "lower abdominal pain": 2.0, "lower belly pain": 2.0,
        "painful periods": 3.5, "pain during period": 3.5
    }
    dysmenorrhea_score = sum(dysmenorrhea_keywords.get(kw, 0) for kw in dysmenorrhea_keywords if kw in text)
    
    # SUPPRESS Dysmenorrhea if PCOS indicators present (missed periods + metabolic symptoms)
    has_pcos_indicators = any(kw in text for kw in ["missed period", "missed periods", "no periods", "no period", "period stopped", "haven't had period"])
    has_pcos_metabolic = any(kw in text for kw in ["hair loss", "acne", "weight gain", "facial hair", "hormonal"])
    if dysmenorrhea_score > 0 and not (has_pcos_indicators and has_pcos_metabolic):
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


# ------------------------------------------------------------------------------------
# Terminal formatting helpers
# ------------------------------------------------------------------------------------
HEADER = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

def speak_text(text: str):
    """Speak using pyttsx3 if available (non-blocking-ish)."""
    if not TTS_AVAILABLE:
        return
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        # silently ignore TTS failures
        pass

# ------------------------------------------------------------------------------------
# Embedded sample data (used if CSV files are missing)
# ------------------------------------------------------------------------------------
# Minimal sample CSV-like data so script runs standalone
SAMPLE_DISEASES = [
    {"disease": "Gastroenteritis", "symptom": "Diarrhea, vomiting, stomach pain"},
    {"disease": "Common Cold", "symptom": "Runny nose, sore throat, cough"},
    {"disease": "Fever", "symptom": "Raised body temperature, chills"},
    {"disease": "Headache", "symptom": "Pain in head or neck region"},
    {"disease": "Asthma", "symptom": "Wheezing, shortness of breath"},
]

SAMPLE_HERBS = [
    {"herb": "Ginger", "benefits": "Anti-nausea, anti-inflammatory", "active_compounds": "Gingerols", "usage": "Ginger tea 1-2 cups daily"},
    {"herb": "Peppermint", "benefits": "Soothes stomach, relieves gas", "active_compounds": "Menthol", "usage": "Peppermint infusion as needed"},
    {"herb": "Turmeric", "benefits": "Anti-inflammatory", "active_compounds": "Curcumin", "usage": "250-500 mg with meals"},
    {"herb": "Neem", "benefits": "Antimicrobial", "active_compounds": "Azadirachtin", "usage": "Topical or decoction by expert"},
    {"herb": "Clove", "benefits": "Analgesic and antimicrobial", "active_compounds": "Eugenol", "usage": "Use in small amounts"}
]

SAMPLE_INGREDIENTS = [
    {"ingredient": "Ginger", "target": "Gastroenteritis"},
    {"ingredient": "Turmeric", "target": "Inflammation"},
    {"ingredient": "Eugenol", "target": "Pain"},
    {"ingredient": "Withaferin A", "target": "Immune Support"},
]

SAMPLE_TARGETS = [
    {"target": "Gastroenteritis", "disease": "Gastroenteritis"},
    {"target": "A Common Cold", "disease": "Common Cold"},
    {"target": "Fever", "disease": "Fever"},
]

SAMPLE_DRUGS = [
    {"name": "Paracetamol", "brand_names": ["Crocin", "Panadol"], "type": "Analgesic", "dosage": "500-1000 mg every 4-6h", "purpose": "Reduce fever and pain", "availability": "OTC", "price_range": "₹10-50", "side_effects": "Liver toxicity in overdose"},
    {"name": "Oral Rehydration Salts", "brand_names": ["ORS"], "type": "Oral solution", "dosage": "As directed", "purpose": "Rehydration", "availability": "OTC", "price_range": "₹20-100", "side_effects": "None if used correctly"},
    {"name": "Omeprazole", "brand_names": ["Prilosec"], "type": "Proton pump inhibitor", "dosage": "20-40 mg daily", "purpose": "Reduce stomach acid", "availability": "Prescription", "price_range": "₹40-200", "side_effects": "Headache, nausea"},
]

# ------------------------------------------------------------------------------------
# Large lookup dictionaries (spelling_map, disease_mapping, condition_info, icons)
# ------------------------------------------------------------------------------------
# This block is heavily expanded to avoid missing keys and reduce errors at runtime.
# You can extend these further by editing below.
spelling_map = {
    # common typos / variants (sample of many)
    'fevr': 'fever', 'feverr': 'fever', 'feaver': 'fever', 'feber': 'fever',
    'coough': 'cough', 'couf': 'cough', 'caugh': 'cough',
    'colud': 'cold', 'coldf': 'cold',
    'asthma': 'asthma', 'astma': 'asthma', 'asthama': 'asthma',
    'bronchitiss': 'bronchitis', 'bronchit': 'bronchitis',
    'pneumona': 'pneumonia', 'pnemonia': 'pneumonia',
    'throatt': 'throat', 'throad': 'throat', 'soar throat': 'sore throat',
    'runnynose': 'runny nose', 'sneezee': 'sneeze',
    'vommit': 'vomit', 'vommiting': 'vomiting', 'nausia': 'nausea',
    'stomuch': 'stomach', 'stomache': 'stomach',
    'diarea': 'diarrhea', 'diarrhoea': 'diarrhea',
    'indegestion': 'indigestion',
    'migrane': 'migraine', 'headeache': 'headache',
    'dipression': 'depression', 'anxity': 'anxiety',
    'insomina': 'insomnia', 'fatige': 'fatigue',
    'diabities': 'diabetes', 'diabets': 'diabetes',
    'maleriya': 'malaria', 'dengee': 'dengue',
    # add more as needed...
}

# Map disease names to embedding-friendly names (lots of fallbacks)
disease_mapping = {
    "Common Cold": "A Common Cold",
    "Cold": "A Common Cold",
    "Flu": "A Common Cold",
    "Influenza": "A Common Cold",
    "Cough": "A Common Cold",
    "Sore Throat": "A Common Cold",
    "Rhinitis": "A Common Cold",
    "Asthma": "Bronchial Asthma",
    "Bronchitis": "Bronchial Asthma",
    "Pneumonia": "Pneumonia",
    "COVID-19": "Pneumonia",
    "Sinusitis": "A Common Cold",
    "Dengue": "Fever",
    "Malaria": "Fever",
    "Typhoid": "Fever",
    "Gastroenteritis": "Fever",
    "Food Poisoning": "Fever",
    "Migraine": "Fever",
    "Headache": "Fever",
    "Fever": "Fever",
    "Hypertension": "Fever",
    "Diabetes": "Fever",
    "Arthritis": "Fever",
    "Acidity": "Fever",
    "Indigestion": "Fever",
    "Constipation": "Fever",
    "UTI": "Fever",
    "Jaundice": "Fever",
    # default cases will fallback to original disease string if not found
}

# Detailed condition information (safe 2-line descriptions)
condition_info = {
    'Asthma': [
        '  Asthma is a chronic inflammatory disease of the airways causing variable airflow obstruction.',
        '  Symptoms include wheeze, breathlessness, chest tightness and cough; avoid triggers and use inhalers as prescribed.'
    ],
    'Fever': [
        '  Fever is elevated body temperature often due to infection or inflammation.',
        '  Monitor temperature, stay hydrated and seek care if very high or prolonged.'
    ],
    'Common Cold': [
        '  A mild viral infection of the upper respiratory tract.',
        '  Symptoms include runny nose, sore throat, cough and sneezing; usually self-limiting.'
    ],
    'Gastroenteritis': [
        '  Inflammation of the stomach and intestines usually causing diarrhea and vomiting.',
        '  Rehydration and rest are essential; seek help if dehydrated or severe.'
    ],
    'Headache': [
        '  Pain in the head area with many potential causes (tension, migraine, infection).',
        '  Manage with rest, hydration, analgesics; seek care if sudden severe or with neurological signs.'
    ],
    'Migraine': [
        '  Recurrent moderate-to-severe headaches often with nausea and sensitivity to light/sound.',
        '  Trigger management and targeted medications are used under guidance.'
    ],
    'Arthritis': [
        '  Arthritis is inflammation of one or more joints causing pain, stiffness, and swelling.',
        '  May be osteoarthritis (wear-and-tear) or rheumatoid (autoimmune); both need proper management.'
    ],
    'Osteoarthritis': [
        '  Degenerative joint disease caused by wear-and-tear over time, common in older adults.',
        '  Joint pain worsens with activity and improves with rest; physical therapy helps.'
    ],
    'Rheumatoid Arthritis': [
        '  Autoimmune condition causing joint inflammation, often affecting multiple joints symmetrically.',
        '  Early diagnosis and treatment with immunosuppressants can help prevent joint damage.'
    ],
    'Joint Pain': [
        '  Joint pain can result from arthritis, injury, inflammation, or muscle strain.',
        '  Determine if localized (single joint) or generalized (multiple joints) for proper diagnosis.'
    ],
    'Dengue': [
        '  Mosquito-borne viral infection causing high fever, joint pain and low platelets.',
        '  Medical follow-up is important to monitor platelet counts.'
    ],
    'Malaria': [
        '  Parasitic infection causing cyclical fevers; can be severe without treatment.',
        '  Prompt diagnosis and anti-malarial therapy are required.'
    ],
    'UTI': [
        '  Infection of urinary tract often causing painful urination and frequency.',
        '  Seek antibiotics if confirmed; hydrate and consult your clinician.'
    ],
    # Add many more 2-line descriptions as needed (kept short for brevity)
}

# Icons to avoid missing keys
severity_icons = {
    'CRITICAL': '🔴', 'HIGH': '🟠', 'SEVERE': '🟥', 'MODERATE': '🟡', 'LOW': '🟢', 'MILD': '🟢', 'UNKNOWN': '⚪'
}
availability_icons = {
    'OTC': '🟢', 'Prescription': '🔵', 'Limited': '🟡', 'Unavailable': '🔴', 'Herbal': '🌿', 'Home Remedy': '🪴'
}

# ------------------------------------------------------------------------------------
# Utility helpers
# ------------------------------------------------------------------------------------
def load_csv_or_fallback(data_dir: str = "data"):
    """
    Try to load CSVs from data_dir (expected: diseases.csv, ingredients.csv, targets.csv, herbs.csv)
    If pandas not available or files missing, return embedded sample data as dict of DataFrames/lists
    
    All file reads use UTF-8 encoding to avoid encoding issues.
    """
    knowledge = {}
    if pd is None:
        # pandas not available; return sample data
        knowledge["diseases"] = SAMPLE_DISEASES
        knowledge["ingredients"] = SAMPLE_INGREDIENTS
        knowledge["targets"] = SAMPLE_TARGETS
        knowledge["herbs"] = SAMPLE_HERBS
        return knowledge

    try:
        # try reading CSVs, use fallbacks if files missing
        def try_read(fname, fallback):
            path = os.path.join(data_dir, fname)
            if os.path.exists(path):
                try:
                    return pd.read_csv(path, encoding='utf-8')
                except UnicodeDecodeError:
                    try:
                        return pd.read_csv(path, encoding='latin-1')
                    except Exception:
                        return pd.DataFrame(fallback)
                except Exception:
                    return pd.DataFrame(fallback)
            else:
                return pd.DataFrame(fallback)

        knowledge["diseases"] = try_read("diseases.csv", SAMPLE_DISEASES)
        knowledge["ingredients"] = try_read("ingredients.csv", SAMPLE_INGREDIENTS)
        knowledge["targets"] = try_read("targets.csv", SAMPLE_TARGETS)
        knowledge["herbs"] = try_read("herbs.csv", SAMPLE_HERBS)
    except Exception as e:
        # if anything fails, use sample data
        knowledge["diseases"] = pd.DataFrame(SAMPLE_DISEASES)
        knowledge["ingredients"] = pd.DataFrame(SAMPLE_INGREDIENTS)
        knowledge["targets"] = pd.DataFrame(SAMPLE_TARGETS)
        knowledge["herbs"] = pd.DataFrame(SAMPLE_HERBS)
    return knowledge

# ------------------------------------------------------------------------------------
# Keep original function names but wire to fallbacks above
# ------------------------------------------------------------------------------------
def load_knowledge_base(data_dir="data") -> Dict:
    """
    Load all medical knowledge data from CSVs or fallback data.
    Robust to missing files, encoding issues, and pandas unavailability.
    Always returns a valid knowledge dictionary.
    """
    try:
        raw = load_csv_or_fallback(data_dir)
        knowledge = {}

        # If pandas DataFrames, keep them; else they are lists/dicts
        knowledge["diseases"] = raw.get("diseases", SAMPLE_DISEASES)
        knowledge["ingredients"] = raw.get("ingredients", SAMPLE_INGREDIENTS)
        knowledge["targets"] = raw.get("targets", SAMPLE_TARGETS)
        knowledge["herbs"] = raw.get("herbs", SAMPLE_HERBS)

        # Create lookup tables (works for both DataFrame and list-of-dicts)
        try:
            # when pandas DataFrame
            tgt_df = knowledge["targets"]
            if hasattr(tgt_df, "iterrows"):
                knowledge["target_to_disease"] = dict(
                    zip(tgt_df["target"].astype(str).str.strip(), tgt_df["disease"].astype(str).str.strip())
                )
            else:
                # list of dicts
                mapping = {}
                for row in tgt_df:
                    mapping[str(row.get("target", "")).strip()] = str(row.get("disease", "")).strip()
                knowledge["target_to_disease"] = mapping
        except Exception:
            knowledge["target_to_disease"] = {}

        # Build ingredient_to_targets
        try:
            ing_df = knowledge["ingredients"]
            mapping = {}
            if hasattr(ing_df, "iterrows"):
                for _, row in ing_df.iterrows():
                    ing = str(row.get("ingredient", "")).strip()
                    tgt = str(row.get("target", "")).strip()
                    mapping.setdefault(ing, []).append(tgt)
            else:
                for row in ing_df:
                    ing = str(row.get("ingredient", "")).strip()
                    tgt = str(row.get("target", "")).strip()
                    mapping.setdefault(ing, []).append(tgt)
            knowledge["ingredient_to_targets"] = mapping
        except Exception:
            knowledge["ingredient_to_targets"] = {}

        return knowledge
    except Exception as e:
        # Last-resort fallback: return minimal but valid knowledge base
        return {
            "diseases": SAMPLE_DISEASES,
            "ingredients": SAMPLE_INGREDIENTS,
            "targets": SAMPLE_TARGETS,
            "herbs": SAMPLE_HERBS,
            "target_to_disease": {},
            "ingredient_to_targets": {}
        }

def get_herb_info(herb_name: str, herbs_df) -> Dict:
    """Get detailed information about an herb. herbs_df can be DataFrame or list."""
    try:
        if pd is not None and hasattr(herbs_df, "iloc"):
            row = herbs_df[herbs_df['herb'].str.lower() == herb_name.lower()]
            if row.empty:
                return {}
            row = row.iloc[0]
            return {
                "name": row.get("herb", herb_name),
                "benefits": row.get("benefits", ""),
                "active_compounds": row.get("active_compounds", ""),
                "usage": row.get("usage", ""),
            }
        else:
            # list of dicts fallback
            for r in herbs_df:
                if str(r.get("herb", "")).lower() == herb_name.lower():
                    return {
                        "name": r.get("herb", herb_name),
                        "benefits": r.get("benefits", ""),
                        "active_compounds": r.get("active_compounds", ""),
                        "usage": r.get("usage", ""),
                    }
    except Exception:
        pass
    return {}

def suggest_drugs_for_disease(disease: str, top_n: int = 5) -> List[Dict]:
    """
    Suggest pharmaceutical drugs/tablets available in medical stores for a disease.
    If DrugDatabase is not available, use embedded sample list and basic matching.
    """
    if HAS_DRUG_DB:
        try:
            db = DrugDatabase()
            drugs = db.get_drugs_sorted_by_commonality(disease)
            formatted = []
            for drug in drugs[:top_n]:
                formatted.append({
                    "name": drug.get("name"),
                    "brand_names": drug.get("brand_names", []),
                    "type": drug.get("type"),
                    "dosage": drug.get("dosage"),
                    "purpose": drug.get("purpose"),
                    "availability": drug.get("availability"),
                    "price_range": drug.get("price_range"),
                    "side_effects": drug.get("side_effects")
                })
            return formatted
        except Exception:
            # fallback to sample
            pass

    # Fallback simple matching from SAMPLE_DRUGS
    matched = []
    disease_l = (disease or "").lower()
    # Simple disease -> drug mapping heuristics
    for d in SAMPLE_DRUGS:
        name = d.get("name", "")
        purpose = d.get("purpose", "").lower()
        dtype = d.get("type", "").lower()
        
        # Check if drug matches disease keywords
        if any(k in disease_l for k in ["fever", "headache", "pain", "muscle", "strain", "back", "sprain"]) and ("pain" in purpose or "analgesic" in dtype or "nsaid" in dtype):
            matched.append(d)
        elif any(k in disease_l for k in ["stomach", "gastric", "gastro", "ulcer", "acidity", "indigestion"]) and any(k in purpose for k in ["acid", "gastric", "reflux", "motility"]):
            matched.append(d)
        elif any(k in disease_l for k in ["kidney", "stone", "urinary"]) and any(k in purpose for k in ["pain", "kidney", "urinary", "stone"]):
            matched.append(d)
        elif not matched:
            # Generic offer pain relievers for unmatched diseases
            if "pain" in purpose or "analgesic" in dtype:
                matched.append(d)
        
        if len(matched) >= top_n:
            break
    
    # If still no matches, provide general pain relievers as last resort
    if not matched:
        matched = [d for d in SAMPLE_DRUGS if "pain" in d.get("purpose", "").lower() or "analgesic" in d.get("type", "").lower()][:top_n]
    
    return matched[:top_n]

def load_drug_interactions(data_dir: str = "data") -> Dict:
    """Load drug interaction database from CSV if available; fallback empty dict."""
    interactions = {}
    if pd is None:
        return interactions
    path = os.path.join(data_dir, "drug_interactions.csv")
    if not os.path.exists(path):
        return interactions
    try:
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            drug1 = str(row.get('drug1', '')).lower().strip()
            drug2 = str(row.get('drug2', '')).lower().strip()
            key = tuple(sorted([drug1, drug2]))
            interactions[key] = {
                'severity': row.get('severity', 'MODERATE'),
                'effect': row.get('effect', ''),
                'recommendation': row.get('recommendation', '')
            }
    except Exception:
        pass
    return interactions

def check_drug_interactions(drug_list: List[str], interactions: Dict = None) -> List[Dict]:
    """Check drug interactions using preloaded interactions dict."""
    if interactions is None:
        interactions = load_drug_interactions()
    if not interactions or len(drug_list) < 2:
        return []
    detected = []
    for i in range(len(drug_list)):
        for j in range(i+1, len(drug_list)):
            a = (drug_list[i] or "").lower().strip()
            b = (drug_list[j] or "").lower().strip()
            key = tuple(sorted([a, b]))
            if key in interactions:
                data = interactions[key]
                detected.append({
                    'drug1': drug_list[i],
                    'drug2': drug_list[j],
                    'severity': data.get('severity', 'MODERATE'),
                    'effect': data.get('effect', ''),
                    'recommendation': data.get('recommendation', '')
                })
    return detected

def load_allergies_db(data_dir: str = "data") -> Dict:
    """Load allergies database if available; fallback empty dict."""
    allergies = {}
    if pd is None:
        return allergies
    path = os.path.join(data_dir, "allergies.csv")
    if not os.path.exists(path):
        return allergies
    try:
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            allergen = str(row.get('allergen', '')).lower().strip()
            allergies[allergen] = {
                'category': row.get('category', ''),
                'severity': row.get('severity', 'MODERATE'),
                'cross_reactions': str(row.get('cross_reactions', '')).split(';') if pd.notna(row.get('cross_reactions', '')) else [],
                'symptoms': str(row.get('symptoms', '')).split(';') if pd.notna(row.get('symptoms', '')) else [],
                'common_sources': row.get('common_sources', '')
            }
    except Exception:
        pass
    return allergies

def check_allergies(drugs: List[Dict], user_allergies: Set[str] = None, allergies_db: Dict = None) -> List[Dict]:
    """Check if recommended drugs contain allergens (basic name-based check)."""
    if not user_allergies or not drugs:
        return []
    if allergies_db is None:
        allergies_db = load_allergies_db()
    warnings = []
    for drug in drugs:
        drug_name = (drug.get('name') or "").lower()
        for allergen in user_allergies:
            a = allergen.lower().strip()
            if a in drug_name or drug_name in a:
                warnings.append({
                    'drug': drug.get('name'),
                    'allergen': allergen,
                    'severity': allergies_db.get(a, {}).get('severity', 'MODERATE'),
                    'warning': f"⚠️ ALLERGY ALERT: {drug.get('name')} may contain {allergen}"
                })
    return warnings

# ------------------------------------------------------------------------------------
# Suggest herbal ingredients for a disease
# This uses embeddings if available, otherwise returns simple heuristic list
# ------------------------------------------------------------------------------------
def suggest_ingredients_for_disease(
    disease: str,
    embeddings_path: str = "data/embeddings.kv",
    model_path: str = "data/stack_model.pkl",
    knowledge: Dict = None
) -> List[Tuple[str, float]]:
    """
    Suggest herbal ingredients for a detected disease.
    If embeddings/model exist and gensim/joblib available, uses them.
    Otherwise returns heuristic list based on knowledge and fallback mapping.
    """
    # If gensim/joblib not available or files missing, fallback
    if KeyedVectors is None or joblib is None or np is None:
        # Heuristic: map some diseases to common herbs
        d = (disease or "").lower()
        heuristics = []
        if "gastro" in d or "diarr" in d or "stomach" in d:
            heuristics = [("Ginger", 0.85), ("Peppermint", 0.75), ("Turmeric", 0.6), ("ORS", 0.5)]
        elif "fever" in d or "dengue" in d or "malaria" in d:
            heuristics = [("Withaferin A", 0.7), ("Papaya leaf extract", 0.6), ("Turmeric", 0.5)]
        elif "cold" in d or "cough" in d or "bronch" in d or "asthma" in d:
            heuristics = [("Tulsi", 0.8), ("Ginger", 0.7), ("Licorice", 0.6)]
        elif "headache" in d or "migraine" in d:
            heuristics = [("Peppermint", 0.7), ("Feverfew", 0.6), ("Turmeric", 0.5)]
        elif "muscle" in d or "strain" in d or "back pain" in d or "sprain" in d or "pain" in d:
            heuristics = [("Turmeric", 0.8), ("Ginger", 0.75), ("Arnica", 0.7), ("Boswellia", 0.65)]
        elif "kidney" in d or "stone" in d or "renal" in d or "urinary" in d:
            heuristics = [("Chanca Piedra", 0.8), ("Dandelion", 0.7), ("Cranberry", 0.65), ("Hydrangea", 0.6)]
        else:
            heuristics = [("Turmeric", 0.6), ("Ginger", 0.55), ("Neem", 0.45)]
        return heuristics[:5]

    # If embeddings present, try to use them (kept backward-compatible)
    try:
        if not os.path.exists(embeddings_path) or not os.path.exists(model_path):
            # Files don't exist, use heuristic fallback
            d = (disease or "").lower()
            heuristics = []
            if "gastro" in d or "diarr" in d or "stomach" in d:
                heuristics = [("Ginger", 0.85), ("Peppermint", 0.75), ("Turmeric", 0.6), ("ORS", 0.5)]
            elif "fever" in d or "dengue" in d or "malaria" in d:
                heuristics = [("Withaferin A", 0.7), ("Papaya leaf extract", 0.6), ("Turmeric", 0.5)]
            elif "cold" in d or "cough" in d or "bronch" in d or "asthma" in d:
                heuristics = [("Tulsi", 0.8), ("Ginger", 0.7), ("Licorice", 0.6)]
            elif "headache" in d or "migraine" in d:
                heuristics = [("Peppermint", 0.7), ("Feverfew", 0.6), ("Turmeric", 0.5)]
            elif "muscle" in d or "strain" in d or "back pain" in d or "sprain" in d or "pain" in d:
                heuristics = [("Turmeric", 0.8), ("Ginger", 0.75), ("Arnica", 0.7), ("Boswellia", 0.65)]
            elif "kidney" in d or "stone" in d or "renal" in d or "urinary" in d:
                heuristics = [("Chanca Piedra", 0.8), ("Dandelion", 0.7), ("Cranberry", 0.65), ("Hydrangea", 0.6)]
            else:
                heuristics = [("Turmeric", 0.6), ("Ginger", 0.55), ("Neem", 0.45)]
            return heuristics[:5]
        emb = KeyedVectors.load(embeddings_path)
        model = joblib.load(model_path)
        ingredients = [l.strip() for l in open("data/nodes_ingredients.txt").read().splitlines() if l.strip()]
        lookup_name = disease_mapping.get(disease, disease)
        if lookup_name not in emb.key_to_index:
            # Disease not in embeddings, use heuristic fallback
            d = (disease or "").lower()
            heuristics = []
            if "gastro" in d or "diarr" in d or "stomach" in d:
                heuristics = [("Ginger", 0.85), ("Peppermint", 0.75), ("Turmeric", 0.6), ("ORS", 0.5)]
            elif "fever" in d or "dengue" in d or "malaria" in d:
                heuristics = [("Withaferin A", 0.7), ("Papaya leaf extract", 0.6), ("Turmeric", 0.5)]
            elif "cold" in d or "cough" in d or "bronch" in d or "asthma" in d:
                heuristics = [("Tulsi", 0.8), ("Ginger", 0.7), ("Licorice", 0.6)]
            elif "headache" in d or "migraine" in d:
                heuristics = [("Peppermint", 0.7), ("Feverfew", 0.6), ("Turmeric", 0.5)]
            elif "muscle" in d or "strain" in d or "back pain" in d or "sprain" in d or "pain" in d:
                heuristics = [("Turmeric", 0.8), ("Ginger", 0.75), ("Arnica", 0.7), ("Boswellia", 0.65)]
            elif "kidney" in d or "stone" in d or "renal" in d or "urinary" in d:
                heuristics = [("Chanca Piedra", 0.8), ("Dandelion", 0.7), ("Cranberry", 0.65), ("Hydrangea", 0.6)]
            else:
                heuristics = [("Turmeric", 0.6), ("Ginger", 0.55), ("Neem", 0.45)]
            return heuristics[:5]
        scores = []
        for ing in ingredients:
            if ing in emb.key_to_index:
                feat = np.multiply(emb[ing], emb[lookup_name])
                proba = model.predict_proba([feat])[0, 1]
                scores.append((ing, float(proba)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:5]
    except Exception:
        # Exception occurred, use heuristic fallback
        d = (disease or "").lower()
        heuristics = []
        if "gastro" in d or "diarr" in d or "stomach" in d:
            heuristics = [("Ginger", 0.85), ("Peppermint", 0.75), ("Turmeric", 0.6), ("ORS", 0.5)]
        elif "fever" in d or "dengue" in d or "malaria" in d:
            heuristics = [("Withaferin A", 0.7), ("Papaya leaf extract", 0.6), ("Turmeric", 0.5)]
        elif "cold" in d or "cough" in d or "bronch" in d or "asthma" in d:
            heuristics = [("Tulsi", 0.8), ("Ginger", 0.7), ("Licorice", 0.6)]
        elif "headache" in d or "migraine" in d:
            heuristics = [("Peppermint", 0.7), ("Feverfew", 0.6), ("Turmeric", 0.5)]
        elif "muscle" in d or "strain" in d or "back pain" in d or "sprain" in d or "pain" in d:
            heuristics = [("Turmeric", 0.8), ("Ginger", 0.75), ("Arnica", 0.7), ("Boswellia", 0.65)]
        elif "kidney" in d or "stone" in d or "renal" in d or "urinary" in d:
            heuristics = [("Chanca Piedra", 0.8), ("Dandelion", 0.7), ("Cranberry", 0.65), ("Hydrangea", 0.6)]
        else:
            heuristics = [("Turmeric", 0.6), ("Ginger", 0.55), ("Neem", 0.45)]
        return heuristics[:5]

# ------------------------------------------------------------------------------------
# AI insights: uses Azure/GitHub LLM if available, otherwise uses heuristic fallback
# ------------------------------------------------------------------------------------
def generate_ai_insights(
    user_input: str,
    disease: str,
    herbal_recommendations: List[Tuple[str, float]],
    drug_recommendations: List[Dict],
    knowledge: Dict
) -> str:
    """
    Generate AI insights using multiple LLM providers with retry logic.
    
    Providers attempted (in order):
    1. OpenAI API (if OPENAI_API_KEY set)
    2. GitHub Models API (if GITHUB_TOKEN set) - with 2 retries
    3. Azure OpenAI (if AZURE_ENDPOINT and AZURE_KEY set)
    4. Local heuristic fallback
    
    Each provider has a 15-second timeout. Graceful fallback on any failure.
    """
    
    herb_names = [ing for ing, _ in herbal_recommendations]
    herbs_str = ", ".join(herb_names) if herb_names else "traditional remedies"
    drug_names = [drug.get("name") for drug in drug_recommendations]
    drugs_str = ", ".join(drug_names) if drug_names else "suitable medications"
    
    system_prompt = """You are an experienced AI health assistant specializing in holistic wellness and medical science. 
Provide evidence-based, professional insights about herbal remedies and medications. 
Always emphasize consulting healthcare professionals for diagnosis and treatment. 
Be concise, clear, medically accurate, and educational."""
    
    user_prompt = f"""Patient symptoms: {user_input}
Detected condition: {disease}
Recommended herbs: {herbs_str}
Recommended medications: {drugs_str}

Provide a professional health assessment covering:
1. How these remedies may help address the condition
2. Benefits and drawbacks of herbal vs pharmaceutical approaches
3. Important safety considerations and potential side effects
4. When to seek immediate medical attention

Format: 3-4 short paragraphs, 180-220 words total."""
    
    # Try OpenAI API (Option 1 - Preferred)
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            import urllib.request
            import json as json_module
            
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 500
            }
            
            req = urllib.request.Request(
                url,
                data=json_module.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json_module.loads(response.read().decode('utf-8'))
                if result.get("choices") and len(result["choices"]) > 0:
                    ai_response = result["choices"][0]["message"]["content"]
                    return ai_response
        except Exception as e:
            pass  # Silently try next provider
    
    # Try GitHub Models API (Option 2) with retry logic
    github_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT")
    if github_token:
        max_retries = 2
        for attempt in range(max_retries):
            try:
                import urllib.request
                import json as json_module
                import ssl
                
                url = "https://models.inference.ai.azure.com/chat/completions"
                headers = {
                    "Authorization": f"Bearer {github_token}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_tokens": 500
                }
                
                req = urllib.request.Request(
                    url,
                    data=json_module.dumps(payload).encode('utf-8'),
                    headers=headers,
                    method='POST'
                )
                
                # Handle SSL certificate issues
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
                    result = json_module.loads(response.read().decode('utf-8'))
                    if result.get("choices") and len(result["choices"]) > 0:
                        ai_response = result["choices"][0]["message"]["content"]
                        return ai_response
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(0.5)  # Brief delay before retry
                    continue
                else:
                    pass  # Try next provider
    
    # Try Azure OpenAI (Option 3)
    if HAS_LLM:
        try:
            endpoint = os.environ.get("AZURE_ENDPOINT")
            azure_key = os.environ.get("AZURE_API_KEY") or os.environ.get("AZURE_KEY")
            if endpoint and azure_key:
                client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(azure_key))
                response = client.complete(
                    messages=[
                        SystemMessage(system_prompt),
                        UserMessage(user_prompt)
                    ],
                    temperature=0.7,
                    top_p=0.95,
                    model="gpt-4o-mini",
                    max_tokens=500
                )
                if response and response.choices and len(response.choices) > 0:
                    return response.choices[0].message.content
        except Exception as e:
            pass  # Silently try fallback

    # Local Heuristic Fallback (Option 4) - Always returns valid response
    herbs_list = ", ".join([h for h, _ in herbal_recommendations[:4]]) if herbal_recommendations else "herbal options"
    drugs_list = ", ".join([d.get("name") for d in drug_recommendations[:4]]) if drug_recommendations else "appropriate medications"
    
    # Build base summary
    summary = (
        f"Based on the reported symptoms, {disease} has been identified as the primary concern. "
        f"\n\nHerbal options like {herbs_list} may provide supportive relief through anti-inflammatory and soothing properties. "
        f"These natural remedies work gradually and are often used for long-term management and prevention. "
        f"\n\nPharmaceutical treatments such as {drugs_list} offer evidence-based symptom management with proven efficacy and faster relief. "
        f"These medications are suitable for acute condition management and immediate symptom control. "
        f"\n\nThe optimal approach depends on condition severity, symptom duration, and individual factors. "
        f"Always consult a qualified healthcare professional before starting any treatment. "
        f"Seek immediate medical attention if you experience severe symptoms, difficulty breathing, high fever, or other concerning signs."
    )
    
    # Add special insights for hormonal conditions
    disease_lower = (disease or "").lower()
    if "hormonal" in disease_lower or "pcos" in disease_lower:
        # Added PCOS logic: Enhanced AI insight for hormonal imbalance and cycle regulation
        hormonal_insight = (
            "\n\n💡 HORMONAL DISORDER NOTE: Conditions like PCOS involve hormonal imbalance affecting the menstrual cycle and metabolism. "
            "Cycle regulation is key—lifestyle changes including regular exercise (30+ mins daily), stress management, balanced nutrition with adequate protein, "
            "and consistent sleep (7-9 hrs) are foundational. Herbal remedies support hormonal balance naturally. Always consult an endocrinologist for "
            "hormone level testing, diagnosis confirmation, and personalized treatment including possible medications like metformin or hormonal contraceptives."
        )
        summary += hormonal_insight
    elif "menorrhagia" in disease_lower or "heavy" in disease_lower and "bleed" in disease_lower:
        # Added Menorrhagia logic: Enhanced AI insight for heavy menstrual bleeding and iron loss
        menorrhagia_insight = (
            "\n\n💡 MENORRHAGIA NOTE: Heavy or prolonged menstrual bleeding can lead to significant iron loss and anemia. Symptoms like weakness and dizziness "
            "may indicate low iron levels. Iron-rich herbal remedies can help replenish stores. Pharmaceutical options often include iron supplements, "
            "tranexamic acid (to reduce bleeding), or hormonal treatments (contraceptives/progestins) to regulate flow. Monitor your symptoms closely—if bleeding "
            "exceeds normal duration/volume or symptoms worsen, seek urgent medical evaluation. Regular iron level testing (ferritin/hemoglobin) is essential."
        )
        summary += menorrhagia_insight
    
    return summary

# ------------------------------------------------------------------------------------
# Format results for terminal display (keeps original formatting style but simplified)
# ------------------------------------------------------------------------------------
def format_answer_for_display(response: Dict) -> str:
    """Format the comprehensive response for user display with herbs and drugs (rich terminal)."""
    # reuse dictionaries defined above
    global spelling_map, condition_info, severity_icons, availability_icons

    # Defensive defaults
    spelling_map_local = spelling_map or {}
    condition_info_local = condition_info or {}
    severity_local = severity_icons or {}
    availability_local = availability_icons or {}

    # Spelling check
    user_input = (response.get("input") or "").lower()
    spelling_issues = []
    for typo, correct in spelling_map_local.items():
        if typo and typo in user_input:
            spelling_issues.append((typo, correct))

    # Header
    answer_lines = []
    answer_lines.append("╔" + "═" * 78 + "╗")
    answer_lines.append("║" + " " * 78 + "║")
    title = f"    {BOLD}🏥 AI-POWERED HEALTH RECOMMENDATION SYSTEM 🌿{RESET}"
    subtitle = f"{BOLD}Comprehensive Herbal & Pharmaceutical Guide{RESET}"
    # center
    answer_lines.append("║" + title.center(78) + "║")
    answer_lines.append("║" + subtitle.center(78) + "║")
    answer_lines.append("║" + " " * 78 + "║")
    answer_lines.append("╚" + "═" * 78 + "╝\n")

    # Spelling section
    if spelling_issues:
        answer_lines.append(f"{YELLOW}{BOLD}✏️  SPELLING CHECK{RESET}")
        answer_lines.append(f"{YELLOW}" + "━" * 78 + f"{RESET}\n")
        answer_lines.append(f"  {YELLOW}⚠️  We detected some spelling variations in your input:{RESET}")
        for typo, correct in spelling_issues:
            answer_lines.append(f"     • \"{YELLOW}{typo}{RESET}\" → should be \"{GREEN}{correct}{RESET}\"")
        answer_lines.append("  " + f"{BOLD}💡 Tip:{RESET} Use correct spelling for more accurate results.")
        answer_lines.append("")

    # Symptom analysis
    answer_lines.append(f"{BLUE}{BOLD}📋 SYMPTOM ANALYSIS{RESET}")
    answer_lines.append(f"{BLUE}" + "━" * 78 + f"{RESET}\n")
    answer_lines.append(f"  📝 Your Input: \"{response.get('input')}\"")
    answer_lines.append(f"  🧠 {BOLD}Detected Condition:{RESET} {GREEN}{response.get('detected_disease')}{RESET}")
    # Confidence interpret
    conf = float(response.get('confidence', 0.0))
    conf_pct = conf * 100.0
    conf_word = "Low"
    if conf_pct >= 80:
        conf_word = "High"
    elif conf_pct >= 60:
        conf_word = "Moderate"
    answer_lines.append(f"     {BOLD}Confidence Level:{RESET} {YELLOW}{conf_pct:.1f}% ({conf_word}){RESET}")
    if response.get("disease_symptom"):
        answer_lines.append(f"     {BOLD}Typical Symptom:{RESET} {response.get('disease_symptom')}")
    answer_lines.append("")

    # Condition description
    answer_lines.append(f"{BLUE}{BOLD}📌 ABOUT YOUR CONDITION{RESET}")
    answer_lines.append(f"{BLUE}" + "━" * 78 + f"{RESET}")
    disease_name = response.get('detected_disease', '')
    disease_key = None
    try:
        disease_key = next((k for k in condition_info_local.keys() if k.lower() in disease_name.lower()), None)
    except Exception:
        disease_key = None
    if disease_key:
        for line in condition_info_local[disease_key]:
            answer_lines.append(line)
    else:
        answer_lines.append(f"  {disease_name} is a medical condition requiring attention.")
        answer_lines.append("  Please consult a healthcare professional for proper diagnosis and treatment.")
    answer_lines.append("")

    # Allergy warnings
    allergy_warnings = response.get("allergy_warnings", [])
    if allergy_warnings:
        answer_lines.append(f"{RED}{BOLD}🚨 ALLERGY ALERTS{RESET}")
        answer_lines.append(f"{RED}" + "━" * 78 + f"{RESET}")
        for warning in allergy_warnings:
            sev = warning.get('severity', 'MODERATE')
            icon = severity_local.get(sev, '🟡')
            answer_lines.append(f"  {icon} {RED}{BOLD}{warning['drug']}{RESET} - {warning['allergen']} allergy")
            answer_lines.append(f"     Severity: {RED}{sev}{RESET}")
            answer_lines.append(f"     ⚠️  {BOLD}DO NOT USE – Use safe alternative instead{RESET}")
        answer_lines.append("")

    # Drug interactions
    drug_interactions = response.get("drug_interactions", [])
    if drug_interactions:
        answer_lines.append(f"{RED}{BOLD}⚠️  DRUG INTERACTION WARNINGS{RESET}")
        answer_lines.append(f"{RED}" + "━" * 78 + f"{RESET}")
        for interaction in drug_interactions:
            sev = interaction.get('severity', 'MODERATE')
            icon = severity_local.get(sev, '🟡')
            answer_lines.append(f"  {icon} {BOLD}{interaction['drug1']} + {interaction['drug2']}{RESET}")
            answer_lines.append(f"     Severity: {sev}")
            answer_lines.append(f"     Effect: {interaction.get('effect')}")
            answer_lines.append(f"     Recommendation: {interaction.get('recommendation')}")
        answer_lines.append("")

    # Emergency signs (NEW - for menstrual and other serious conditions)
    emergency_signs = response.get("emergency_signs", [])
    if emergency_signs:
        answer_lines.append(f"{RED}{BOLD}🚨 EMERGENCY WARNING SIGNS{RESET}")
        answer_lines.append(f"{RED}" + "━" * 78 + f"{RESET}")
        answer_lines.append(f"  {RED}{BOLD}SEEK IMMEDIATE MEDICAL ATTENTION IF YOU EXPERIENCE:{RESET}")
        for sign in emergency_signs:
            answer_lines.append(f"  {RED}⚠️  {sign}{RESET}")
        answer_lines.append("")

    # Herbal recommendations
    herbal_recs = response.get("herbal_recommendations", [])
    if herbal_recs:
        answer_lines.append(f"{GREEN}{BOLD}🌿 HERBAL INGREDIENTS ({len(herbal_recs)}){RESET}")
        answer_lines.append(f"{GREEN}" + "━" * 78 + f"{RESET}")
        for i, rec in enumerate(herbal_recs, 1):
            score = float(rec.get('relevance_score', 0.0))
            bar_len = max(0, min(30, int(round(score * 30))))
            bar = "█" * bar_len + "░" * (30 - bar_len)
            answer_lines.append(f"  {BOLD}{i}. {rec.get('ingredient').upper()}{RESET}")
            answer_lines.append(f"     Relevance: {GREEN}{bar}{RESET} {score:.1%}")
            answer_lines.append(f"     Benefits:  {rec.get('benefits')}")
            if rec.get("active_compounds"):
                answer_lines.append(f"     Compounds: {rec.get('active_compounds')}")
            answer_lines.append(f"     Usage:     {rec.get('usage')}")
        answer_lines.append("")

    # Drug recommendations
    drug_recs = response.get("drug_recommendations", [])
    if drug_recs:
        answer_lines.append(f"{YELLOW}{BOLD}💊 PHARMACEUTICAL MEDICATIONS ({len(drug_recs)}){RESET}")
        answer_lines.append(f"{YELLOW}" + "━" * 78 + f"{RESET}")
        for i, drug in enumerate(drug_recs, 1):
            avail = drug.get('availability', 'Unknown')
            avail_icon = availability_local.get(avail, '🟡')
            answer_lines.append(f"  {BOLD}{i}. {drug.get('name').upper()}{RESET}")
            brand_names = ", ".join(drug.get('brand_names', [])) if drug.get('brand_names') else "—"
            answer_lines.append(f"     {BOLD}Brand Names:{RESET}  {brand_names}")
            answer_lines.append(f"     {BOLD}Type:{RESET}         {drug.get('type', '—')}")
            answer_lines.append(f"     {BOLD}Dosage:{RESET}       {drug.get('dosage', '—')}")
            answer_lines.append(f"     {BOLD}Purpose:{RESET}      {drug.get('purpose', '—')}")
            answer_lines.append(f"     {BOLD}Availability:{RESET} {avail_icon} {avail}")
            answer_lines.append(f"     {BOLD}Price Range:{RESET}  {YELLOW}{drug.get('price_range', '—')}{RESET}")
            answer_lines.append(f"     {BOLD}Side Effects:{RESET} {RED}{drug.get('side_effects', '—')}{RESET}")
        answer_lines.append("")

    # Comparison section
    if herbal_recs and drug_recs:
        answer_lines.append(f"{HEADER}{BOLD}🔄 COMPARISON: HERBAL vs PHARMACEUTICAL{RESET}")
        answer_lines.append(f"{HEADER}" + "━" * 78 + f"{RESET}")
        answer_lines.append("  ✓ Natural ingredients                ✓ Clinically proven")
        answer_lines.append("  ✓ Fewer synthetic additives          ✓ Faster symptom relief")
        answer_lines.append("  ✓ Milder with fewer side effects     ✓ Precise dosing")
        answer_lines.append("  ✓ Long-term preventive care          ✓ Well-researched effects")
        answer_lines.append("  ✗ Slower acting                       ✗ More pronounced side effects")
        answer_lines.append("  ✗ Quality varies by brand             ✗ May require prescription")
        answer_lines.append("")
        answer_lines.append(f"  {BOLD}{BLUE}💡 SMART RECOMMENDATION:{RESET}")
        answer_lines.append("     • Acute Conditions: Start with pharmaceutical options")
        answer_lines.append("     • Chronic Prevention: Consider herbal remedies")
        answer_lines.append("     • Optimal Approach: Combination therapy (consult doctor)")
        answer_lines.append("")

    # AI insights
    if response.get("ai_insights"):
        answer_lines.append(f"{HEADER}{BOLD}🤖 AI-GENERATED INSIGHTS{RESET}")
        answer_lines.append(f"{HEADER}" + "━" * 78 + f"{RESET}")
        answer_lines.append(response.get("ai_insights"))
        answer_lines.append("")

    # Footer disclaimer
    answer_lines.append(f"{RED}{BOLD}╔" + "═" * 78 + "╗{RESET}".replace("{RESET}", RESET))
    answer_lines.append(f"{RED}{BOLD}║ ⚠️  IMPORTANT DISCLAIMER{RESET}".replace("{RESET}", RESET))
    answer_lines.append(f"{RED}{BOLD}╠" + "═" * 78 + "╣{RESET}".replace("{RESET}", RESET))
    answer_lines.append(f"{RED}║ This is for EDUCATIONAL PURPOSES ONLY. This system provides general information and should NOT replace professional medical advice.{RESET}")
    answer_lines.append(f"{RED}║ ALWAYS consult qualified healthcare professionals before starting any herbal treatment, taking new medications, combining herbs & drugs, or making dietary changes.{RESET}")
    answer_lines.append(f"{RED}║ 🚨 IN CASE OF EMERGENCY: Seek immediate medical attention{RESET}")
    answer_lines.append(f"{RED}{BOLD}╚" + "═" * 78 + "╝{RESET}".replace("{RESET}", RESET))

    # join with newline
    return "\n".join(answer_lines)

# ------------------------------------------------------------------------------------
# Main orchestrator: generate_comprehensive_answer (keeps original logic)
# ------------------------------------------------------------------------------------
def generate_comprehensive_answer(
    user_input: str,
    knowledge: Dict,
    use_ai: bool = True,
    include_drugs: bool = True,
    user_allergies: Set[str] = None
) -> Dict:
    """
    Generate a comprehensive answer to user's health query.
    Combines disease prediction, herbal recommendations, drug recommendations, and AI insights.
    """
    # Step 1: Predict disease using improved detection v2 as primary method
    enhanced_result = None
    try:
        # PRIORITY: Use detect_condition_v2 first for accurate menstrual/hormonal detection
        disease, confidence = detect_condition_v2(user_input)
        
        # If USE_ENHANCED, also try enhanced predictor for additional context (menstrual/PCOS patterns)
        if USE_ENHANCED:
            try:
                enhanced_result = predict_disease_enhanced(user_input)
            except Exception:
                enhanced_result = None
    except Exception:
        # Fallback to enhanced predictor if available
        try:
            if USE_ENHANCED:
                enhanced_result = predict_disease_enhanced(user_input)
                disease = enhanced_result.get('primary_disease')
                confidence = float(enhanced_result.get('confidence', 0.0))
            else:
                predicted = predict_disease(user_input)
                if isinstance(predicted, tuple):
                    disease, confidence = predicted
                else:
                    disease = predicted
                    confidence = 0.5
        except Exception:
            disease, confidence = ("General Symptom", 0.5)

    # Step 2: Get herbal recommendations
    # If enhanced predictor has herbal_remedies, use those; otherwise get from knowledge base
    if enhanced_result and enhanced_result.get('herbal_remedies'):
        # Use herbal remedies from menstrual/specialized pattern detection
        enhanced_herbal = enhanced_result.get('herbal_remedies', [])
        herbal_recommendations = [(r['name'], 0.85) for r in enhanced_herbal]
    else:
        # Fall back to knowledge base lookup
        herbal_recommendations = suggest_ingredients_for_disease(disease, knowledge=knowledge)

    # Step 3: Get pharma recommendations if enabled
    drug_recommendations = []
    drug_interactions = []
    allergy_warnings = []

    if include_drugs:
        # If enhanced predictor has pharma_options, use those; otherwise get from knowledge base
        if enhanced_result and enhanced_result.get('pharma_options'):
            # Use pharma options from menstrual/specialized pattern detection
            enhanced_drugs = enhanced_result.get('pharma_options', [])
            drug_recommendations = [
                {
                    'name': d['name'],
                    'use': d['use'],
                    'brand_names': d.get('brand_names', []),
                    'type': 'Specialized Medication',
                    'dosage': 'Consult healthcare provider',
                    'purpose': d['use'],
                    'availability': 'Common - Medical Store',
                    'price_range': 'Variable',
                    'side_effects': 'Consult healthcare provider'
                }
                for d in enhanced_drugs
            ]
        else:
            # Fall back to knowledge base lookup
            drug_recommendations = suggest_drugs_for_disease(disease, top_n=5)
        
        drug_names = [d.get('name', '') for d in drug_recommendations]
        interactions_db = load_drug_interactions()
        drug_interactions = check_drug_interactions(drug_names, interactions_db)
        if user_allergies:
            allergy_warnings = check_allergies(drug_recommendations, user_allergies)

    # Build response
    response = {
        "input": user_input,
        "detected_disease": disease,
        "confidence": float(confidence),
        "herbal_recommendations": [],
        "drug_recommendations": drug_recommendations,
        "drug_interactions": drug_interactions,
        "allergy_warnings": allergy_warnings,
        "ai_insights": None,
        "emergency_signs": enhanced_result.get('emergency_signs', []) if enhanced_result else []
    }

    # Enrich herbal recs
    herbs_df = knowledge.get("herbs", SAMPLE_HERBS)
    for ingredient, score in herbal_recommendations:
        herb_info = get_herb_info(ingredient, herbs_df)
        response["herbal_recommendations"].append({
            "ingredient": ingredient,
            "relevance_score": float(score),
            "benefits": herb_info.get("benefits", "Traditional herbal remedy") if isinstance(herb_info, dict) else "Traditional herbal remedy",
            "active_compounds": herb_info.get("active_compounds", "") if isinstance(herb_info, dict) else "",
            "usage": herb_info.get("usage", "Consult herbalist for dosage") if isinstance(herb_info, dict) else "Consult herbalist for dosage"
        })

    # Disease context from knowledge base (if available)
    disease_info = None
    try:
        ds = knowledge.get("diseases", [])
        if pd is not None and hasattr(ds, "iterrows"):
            found = ds[ds["disease"].str.lower() == (disease or "").lower()]
            if not found.empty:
                disease_info = found.iloc[0]
        else:
            # list fallback
            for r in ds:
                if str(r.get("disease", "")).lower() == (disease or "").lower():
                    disease_info = r
                    break
    except Exception:
        disease_info = None

    if disease_info is not None:
        # symptom may be present as column or key
        if isinstance(disease_info, dict):
            response["disease_symptom"] = disease_info.get("symptom", "")
        else:
            try:
                response["disease_symptom"] = disease_info.get("symptom", "")
            except (AttributeError, TypeError):
                response["disease_symptom"] = ""

    # AI insights
    if use_ai:
        response["ai_insights"] = generate_ai_insights(user_input, disease, herbal_recommendations, drug_recommendations, knowledge)

    return response

# ------------------------------------------------------------------------------------
# Logging helper
# ------------------------------------------------------------------------------------
LOG_FILE = "assistant_interactions.jsonl"

def log_interaction(entry: Dict):
    """Append an entry to LOG_FILE in JSON lines format."""
    try:
        entry_copy = dict(entry)
        entry_copy["_timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry_copy, ensure_ascii=False) + "\n")
    except Exception:
        pass

# ------------------------------------------------------------------------------------
# Main interactive terminal UI
# ------------------------------------------------------------------------------------
def main():
    # Load knowledge base
    print("🏥 Welcome to Dual Recommendation Health Assistant!")
    print("   (Herbal Remedies + Pharmaceutical Medications)")
    print("=" * 66)
    print("📚 Loading medical knowledge base...")
    knowledge = load_knowledge_base()
    print("✅ Knowledge base loaded!")
    print("💊 Pharmaceutical database " + ("available!" if HAS_DRUG_DB else "(fallback sample used)"))
    print()
    if HAS_LLM:
        print("✅ AI LLM enabled (environment configured)")
    else:
        print("⚠️  AI LLM not available — using heuristic fallback for AI insights.")
    print("\n" + "=" * 66 + "\n")
    print(f"{YELLOW}💡 TIP:{RESET} For best results, enter symptoms simply (e.g., 'fever', 'headache', 'loose motions')")
    print("\n" + "=" * 66 + "\n")

    # Greet and optional TTS
    speak_text("Welcome to the Dual Recommendation Health Assistant. Enter your symptoms or type quit to exit.")

    try:
        while True:
            user_input = input("🧍 Enter your problem or symptoms (or 'quit' to exit): ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit"):
                print("Goodbye — stay healthy!")
                speak_text("Goodbye. Stay healthy.")
                break

            # optional allergy input prompt
            allergy_input = input("⚠️  Any allergies? (comma separated or press Enter): ").strip()
            user_allergies = set([a.strip() for a in allergy_input.split(",") if a.strip()]) if allergy_input else None

            print("\n🔍 Analyzing your symptoms...\n")
            response = generate_comprehensive_answer(user_input, knowledge, use_ai=True, include_drugs=True, user_allergies=user_allergies)

            # format and display
            display = format_answer_for_display(response)
            print(display)

            # TTS short summary
            tts_short = f"Detected condition: {response.get('detected_disease')}. Confidence {response.get('confidence')*100:.0f} percent."
            speak_text(tts_short)

            # log
            log_entry = {
                "input": user_input,
                "detected_disease": response.get("detected_disease"),
                "confidence": response.get("confidence"),
                "herbal_recommendations": [h.get("ingredient") for h in response.get("herbal_recommendations", [])],
                "drug_recommendations": [d.get("name") for d in response.get("drug_recommendations", [])],
                "allergy_warnings": response.get("allergy_warnings", []),
                "drug_interactions": response.get("drug_interactions", [])
            }
            log_interaction(log_entry)

            # ask to show JSON
            show_json = input("\n📊 Show detailed JSON response? (y/n): ").strip().lower()
            if show_json in ("y", "yes"):
                print(json.dumps(response, indent=2, ensure_ascii=False))

            print("\n" + "=" * 66 + "\n")

    except KeyboardInterrupt:
        print("\nExiting — take care.")
        speak_text("Exiting. Take care.")

if __name__ == "__main__":
    main()