#!/usr/bin/env python3
"""
Dataset Expansion Script - Week 2 Improvement
Adds 20+ common missing diseases to expand model coverage from 21 to 40+ diseases
"""

import pandas as pd
import random
import os

def generate_disease_symptoms():
    """
    Generate synthetic symptom descriptions for 20+ missing common diseases
    Each disease gets 15-20 varied symptom descriptions
    """
    
    disease_symptom_templates = {
        'Appendicitis': [
            "sharp pain in lower right abdomen",
            "severe abdominal pain with nausea and vomiting",
            "lower right belly pain that started near belly button",
            "appendix pain with fever and loss of appetite",
            "sudden pain near navel that moves to lower right",
            "can't eat, stomach hurts badly on right side",
            "pressing on right abdomen causes severe pain",
            "abdominal pain worse with coughing or walking",
            "right side stomach pain with constipation",
            "acute pain lower right quadrant with fever",
            "appendicitis symptoms pain nausea fever",
            "tender abdomen right side can't stand straight",
            "sharp stabbing pain right lower belly",
            "pain started around belly button moved to right",
            "severe right abdominal pain with vomiting"
        ],
        
        'Kidney Stones': [
            "severe pain in back and side below ribs",
            "excruciating flank pain that comes in waves",
            "blood in urine with sharp back pain",
            "kidney pain radiating to lower abdomen and groin",
            "painful urination with pink or red urine",
            "intense cramping in back and side",
            "nausea with severe pain in kidney area",
            "sharp pain below ribcage that won't go away",
            "passing kidney stones painful urination blood",
            "waves of pain in back moving to groin",
            "can't get comfortable pain in kidney region",
            "cloudy urine with bad smell and pain",
            "renal colic severe back pain",
            "sharp pain when urinating blood in pee",
            "kidney stone attack pain nausea vomiting"
        ],
        
        'Gallstones': [
            "sudden pain in upper right abdomen",
            "gallbladder pain after eating fatty foods",
            "sharp pain below right ribcage",
            "pain between shoulder blades after meals",
            "intense pain in upper belly center",
            "nausea and vomiting with right side pain",
            "pain under right shoulder blade",
            "upper abdomen pain that lasts for hours",
            "gallstone attack severe right upper belly pain",
            "pain after eating fried or greasy food",
            "right upper quadrant pain with indigestion",
            "sudden severe pain below breastbone",
            "back pain between shoulders with nausea",
            "biliary colic pain upper right abdomen",
            "jaundice with abdominal pain yellowing skin"
        ],
        
        'Stroke': [
            "sudden numbness on one side of body",
            "face drooping on one side can't smile",
            "arm weakness unable to raise both arms",
            "speech difficulty slurred words confused",
            "sudden severe headache like never before",
            "vision problems in one or both eyes",
            "trouble walking dizziness loss of balance",
            "confusion can't understand what people say",
            "face arm speech symptoms sudden onset",
            "paralysis on one side of body sudden",
            "drooping face weak arm slurred speech",
            "worst headache of my life sudden onset",
            "can't move right side of body suddenly",
            "left side numbness facial droop",
            "stroke symptoms face drooping arm weakness"
        ],
        
        'Heart Attack': [
            "crushing chest pain pressure discomfort",
            "pain in chest spreading to left arm",
            "chest tightness with shortness of breath",
            "pain in jaw neck or back with chest discomfort",
            "cold sweat with severe chest pain",
            "feeling like elephant sitting on chest",
            "chest pain radiating down left arm",
            "nausea with chest pressure and anxiety",
            "upper body pain chest arms back neck jaw",
            "shortness of breath with or without chest pain",
            "sudden chest pain sweating feeling doom",
            "squeezing sensation in center of chest",
            "heart attack symptoms chest pain arm pain",
            "lightheaded dizzy with chest discomfort",
            "chest pain lasting more than few minutes"
        ],
        
        'Angina': [
            "chest pain or discomfort with exertion",
            "pressure or squeezing in chest during activity",
            "chest pain relieved by rest",
            "tight band around chest when walking",
            "chest discomfort spreading to shoulders",
            "pain in chest arms neck jaw back",
            "shortness of breath with chest tightness",
            "chest pain goes away after resting",
            "angina attack during physical activity",
            "pressure in chest when climbing stairs",
            "chest discomfort improves with nitroglycerin",
            "stable angina pain predictable pattern",
            "chest tightness during exercise",
            "pain subsides within 5 minutes of rest",
            "recurring chest pain with activity"
        ],
        
        'Meningitis': [
            "severe headache with stiff neck",
            "high fever with sensitivity to light",
            "stiff neck cannot touch chin to chest",
            "headache nausea vomiting confused",
            "photophobia severe headache neck stiffness",
            "altered mental status with fever",
            "rash that doesn't fade when pressed",
            "seizures with high fever and headache",
            "severe headache worst ever with fever",
            "neck rigidity cannot bend neck forward",
            "meningitis symptoms headache stiff neck fever",
            "confusion drowsiness with severe headache",
            "irritability with light sensitivity fever",
            "bulging fontanelle in infant with fever",
            "bacterial meningitis symptoms neck pain headache"
        ],
        
        'Sepsis': [
            "high fever with rapid heart rate",
            "confusion with signs of infection",
            "extreme pain or discomfort",
            "clammy or sweaty skin with chills",
            "shortness of breath rapid breathing",
            "feeling like might die sense of doom",
            "shivering extreme cold with fever",
            "low blood pressure with rapid pulse",
            "septic shock symptoms fever confusion",
            "severe infection spreading through body",
            "rapid breathing over 20 breaths per minute",
            "altered mental state with infection",
            "mottled skin poor circulation fever",
            "decreased urine output with infection",
            "sepsis symptoms fever confusion rapid breathing"
        ],
        
        'Anaphylaxis': [
            "severe allergic reaction throat swelling",
            "difficulty breathing after allergen exposure",
            "hives all over body itching swelling",
            "throat closing up can't swallow",
            "rapid pulse with dizziness after eating",
            "swollen tongue and lips trouble breathing",
            "anaphylactic shock sudden severe reaction",
            "wheezing difficulty breathing tight chest",
            "sudden drop in blood pressure dizziness",
            "itchy rash spreading rapidly all over",
            "feeling faint after bee sting",
            "severe reaction to food medication insect",
            "face swelling difficulty breathing hives",
            "nausea vomiting with breathing difficulty",
            "anaphylaxis symptoms throat swelling breathing trouble"
        ],
        
        'Allergic Reaction': [
            "itchy rash hives after exposure",
            "sneezing runny nose watery eyes",
            "skin rash red itchy bumps",
            "swelling of lips face throat",
            "itching without rash after contact",
            "allergic reaction to food medication",
            "hives breaking out after eating",
            "red itchy welts on skin",
            "mild swelling with itching",
            "allergic symptoms sneezing itching",
            "contact dermatitis red itchy rash",
            "seasonal allergies sneezing congestion",
            "food allergy symptoms stomach upset rash",
            "drug allergy rash itching swelling",
            "allergic response hives itching swelling"
        ],
        
        'Osteoporosis': [
            "back pain from fractured vertebrae",
            "loss of height over time",
            "stooped posture bent forward",
            "bone fracture easier than expected",
            "broken bone from minor fall",
            "chronic back pain weak bones",
            "vertebral compression fracture pain",
            "easily fractured bones osteoporosis",
            "height loss stooped posture",
            "fragile bones frequent fractures",
            "low bone density fracture risk",
            "spinal compression fractures pain",
            "brittle bones break easily",
            "bone weakness fractures with minimal trauma",
            "osteoporosis symptoms back pain height loss"
        ],
        
        'Gout': [
            "sudden severe pain in big toe",
            "joint pain swelling redness warmth",
            "big toe joint extremely painful",
            "gout attack intense joint pain",
            "swollen red hot joint overnight",
            "unbearable pain in toe joint",
            "acute gout flare big toe",
            "joint inflammation very tender",
            "pain so bad can't touch joint",
            "big toe swollen can't wear shoes",
            "gout symptoms toe pain swelling",
            "uric acid buildup joint pain",
            "sudden onset joint pain at night",
            "red shiny skin over swollen joint",
            "gout attack big toe excruciating pain"
        ],
        
        'Rheumatoid Arthritis': [
            "joint pain stiffness morning lasting hours",
            "swollen tender warm joints both hands",
            "symmetrical joint pain both sides",
            "morning stiffness lasting over 30 minutes",
            "fatigue with joint pain swelling",
            "small joints hands feet affected",
            "rheumatoid arthritis joint inflammation",
            "fingers swollen difficult to bend",
            "joint deformity with chronic pain",
            "rheumatoid nodules with joint pain",
            "autoimmune arthritis multiple joints",
            "bilateral joint pain hands wrists",
            "chronic inflammation joints morning stiffness",
            "RA symptoms joint pain swelling stiffness",
            "multiple joints affected symmetrically"
        ],
        
        'Osteoarthritis': [
            "joint pain worse with activity",
            "knee pain when walking stairs",
            "hip pain stiffness after rest",
            "joint stiffness in morning brief",
            "bone on bone grinding sensation",
            "joint pain improves with rest",
            "arthritis pain hands knees hips",
            "degenerative joint disease pain",
            "joint flexibility loss limited motion",
            "knee swelling pain walking",
            "osteoarthritis symptoms joint pain stiffness",
            "wear and tear arthritis",
            "joint pain worse end of day",
            "cartilage breakdown joint pain",
            "age-related arthritis joint discomfort"
        ],
        
        'Fibromyalgia': [
            "widespread pain all over body",
            "chronic widespread musculoskeletal pain",
            "fatigue even after sleeping",
            "tender points painful to touch",
            "sleep problems with body pain",
            "fibromyalgia symptoms pain fatigue",
            "cognitive difficulties fibro fog",
            "body aches pain exhaustion",
            "sensitive to touch pressure pain",
            "chronic pain syndrome widespread",
            "muscle pain stiffness fatigue",
            "pain in multiple body areas",
            "tender points neck shoulders back",
            "fibromyalgia pain fatigue memory problems",
            "widespread musculoskeletal pain chronic"
        ],
        
        'Chronic Fatigue Syndrome': [
            "extreme fatigue not relieved by rest",
            "exhaustion worsens with activity",
            "post-exertional malaise severe fatigue",
            "unrefreshing sleep still tired",
            "chronic exhaustion lasting months",
            "CFS symptoms severe fatigue weakness",
            "memory problems with extreme tiredness",
            "chronic fatigue unable to function",
            "debilitating fatigue brain fog",
            "severe exhaustion difficulty concentrating",
            "myalgic encephalomyelitis chronic fatigue",
            "profound fatigue not explained",
            "exercise makes fatigue much worse",
            "chronic fatigue syndrome tired all time",
            "extreme exhaustion lasting over 6 months"
        ],
        
        'Peptic Ulcer': [
            "burning stomach pain between meals",
            "upper abdominal pain relieved by eating",
            "stomach pain worse when hungry",
            "burning sensation in stomach",
            "indigestion with stomach pain",
            "peptic ulcer pain upper belly",
            "stomach pain wakes me at night",
            "burning pain below breastbone",
            "nausea with stomach discomfort",
            "stomach ulcer pain after eating",
            "upper abdomen burning pain",
            "gastric ulcer gnawing pain",
            "duodenal ulcer pain before meals",
            "stomach pain improves with antacids",
            "peptic ulcer symptoms stomach pain burning"
        ],
        
        'GERD': [
            "heartburn after eating meals",
            "acid reflux burning in chest",
            "sour taste in mouth regurgitation",
            "burning sensation behind breastbone",
            "chest pain after lying down",
            "GERD symptoms heartburn acid reflux",
            "difficulty swallowing with heartburn",
            "chronic cough from acid reflux",
            "bitter taste acid coming up",
            "heartburn worse at night lying",
            "gastroesophageal reflux burning chest",
            "acid backup into throat",
            "chronic heartburn several times week",
            "burning in chest after eating",
            "GERD acid reflux heartburn symptoms"
        ],
        
        'Irritable Bowel Syndrome': [
            "abdominal pain with bowel changes",
            "cramping relieved by bowel movement",
            "diarrhea alternating with constipation",
            "bloating with abdominal discomfort",
            "IBS symptoms cramping diarrhea",
            "stomach cramps with gas bloating",
            "bowel habits changed pain cramping",
            "mucus in stool with cramping",
            "abdominal pain diarrhea or constipation",
            "IBS flare cramping bloating",
            "irritable bowel abdominal pain",
            "functional bowel disorder cramping",
            "chronic abdominal pain bowel issues",
            "IBS symptoms pain bloating diarrhea",
            "spastic colon abdominal cramping"
        ],
        
        'Celiac Disease': [
            "diarrhea after eating gluten",
            "abdominal bloating with gluten",
            "weight loss despite eating",
            "chronic diarrhea malabsorption",
            "celiac disease gluten intolerance",
            "gluten sensitivity stomach pain",
            "bloating diarrhea after bread pasta",
            "malnutrition with digestive problems",
            "fatigue with chronic diarrhea",
            "abdominal pain eating wheat products",
            "celiac symptoms diarrhea bloating",
            "gluten triggers digestive symptoms",
            "intestinal damage from gluten",
            "chronic digestive issues gluten",
            "celiac disease diarrhea weight loss"
        ]
    }
    
    # Add more diseases to reach 20+
    additional_diseases = {
        'Sinusitis': [
            "facial pain and pressure around sinuses",
            "thick yellow or green nasal discharge",
            "nasal congestion stuffy nose",
            "pain in forehead cheeks nose",
            "sinus infection facial pain congestion",
            "postnasal drip with facial pressure",
            "headache from sinus pressure",
            "reduced sense of smell congestion",
            "sinus pain worse bending forward",
            "chronic sinusitis facial pain",
            "blocked nose facial tenderness",
            "sinus pressure headache congestion",
            "nasal discharge with facial pain",
            "sinusitis symptoms congestion pressure",
            "sinus infection pain green mucus"
        ],
        
        'Tonsillitis': [
            "severe sore throat difficulty swallowing",
            "swollen tonsils with white patches",
            "throat pain fever swollen glands",
            "tonsillitis red swollen tonsils",
            "painful swallowing with fever",
            "enlarged tonsils with pus",
            "throat infection swollen tonsils",
            "sore throat fever bad breath",
            "difficulty swallowing tonsils swollen",
            "tonsillitis symptoms throat pain fever",
            "white spots on tonsils sore throat",
            "swollen lymph nodes neck throat pain",
            "bacterial tonsillitis severe pain",
            "infected tonsils painful swallowing",
            "tonsillitis fever sore throat swelling"
        ]
    }
    
    disease_symptom_templates.update(additional_diseases)
    
    return disease_symptom_templates


