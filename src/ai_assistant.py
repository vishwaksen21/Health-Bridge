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
                    return pd.read_csv(path)
                except Exception:
                    return pd.DataFrame(fallback)
            else:
                return pd.DataFrame(fallback)

        knowledge["diseases"] = try_read("diseases.csv", SAMPLE_DISEASES)
        knowledge["ingredients"] = try_read("ingredients.csv", SAMPLE_INGREDIENTS)
        knowledge["targets"] = try_read("targets.csv", SAMPLE_TARGETS)
        knowledge["herbs"] = try_read("herbs.csv", SAMPLE_HERBS)
    except Exception:
        # if anything fails
        knowledge["diseases"] = pd.DataFrame(SAMPLE_DISEASES)
        knowledge["ingredients"] = pd.DataFrame(SAMPLE_INGREDIENTS)
        knowledge["targets"] = pd.DataFrame(SAMPLE_TARGETS)
        knowledge["herbs"] = pd.DataFrame(SAMPLE_HERBS)
    return knowledge

# ------------------------------------------------------------------------------------
# Keep original function names but wire to fallbacks above
# ------------------------------------------------------------------------------------
def load_knowledge_base(data_dir="data") -> Dict:
    """Load all medical knowledge data from CSVs or fallback data."""
    raw = load_csv_or_fallback(data_dir)
    knowledge = {}

    # If pandas DataFrames, keep them; else they are lists/dicts
    knowledge["diseases"] = raw["diseases"]
    knowledge["ingredients"] = raw["ingredients"]
    knowledge["targets"] = raw["targets"]
    knowledge["herbs"] = raw["herbs"]

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
        if any(k in disease_l for k in ["fever", "headache", "pain"]) and "fever" in purpose or "pain" in purpose or "analgesic" in d.get("type", "").lower():
            matched.append(d)
        elif any(k in disease_l for k in ["stomach", "gastric", "gastro", "ulcer", "acidity", "indigestion"]) and any(k in purpose for k in ["acid", "gastric", "reflux", "motility"]):
            matched.append(d)
        else:
            # generic offer
            matched.append(d)
        if len(matched) >= top_n:
            break
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
        else:
            heuristics = [("Turmeric", 0.6), ("Ginger", 0.55), ("Neem", 0.45)]
        return heuristics[:5]

    # If embeddings present, try to use them (kept backward-compatible)
    try:
        if not os.path.exists(embeddings_path) or not os.path.exists(model_path):
            return suggest_ingredients_for_disease(disease, knowledge=knowledge)  # fallback recursion to heuristic
        emb = KeyedVectors.load(embeddings_path)
        model = joblib.load(model_path)
        ingredients = [l.strip() for l in open("data/nodes_ingredients.txt").read().splitlines() if l.strip()]
        lookup_name = disease_mapping.get(disease, disease)
        if lookup_name not in emb.key_to_index:
            return []
        scores = []
        for ing in ingredients:
            if ing in emb.key_to_index:
                feat = np.multiply(emb[ing], emb[lookup_name])
                proba = model.predict_proba([feat])[0, 1]
                scores.append((ing, float(proba)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:5]
    except Exception:
        return suggest_ingredients_for_disease(disease, knowledge=knowledge)

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
    Generate AI insights using multiple LLM providers in order of preference:
    1. OpenAI API (if OPENAI_API_KEY set)
    2. GitHub Models API (if GITHUB_TOKEN set)
    3. Azure OpenAI (if AZURE_ENDPOINT and AZURE_KEY set)
    4. Local heuristic fallback
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
            print(f"  [Note: OpenAI API call failed, trying alternatives...]")
    
    # Try GitHub Models API (Option 2)
    github_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT")
    if github_token:
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
            print(f"  [Note: GitHub Models API call failed, trying alternatives...]")
    
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
                return response.choices[0].message.content
        except Exception as e:
            print(f"  [Note: Azure OpenAI call failed, using local fallback...]")

    # Local Heuristic Fallback (Option 4)
    herbs_list = ", ".join([h for h, _ in herbal_recommendations[:4]]) if herbal_recommendations else "herbal options"
    drugs_list = ", ".join([d.get("name") for d in drug_recommendations[:4]]) if drug_recommendations else "appropriate medications"
    
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
    # Step 1: Predict disease
    try:
        if USE_ENHANCED:
            result = predict_disease_enhanced(user_input)
            disease = result.get('primary_disease')
            confidence = float(result.get('confidence', 0.0))
        else:
            predicted = predict_disease(user_input)
            if isinstance(predicted, tuple):
                disease, confidence = predicted
            else:
                disease = predicted
                confidence = 0.5
    except Exception:
        # fallback
        disease, confidence = ("General Symptom", 0.5)

    # Step 2: Get herbal recommendations
    herbal_recommendations = suggest_ingredients_for_disease(disease, knowledge=knowledge)

    # Step 3: Get pharma recommendations if enabled
    drug_recommendations = []
    drug_interactions = []
    allergy_warnings = []

    if include_drugs:
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
        "ai_insights": None
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