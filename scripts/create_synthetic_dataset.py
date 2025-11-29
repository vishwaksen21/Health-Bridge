"""
Create Synthetic Symptom Dataset for Training
Generates realistic symptom descriptions for common diseases
"""

import pandas as pd
import os
import random

def create_synthetic_symptom_dataset():
    """
    Create a synthetic dataset with symptom descriptions for training
    """
    
    # Disease definitions with realistic symptom variations
    disease_symptoms = {
        "Common Cold": [
            "runny nose and sneezing",
            "sore throat with cough",
            "nasal congestion and headache",
            "mild fever with runny nose",
            "sneezing and watery eyes",
            "stuffy nose and sore throat",
            "cough with nasal discharge",
            "throat pain and runny nose",
            "congestion with mild headache",
            "frequent sneezing with cough"
        ],
        "Influenza": [
            "high fever with body ache",
            "severe headache and fever",
            "chills with muscle pain",
            "fever and extreme fatigue",
            "body ache with high temperature",
            "fever chills and weakness",
            "muscle pain with fever",
            "severe fatigue and fever",
            "high fever with headache",
            "body pain and chills"
        ],
        "Malaria": [
            "high fever with chills",
            "fever and sweating episodes",
            "chills with headache",
            "periodic fever attacks",
            "fever with body ache",
            "shivering and high fever",
            "sweating with fever",
            "fever chills and nausea",
            "high temperature with weakness",
            "fever with vomiting"
        ],
        "Dengue": [
            "high fever with joint pain",
            "severe body ache and fever",
            "fever with rash",
            "joint pain and headache",
            "high fever with eye pain",
            "body pain with fever",
            "fever with bleeding gums",
            "severe headache and fever",
            "joint pain with high temperature",
            "fever and muscle pain"
        ],
        "Diabetes": [
            "frequent urination",
            "increased thirst and hunger",
            "excessive urination at night",
            "constant thirst",
            "frequent hunger with weight loss",
            "tiredness with increased thirst",
            "blurred vision and thirst",
            "slow healing wounds",
            "increased appetite with fatigue",
            "excessive thirst and urination"
        ],
        "Hypertension": [
            "severe headache",
            "chest pain with headache",
            "shortness of breath",
            "nosebleeds with headache",
            "dizziness and headache",
            "vision problems",
            "chest discomfort",
            "irregular heartbeat",
            "difficulty breathing",
            "pounding in chest"
        ],
        "Asthma": [
            "difficulty breathing",
            "wheezing and cough",
            "chest tightness",
            "shortness of breath at night",
            "wheezing with chest pain",
            "persistent cough",
            "breathing difficulty with exercise",
            "chest tightness and cough",
            "wheezing after exertion",
            "breathlessness with cough"
        ],
        "Gastroenteritis": [
            "diarrhea and vomiting",
            "stomach cramps with nausea",
            "loose stools and fever",
            "abdominal pain with diarrhea",
            "nausea and stomach upset",
            "vomiting with stomach pain",
            "watery diarrhea",
            "stomach cramps and fever",
            "nausea with loose motions",
            "vomiting and abdominal pain"
        ],
        "Migraine": [
            "severe throbbing headache",
            "headache with nausea",
            "pain on one side of head",
            "headache with sensitivity to light",
            "pulsating headache",
            "severe headache with vomiting",
            "headache with visual disturbances",
            "throbbing pain with nausea",
            "intense headache one side",
            "headache with light sensitivity"
        ],
        "Pneumonia": [
            "cough with phlegm",
            "fever with chest pain",
            "difficulty breathing and cough",
            "chest pain when breathing",
            "high fever with cough",
            "shortness of breath and fever",
            "productive cough with fever",
            "chest pain and fever",
            "breathing difficulty with cough",
            "fever and chesty cough"
        ],
        "Bronchitis": [
            "persistent cough with mucus",
            "chest discomfort and cough",
            "coughing up phlegm",
            "chest congestion",
            "wheezing with cough",
            "productive cough",
            "chest tightness with cough",
            "cough with colored mucus",
            "shortness of breath and cough",
            "persistent productive cough"
        ],
        "Urinary Tract Infection": [
            "burning sensation during urination",
            "frequent urge to urinate",
            "cloudy urine",
            "pelvic pain",
            "burning while urinating",
            "strong urge to urinate",
            "lower abdominal pain",
            "painful urination",
            "frequent urination with pain",
            "bladder discomfort"
        ],
        "Arthritis": [
            "joint pain and stiffness",
            "swollen joints",
            "joint stiffness in morning",
            "pain in multiple joints",
            "joint swelling and pain",
            "stiff joints after rest",
            "joint pain with movement",
            "swelling in hands and feet",
            "joint pain and reduced mobility",
            "morning stiffness in joints"
        ],
        "Tuberculosis": [
            "persistent cough lasting weeks",
            "coughing up blood",
            "chest pain with cough",
            "night sweats and fever",
            "weight loss and fatigue",
            "chronic cough with blood",
            "fever with night sweats",
            "persistent cough with weight loss",
            "chest pain and fatigue",
            "cough lasting more than 3 weeks"
        ],
        "COVID-19": [
            "fever with dry cough",
            "loss of taste and smell",
            "difficulty breathing",
            "fever and fatigue",
            "dry cough with fever",
            "breathing difficulty and fever",
            "loss of smell and taste",
            "fever with body ache",
            "shortness of breath",
            "cough with loss of taste"
        ],
        "Typhoid": [
            "prolonged fever",
            "fever with abdominal pain",
            "headache and weakness",
            "fever with constipation",
            "high fever lasting days",
            "fever with loss of appetite",
            "abdominal pain with fever",
            "fever and fatigue",
            "prolonged high temperature",
            "fever with digestive issues"
        ],
        "Chickenpox": [
            "itchy rash with blisters",
            "fever with skin rash",
            "red spots turning to blisters",
            "itchy bumps on skin",
            "rash with fever",
            "blisters all over body",
            "itchy red rash",
            "fever with itchy spots",
            "skin eruptions with itching",
            "red bumps turning to blisters"
        ],
        "Measles": [
            "high fever with rash",
            "red rash spreading",
            "fever with cough and rash",
            "spots behind ears",
            "rash with fever",
            "red spots spreading from face",
            "fever with runny nose and rash",
            "measles rash with cough",
            "fever and red skin rash",
            "rash starting on face"
        ],
        "Hypothyroidism": [
            "fatigue and weight gain",
            "cold sensitivity",
            "constipation and fatigue",
            "dry skin and hair loss",
            "weight gain with tiredness",
            "feeling cold and tired",
            "sluggishness and weight gain",
            "muscle weakness and fatigue",
            "cold intolerance with fatigue",
            "unexplained weight gain"
        ],
        "Hyperthyroidism": [
            "weight loss with increased appetite",
            "rapid heartbeat",
            "nervousness and anxiety",
            "trembling hands",
            "weight loss and sweating",
            "increased heart rate",
            "anxiety with weight loss",
            "heat intolerance",
            "sweating and tremors",
            "rapid pulse with nervousness"
        ],
        "Anemia": [
            "fatigue and weakness",
            "pale skin",
            "shortness of breath",
            "dizziness and fatigue",
            "weakness and pallor",
            "tiredness with pale complexion",
            "breathlessness with fatigue",
            "weakness and dizziness",
            "fatigue with pale skin",
            "tiredness and shortness of breath"
        ]
    }
    
    # Generate dataset with variations
    data = []
    
    # Add base symptoms
    for disease, symptom_list in disease_symptoms.items():
        for symptom in symptom_list:
            data.append({
                'symptom_text': symptom,
                'disease': disease
            })
    
    # Add variations with templates
    templates = [
        "I have {symptoms}",
        "Experiencing {symptoms}",
        "Suffering from {symptoms}",
        "{symptoms} for past few days",
        "Recently developed {symptoms}",
        "Feeling {symptoms}",
        "Having {symptoms}",
        "{symptoms} since yesterday"
    ]
    
    for disease, symptom_list in disease_symptoms.items():
        for symptom in symptom_list[:5]:  # Only first 5 to avoid too much data
            template = random.choice(templates)
            variation = template.format(symptoms=symptom)
            data.append({
                'symptom_text': variation,
                'disease': disease
            })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df


def main():
    """Create and save the synthetic dataset"""
    
    print("🔨 Creating synthetic symptom dataset...")
    
    # Create dataset
    df = create_synthetic_symptom_dataset()
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save to CSV
    output_path = "data/symptom_disease.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Dataset created successfully!")
    print(f"   • File: {output_path}")
    print(f"   • Total samples: {len(df)}")
    print(f"   • Unique diseases: {df['disease'].nunique()}")
    print(f"   • Diseases: {', '.join(sorted(df['disease'].unique()))}")
    
    # Show sample
    print(f"\n📋 Sample entries:")
    print(df.head(10).to_string(index=False))
    
    # Show distribution
    print(f"\n📊 Disease distribution:")
    print(df['disease'].value_counts().head(10))
    
    return df


if __name__ == "__main__":
    main()