def create_expanded_dataset():
    """
    Create expanded dataset combining existing + new diseases
    """
    
    print("📊 Dataset Expansion - Week 2")
    print("="*70)
    
    # Load existing dataset
    existing_df = pd.read_csv('data/symptom_disease.csv')
    print(f"✅ Loaded existing dataset: {len(existing_df)} samples, {existing_df['disease'].nunique()} diseases")
    
    # Generate new disease data
    new_disease_templates = generate_disease_symptoms()
    
    new_data = []
    for disease, symptom_list in new_disease_templates.items():
        for symptom in symptom_list:
            new_data.append({
                'symptom_text': symptom,
                'disease': disease
            })
    
    new_df = pd.DataFrame(new_data)
    print(f"✅ Generated new disease data: {len(new_df)} samples, {new_df['disease'].nunique()} diseases")
    
    # Combine datasets
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    
    # Shuffle the data
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save expanded dataset
    output_path = 'data/symptom_disease_expanded.csv'
    combined_df.to_csv(output_path, index=False)
    
    print(f"\n📈 Expansion Complete!")
    print(f"   Original: {len(existing_df)} samples, {existing_df['disease'].nunique()} diseases")
    print(f"   New: {len(new_df)} samples, {new_df['disease'].nunique()} diseases")
    print(f"   Combined: {len(combined_df)} samples, {combined_df['disease'].nunique()} diseases")
    print(f"   Saved to: {output_path}")
    
    # Show disease distribution
    print(f"\n📋 Disease Distribution:")
    disease_counts = combined_df['disease'].value_counts().sort_values(ascending=False)
    for disease, count in disease_counts.head(20).items():
        print(f"   {disease:<35s} {count:3d} samples")
    
    if len(disease_counts) > 20:
        print(f"   ... and {len(disease_counts) - 20} more diseases")
    
    return combined_df


if __name__ == '__main__':
    df = create_expanded_dataset()
    print("\n✅ Dataset expansion complete!")
    print("   Next step: Run data augmentation to increase samples per disease")
