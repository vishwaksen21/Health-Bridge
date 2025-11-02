"""
Pharmaceutical Drug & Tablet Database

Comprehensive database of common medications available in medical stores
organized by disease type. Includes dosage information and common side effects.
"""

import pandas as pd
from typing import Dict, List, Tuple

# Comprehensive pharmaceutical database
PHARMACEUTICAL_DATABASE = {
    "Diabetes": {
        "description": "Blood sugar management and diabetes treatment",
        "drugs": [
            {
                "name": "Metformin",
                "brand_names": ["Glucophage", "Diabex", "Formetic"],
                "type": "Oral",
                "dosage": "500-2000 mg daily (divided doses)",
                "purpose": "First-line treatment, reduces blood glucose",
                "availability": "Very Common - Medical Store",
                "price_range": "₹30-200 per tablet",
                "side_effects": "GI upset, metallic taste, B12 deficiency"
            },
            {
                "name": "Glibenclamide",
                "brand_names": ["Daonil", "Euglucon"],
                "type": "Oral",
                "dosage": "5-20 mg daily",
                "purpose": "Stimulates insulin release",
                "availability": "Common - Medical Store",
                "price_range": "₹15-100 per tablet",
                "side_effects": "Hypoglycemia, weight gain"
            },
            {
                "name": "Pioglitazone",
                "brand_names": ["Actos", "Glipizone"],
                "type": "Oral",
                "dosage": "15-45 mg daily",
                "purpose": "Improves insulin sensitivity",
                "availability": "Common - Medical Store",
                "price_range": "₹40-300 per tablet",
                "side_effects": "Weight gain, fluid retention, bone loss"
            },
            {
                "name": "Insulin (Rapid-acting)",
                "brand_names": ["Novolog", "Apidra", "Humalog"],
                "type": "Injection",
                "dosage": "Individualized, before meals",
                "purpose": "Direct blood glucose control",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-500 per vial",
                "side_effects": "Hypoglycemia, injection site reaction"
            },
            {
                "name": "Sitagliptin",
                "brand_names": ["Januvia", "Siglist"],
                "type": "Oral",
                "dosage": "100 mg daily",
                "purpose": "DPP-4 inhibitor, moderates blood glucose",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹150-400 per tablet",
                "side_effects": "Upper respiratory infection, headache"
            }
        ]
    },
    
    "Heart Disease": {
        "description": "Cardiovascular health and heart condition management",
        "drugs": [
            {
                "name": "Atorvastatin",
                "brand_names": ["Lipitor", "Storvas", "Atorlip"],
                "type": "Oral",
                "dosage": "10-80 mg daily",
                "purpose": "Reduces cholesterol, prevents heart disease",
                "availability": "Very Common - Medical Store",
                "price_range": "₹20-150 per tablet",
                "side_effects": "Muscle pain, liver issues, memory problems"
            },
            {
                "name": "Aspirin",
                "brand_names": ["Disperin", "Ecosprin", "Aspirin 75"],
                "type": "Oral",
                "dosage": "75-325 mg daily",
                "purpose": "Blood thinner, prevents clots",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹5-50 per tablet",
                "side_effects": "GI bleeding, allergic reactions"
            },
            {
                "name": "Amlodipine",
                "brand_names": ["Norvasc", "Amlong", "Cardace"],
                "type": "Oral",
                "dosage": "2.5-10 mg daily",
                "purpose": "Blood pressure control",
                "availability": "Very Common - Medical Store",
                "price_range": "₹15-100 per tablet",
                "side_effects": "Edema, headache, dizziness"
            },
            {
                "name": "Metoprolol",
                "brand_names": ["Lopressor", "Betaloc"],
                "type": "Oral",
                "dosage": "50-190 mg daily",
                "purpose": "Beta-blocker, reduces heart rate and BP",
                "availability": "Common - Medical Store",
                "price_range": "₹20-80 per tablet",
                "side_effects": "Fatigue, dizziness, cold extremities"
            },
            {
                "name": "Lisinopril",
                "brand_names": ["Prinivil", "Casopin", "Zestril"],
                "type": "Oral",
                "dosage": "10-40 mg daily",
                "purpose": "ACE inhibitor, reduces BP and protects heart",
                "availability": "Common - Medical Store",
                "price_range": "₹25-120 per tablet",
                "side_effects": "Dry cough, dizziness, hyperkalemia"
            }
        ]
    },
    
    "Asthma": {
        "description": "Respiratory disease and breathing support",
        "drugs": [
            {
                "name": "Salbutamol",
                "brand_names": ["Ventolin", "Asthalin", "Budecort"],
                "type": "Inhaler/Oral",
                "dosage": "100-200 mcg per dose, as needed",
                "purpose": "Quick relief from asthma symptoms",
                "availability": "Very Common - Medical Store",
                "price_range": "₹50-300 per inhaler",
                "side_effects": "Tremors, tachycardia, anxiety"
            },
            {
                "name": "Beclomethasone",
                "brand_names": ["Beclovent", "Budecort", "Beclate"],
                "type": "Inhaler",
                "dosage": "50-200 mcg twice daily",
                "purpose": "Long-term asthma control, reduces inflammation",
                "availability": "Common - Medical Store",
                "price_range": "₹100-400 per inhaler",
                "side_effects": "Oral thrush, hoarseness"
            },
            {
                "name": "Montelukast",
                "brand_names": ["Singulair", "Montair", "Onceair"],
                "type": "Oral",
                "dosage": "4-10 mg daily",
                "purpose": "Leukotriene inhibitor, prevents asthma attacks",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹100-300 per tablet",
                "side_effects": "Behavior changes, depression, headache"
            },
            {
                "name": "Theophylline",
                "brand_names": ["Nuelin", "Asmaril"],
                "type": "Oral",
                "dosage": "300-600 mg daily (divided)",
                "purpose": "Bronchodilator, opens airways",
                "availability": "Medical Store",
                "price_range": "₹30-100 per tablet",
                "side_effects": "Nausea, insomnia, arrhythmias"
            },
            {
                "name": "Ipratropium",
                "brand_names": ["Atrovent", "Ipravent"],
                "type": "Inhaler",
                "dosage": "20-40 mcg three times daily",
                "purpose": "Anticholinergic bronchodilator",
                "availability": "Medical Store",
                "price_range": "₹200-500 per inhaler",
                "side_effects": "Dry mouth, urinary retention"
            }
        ]
    },
    
    "Depression": {
        "description": "Mental health and mood disorder treatment",
        "drugs": [
            {
                "name": "Sertraline",
                "brand_names": ["Zoloft", "Zolsert", "Setarox"],
                "type": "Oral",
                "dosage": "50-200 mg daily",
                "purpose": "SSRI, increases serotonin levels",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹80-300 per tablet",
                "side_effects": "Sexual dysfunction, sleep issues, nausea"
            },
            {
                "name": "Escitalopram",
                "brand_names": ["Lexapro", "Escitalem"],
                "type": "Oral",
                "dosage": "10-20 mg daily",
                "purpose": "SSRI, antidepressant",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹100-400 per tablet",
                "side_effects": "Insomnia, tremors, sexual dysfunction"
            },
            {
                "name": "Amitriptyline",
                "brand_names": ["Elavil", "Tryptyline"],
                "type": "Oral",
                "dosage": "25-100 mg daily",
                "purpose": "Tricyclic antidepressant",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹20-80 per tablet",
                "side_effects": "Dry mouth, weight gain, drowsiness"
            },
            {
                "name": "Fluoxetine",
                "brand_names": ["Prozac", "Fluoxil"],
                "type": "Oral",
                "dosage": "20-80 mg daily",
                "purpose": "SSRI, long-acting antidepressant",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹100-250 per capsule",
                "side_effects": "Insomnia, anxiety, sexual dysfunction"
            },
            {
                "name": "Lorazepam",
                "brand_names": ["Ativan", "Loram"],
                "type": "Oral",
                "dosage": "0.5-4 mg daily (divided)",
                "purpose": "Benzodiazepine, anti-anxiety",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "Dependence, sedation, memory issues"
            }
        ]
    },
    
    "COVID-19": {
        "description": "Coronavirus infection treatment and symptom management",
        "drugs": [
            {
                "name": "Remdesivir",
                "brand_names": ["Veklury", "Gileadmivir"],
                "type": "Injection",
                "dosage": "200 mg loading, 100 mg daily",
                "purpose": "Antiviral, reduces severity",
                "availability": "Hospital/Medical Store (Prescription)",
                "price_range": "₹5,000-10,000 per vial",
                "side_effects": "Liver damage, catheter pain"
            },
            {
                "name": "Paracetamol",
                "brand_names": ["Calpol", "Dolo 650", "Panadol"],
                "type": "Oral",
                "dosage": "500-1000 mg every 6 hours",
                "purpose": "Fever and pain management",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹5-30 per tablet",
                "side_effects": "Rare - liver toxicity if overdosed"
            },
            {
                "name": "Azithromycin",
                "brand_names": ["Azee", "Zithromax"],
                "type": "Oral",
                "dosage": "500 mg daily for 3-5 days",
                "purpose": "Antibiotic, prevents secondary infections",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹100-300 per tablet",
                "side_effects": "Nausea, QT prolongation, diarrhea"
            },
            {
                "name": "Dexamethasone",
                "brand_names": ["Decadron", "Dexamethasone"],
                "type": "Oral/Injection",
                "dosage": "6-8 mg daily",
                "purpose": "Corticosteroid, reduces inflammation",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹20-100 per dose",
                "side_effects": "Hyperglycemia, immune suppression"
            },
            {
                "name": "Tocilizumab",
                "brand_names": ["Actemra"],
                "type": "Injection",
                "dosage": "4-8 mg/kg single dose",
                "purpose": "Immunosuppressant, reduces cytokine storm",
                "availability": "Hospital Only (Prescription)",
                "price_range": "₹10,000-50,000 per vial",
                "side_effects": "Infection risk, liver damage"
            }
        ]
    },
    
    "Bronchitis": {
        "description": "Respiratory tract inflammation and cough management",
        "drugs": [
            {
                "name": "Amoxicillin",
                "brand_names": ["Augmentin", "Amoxyclav", "Acmox"],
                "type": "Oral",
                "dosage": "500 mg thrice daily",
                "purpose": "Antibiotic, treats bacterial infection",
                "availability": "Very Common - Medical Store",
                "price_range": "₹20-100 per tablet",
                "side_effects": "Allergic reactions, diarrhea, rash"
            },
            {
                "name": "Cough Syrup (Guaifenesin)",
                "brand_names": ["Mucinex", "Robitussin", "Actikuf"],
                "type": "Syrup",
                "dosage": "5-10 ml every 4-6 hours",
                "purpose": "Expectorant, clears mucus",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹50-150 per bottle",
                "side_effects": "Nausea, vomiting, headache"
            },
            {
                "name": "Salbutamol",
                "brand_names": ["Asthalin", "Ventolin"],
                "type": "Inhaler",
                "dosage": "100-200 mcg, as needed",
                "purpose": "Bronchodilator, relieves symptoms",
                "availability": "Common - Medical Store",
                "price_range": "₹50-300 per inhaler",
                "side_effects": "Tremors, tachycardia"
            },
            {
                "name": "Codeine",
                "brand_names": ["Codeimed", "Tixylix"],
                "type": "Syrup/Tablet",
                "dosage": "15-30 mg every 6-8 hours",
                "purpose": "Cough suppressant",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹80-200 per bottle",
                "side_effects": "Drowsiness, constipation, dependence"
            },
            {
                "name": "Salbutamol + Guaifenesin",
                "brand_names": ["Bronchodil", "Asthalin-GX"],
                "type": "Syrup",
                "dosage": "5 ml thrice daily",
                "purpose": "Combined bronchodilation and expectorant",
                "availability": "Medical Store",
                "price_range": "₹100-250 per bottle",
                "side_effects": "Nausea, headache, tremors"
            }
        ]
    },
    
    "Malaria": {
        "description": "Parasitic infection treatment",
        "drugs": [
            {
                "name": "Artemether",
                "brand_names": ["Artesunate", "Artemotil"],
                "type": "Injection",
                "dosage": "3.2 mg/kg daily for 3 days",
                "purpose": "First-line treatment, highly effective",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹500-2000 per vial",
                "side_effects": "Hemolysis, neurotoxicity (rare)"
            },
            {
                "name": "Chloroquine",
                "brand_names": ["Avloclor", "Chloroquine"],
                "type": "Oral",
                "dosage": "600 mg daily for 3 days",
                "purpose": "Treats Plasmodium vivax and ovale",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹30-150 per tablet",
                "side_effects": "Vision problems, itching, nausea"
            },
            {
                "name": "Primaquine",
                "brand_names": ["Primacine"],
                "type": "Oral",
                "dosage": "15-30 mg daily for 14 days",
                "purpose": "Eliminates dormant parasites",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per tablet",
                "side_effects": "Hemolysis (G6PD deficiency), abdominal pain"
            },
            {
                "name": "Lumefantrine + Artemether",
                "brand_names": ["Coartem", "Artemin"],
                "type": "Oral",
                "dosage": "As per body weight",
                "purpose": "Artemisinin-based combination therapy",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-800 per tablet",
                "side_effects": "Headache, myalgia, diarrhea"
            },
            {
                "name": "Quinine",
                "brand_names": ["Quinorm"],
                "type": "Injection",
                "dosage": "10 mg/kg every 8 hours",
                "purpose": "Alternative for severe malaria",
                "availability": "Hospital/Medical Store (Prescription)",
                "price_range": "₹500-1500 per vial",
                "side_effects": "Cinchonism, hypoglycemia, thrombosis"
            }
        ]
    },
    
    "Impetigo": {
        "description": "Bacterial skin infection treatment",
        "drugs": [
            {
                "name": "Mupirocin Ointment",
                "brand_names": ["Bactroban", "Mupirocin"],
                "type": "Topical",
                "dosage": "Apply locally 3 times daily",
                "purpose": "Topical antibiotic for mild cases",
                "availability": "Common - Medical Store (OTC)",
                "price_range": "₹100-300 per tube",
                "side_effects": "Local irritation, pruritus"
            },
            {
                "name": "Cephalexin",
                "brand_names": ["Ceporex", "Lexinorm"],
                "type": "Oral",
                "dosage": "500 mg four times daily",
                "purpose": "Cephalosporin antibiotic",
                "availability": "Common - Medical Store",
                "price_range": "₹50-200 per tablet",
                "side_effects": "Allergic reactions, diarrhea"
            },
            {
                "name": "Cloxacillin",
                "brand_names": ["Orbenin", "Cloxapen"],
                "type": "Oral",
                "dosage": "500 mg four times daily",
                "purpose": "Beta-lactamase resistant penicillin",
                "availability": "Common - Medical Store",
                "price_range": "₹30-100 per tablet",
                "side_effects": "Nausea, diarrhea, rash"
            },
            {
                "name": "Tetracycline",
                "brand_names": ["Tetdox"],
                "type": "Oral",
                "dosage": "250-500 mg four times daily",
                "purpose": "Broad-spectrum antibiotic",
                "availability": "Medical Store",
                "price_range": "₹20-80 per tablet",
                "side_effects": "Sun sensitivity, discoloration in children"
            },
            {
                "name": "Bacitracin + Neomycin Ointment",
                "brand_names": ["Polysporin", "Triple Antibiotic"],
                "type": "Topical",
                "dosage": "Apply locally 2-3 times daily",
                "purpose": "Combined antibiotic coverage",
                "availability": "Medical Store (OTC)",
                "price_range": "₹150-400 per tube",
                "side_effects": "Local irritation, allergic reactions"
            }
        ]
    },
    
    "GERD": {
        "description": "Acid reflux and digestive disorder management",
        "drugs": [
            {
                "name": "Omeprazole",
                "brand_names": ["Prilosec", "Omez", "Omeprol"],
                "type": "Oral",
                "dosage": "20-40 mg daily",
                "purpose": "Proton pump inhibitor, reduces acid",
                "availability": "Very Common - Medical Store",
                "price_range": "₹30-150 per tablet",
                "side_effects": "Long-term B12 deficiency, headache"
            },
            {
                "name": "Ranitidine",
                "brand_names": ["Zantac", "Rantac"],
                "type": "Oral",
                "dosage": "150 mg twice daily",
                "purpose": "H2 blocker, reduces acid production",
                "availability": "Common - Medical Store",
                "price_range": "₹20-100 per tablet",
                "side_effects": "Headache, constipation, diarrhea"
            },
            {
                "name": "Antacid (Aluminum Hydroxide)",
                "brand_names": ["Maalox", "Gelusil", "Mucaine"],
                "type": "Oral/Syrup",
                "dosage": "As needed after meals",
                "purpose": "Neutralizes stomach acid",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹30-100",
                "side_effects": "Constipation, interference with other meds"
            },
            {
                "name": "Pantoprazole",
                "brand_names": ["Pantocid", "Pantogar"],
                "type": "Oral/Injection",
                "dosage": "40 mg daily",
                "purpose": "PPI, long-acting acid reduction",
                "availability": "Common - Medical Store",
                "price_range": "₹80-300 per tablet",
                "side_effects": "Headache, diarrhea, B12 deficiency"
            },
            {
                "name": "Domperidone",
                "brand_names": ["Motilium", "Domperidon"],
                "type": "Oral",
                "dosage": "10-20 mg thrice daily",
                "purpose": "Promotes gastric motility",
                "availability": "Common - Medical Store",
                "price_range": "₹30-120 per tablet",
                "side_effects": "Headache, diarrhea, rare cardiac issues"
            }
        ]
    },
    
    "Dengue": {
        "description": "Viral fever management and symptom relief",
        "drugs": [
            {
                "name": "Paracetamol",
                "brand_names": ["Calpol", "Dolo 650", "Panadol"],
                "type": "Oral",
                "dosage": "500-1000 mg every 6 hours",
                "purpose": "Fever and pain management",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹5-30 per tablet",
                "side_effects": "Rare - liver toxicity if overdosed"
            },
            {
                "name": "Ibuprofen",
                "brand_names": ["Brufen", "Combiflam"],
                "type": "Oral",
                "dosage": "400-600 mg every 6-8 hours",
                "purpose": "Anti-inflammatory, pain and fever relief",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹20-100 per tablet",
                "side_effects": "GI upset, bleeding (avoid in dengue hemorrhagic)"
            },
            {
                "name": "Platelet Transfusion",
                "brand_names": ["Blood Bank", "Medical Grade"],
                "type": "Transfusion",
                "dosage": "As per requirement",
                "purpose": "For severe thrombocytopenia",
                "availability": "Hospital/Blood Bank (Prescription)",
                "price_range": "₹3,000-5,000 per unit",
                "side_effects": "Transfusion reactions, infection risk"
            },
            {
                "name": "Oral Rehydration Solution",
                "brand_names": ["ORS Packets", "Electral", "Glucon-D"],
                "type": "Oral Solution",
                "dosage": "As tolerated, frequently",
                "purpose": "Fluid and electrolyte replacement",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-50 per packet",
                "side_effects": "None - safe for all ages"
            },
            {
                "name": "Chlorpheniramine",
                "brand_names": ["Phenergan", "Avil"],
                "type": "Oral/Injection",
                "dosage": "4-6 mg every 6-8 hours",
                "purpose": "Antihistamine, reduces allergic reactions",
                "availability": "Common - Medical Store",
                "price_range": "₹10-50 per tablet",
                "side_effects": "Drowsiness, dry mouth"
            }
        ]
    },

    "Fever": {
        "description": "High fever management and symptomatic relief",
        "drugs": [
            {
                "name": "Paracetamol",
                "brand_names": ["Calpol", "Dolo 650", "Panadol"],
                "type": "Oral",
                "dosage": "500-1000 mg every 6 hours",
                "purpose": "Fever and pain management",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹5-30 per tablet",
                "side_effects": "Rare - liver toxicity if overdosed"
            },
            {
                "name": "Ibuprofen",
                "brand_names": ["Brufen", "Combiflam"],
                "type": "Oral",
                "dosage": "400-600 mg every 6-8 hours",
                "purpose": "Anti-inflammatory, pain and fever relief",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹20-100 per tablet",
                "side_effects": "GI upset, heartburn"
            },
            {
                "name": "Aspirin",
                "brand_names": ["Disperin", "Aspirin 500"],
                "type": "Oral",
                "dosage": "325-650 mg every 4-6 hours",
                "purpose": "Fever reduction and pain relief",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-40 per tablet",
                "side_effects": "GI bleeding, allergic reactions"
            },
            {
                "name": "Nimesulide",
                "brand_names": ["Nimulid", "Nimsaid"],
                "type": "Oral",
                "dosage": "100-200 mg twice daily",
                "purpose": "NSAID for fever and inflammation",
                "availability": "Very Common - Medical Store",
                "price_range": "₹20-60 per tablet",
                "side_effects": "GI upset, liver issues in long-term use"
            },
            {
                "name": "Metamizole",
                "brand_names": ["Novalgin", "Analgin"],
                "type": "Oral/Injection",
                "dosage": "500-1000 mg every 6-8 hours",
                "purpose": "Potent fever and pain reliever",
                "availability": "Common - Medical Store",
                "price_range": "₹15-50 per tablet",
                "side_effects": "Rare agranulocytosis, allergic reactions"
            }
        ]
    },

    "Cold": {
        "description": "Common cold and viral infection management",
        "drugs": [
            {
                "name": "Cough Syrup (Guaifenesin)",
                "brand_names": ["Mucinex", "Robitussin", "Actikuf"],
                "type": "Syrup",
                "dosage": "5-10 ml every 4-6 hours",
                "purpose": "Expectorant, clears mucus",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹50-150 per bottle",
                "side_effects": "Nausea, vomiting, headache"
            },
            {
                "name": "Paracetamol",
                "brand_names": ["Calpol", "Dolo 650", "Panadol"],
                "type": "Oral",
                "dosage": "500-1000 mg every 6 hours",
                "purpose": "Fever and body ache relief",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹5-30 per tablet",
                "side_effects": "Rare - liver toxicity if overdosed"
            },
            {
                "name": "Cetirizine",
                "brand_names": ["Allerdin", "Histacet"],
                "type": "Oral",
                "dosage": "10 mg once daily",
                "purpose": "Antihistamine for allergy and runny nose",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-40 per tablet",
                "side_effects": "Drowsiness, dry mouth"
            },
            {
                "name": "Decongestant Nasal Spray",
                "brand_names": ["Nasivion", "Otrivin"],
                "type": "Nasal Spray",
                "dosage": "1-2 sprays in each nostril every 8-12 hours",
                "purpose": "Nasal congestion relief",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹30-80 per bottle",
                "side_effects": "Nasal irritation, rebound congestion with overuse"
            },
            {
                "name": "Vitamin C Supplement",
                "brand_names": ["Celin", "Ascorbic Acid"],
                "type": "Oral",
                "dosage": "500-1000 mg daily",
                "purpose": "Immune support and cold recovery",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "None at recommended doses"
            }
        ]
    },
    
    "Arthritis": {
        "description": "Joint inflammation, arthritis, and musculoskeletal pain management",
        "drugs": [
            {
                "name": "Ibuprofen",
                "brand_names": ["Brufen", "Combiflam", "Ibugesic"],
                "type": "Oral",
                "dosage": "200-400 mg every 6-8 hours",
                "purpose": "NSAID, reduces inflammation and joint pain",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "GI upset, ulcers, kidney issues with long-term use"
            },
            {
                "name": "Naproxen",
                "brand_names": ["Naprosyn", "Aleve", "Naprokind"],
                "type": "Oral",
                "dosage": "250-500 mg twice daily",
                "purpose": "Long-acting NSAID for arthritis pain",
                "availability": "Common - Medical Store",
                "price_range": "₹30-100 per tablet",
                "side_effects": "GI bleeding, cardiovascular issues, fluid retention"
            },
            {
                "name": "Meloxicam",
                "brand_names": ["Mobisyl", "Movon", "Metacam"],
                "type": "Oral",
                "dosage": "7.5-15 mg daily",
                "purpose": "NSAID, selective COX-2 inhibitor",
                "availability": "Medical Store",
                "price_range": "₹50-150 per tablet",
                "side_effects": "GI upset, cardiovascular events, rash"
            },
            {
                "name": "Diclofenac",
                "brand_names": ["Voveran", "Cataflam", "Diclogesic"],
                "type": "Oral/Injection/Topical",
                "dosage": "50-100 mg daily (divided doses)",
                "purpose": "Potent NSAID for moderate to severe joint pain",
                "availability": "Common - Medical Store",
                "price_range": "₹10-80 per tablet",
                "side_effects": "GI bleeding, liver/kidney issues, cardiovascular effects"
            },
            {
                "name": "Methotrexate",
                "brand_names": ["Methoblast", "Methotrexate"],
                "type": "Oral/Injection",
                "dosage": "7.5-25 mg weekly",
                "purpose": "DMARD, disease-modifying for rheumatoid arthritis",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-1000 per dose",
                "side_effects": "Bone marrow suppression, liver damage, infections"
            },
            {
                "name": "Sulfasalazine",
                "brand_names": ["Salazopyrin", "Azulfidine"],
                "type": "Oral",
                "dosage": "500-1000 mg twice daily",
                "purpose": "DMARD for rheumatoid arthritis",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-150 per tablet",
                "side_effects": "Nausea, rash, hepatotoxicity, blood dyscrasias"
            },
            {
                "name": "Leflunomide",
                "brand_names": ["Arava", "Lefno"],
                "type": "Oral",
                "dosage": "10-20 mg daily",
                "purpose": "DMARD for active rheumatoid arthritis",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹300-800 per tablet",
                "side_effects": "Hepatotoxicity, teratogenicity, GI upset"
            },
            {
                "name": "Prednisolone (Corticosteroid)",
                "brand_names": ["Omnacortil", "Predacort"],
                "type": "Oral",
                "dosage": "5-20 mg daily (tapered)",
                "purpose": "Anti-inflammatory for acute arthritis flares",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "Immunosuppression, weight gain, osteoporosis with chronic use"
            },
            {
                "name": "Calcium + Vitamin D",
                "brand_names": ["Shelcal", "Calcibind", "Bone Aid"],
                "type": "Oral",
                "dosage": "500 mg Ca + 200 IU Vit D twice daily",
                "purpose": "Bone health support, prevents osteoarthritis progression",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹20-100 per tablet",
                "side_effects": "Constipation, kidney stone risk"
            },
            {
                "name": "Glucosamine + Chondroitin",
                "brand_names": ["Osteo-Ease", "Joint-Care", "Glucartos"],
                "type": "Oral",
                "dosage": "1500 mg Glucosamine + 1200 mg Chondroitin daily",
                "purpose": "Joint cartilage support for osteoarthritis",
                "availability": "Common - Medical Store (OTC)",
                "price_range": "₹100-300 per tablet",
                "side_effects": "Mild GI upset, allergic reactions"
            }
        ]
    }
}

class DrugDatabase:
    """
    Comprehensive drug and pharmaceutical database manager.
    Provides access to medications organized by disease.
    """
    
    # Mapping of predicted disease names to database disease names
    DISEASE_MAPPING = {
        "Influenza": "Fever",
        "Viral Fever": "Fever",
        "Flu": "Fever",
        "COVID-19": "COVID-19",
        "Common Cold": "Cold",
        "Pharyngitis": "Cold",
        "Rhinitis": "Cold",
        "Laryngitis": "Cold",
        "Cough": "Cold",
        "Bronchitis": "Bronchitis",
        "Asthma": "Asthma",
        "Pneumonia": "Bronchitis",
        "Tuberculosis": "Bronchitis",
        "Malaria": "Malaria",
        "Dengue": "Dengue",
        "Chikungunya": "Dengue",
        "Depression": "Depression",
        "Anxiety": "Depression",
        "GERD": "GERD",
        "Gastroenteritis": "GERD",
        "Diarrhea": "GERD",
        "Impetigo": "Impetigo",
        "Skin Infection": "Impetigo",
        "Fever": "Fever",
        "Headache": "Fever",
        "Migraine": "Fever",
        "Body Ache": "Fever",
        "Hypothyroidism": "Fever",
        "Hyperthyroidism": "Fever",
        "Thyroid": "Fever",
        "Urticaria": "Fever",
        "Food Poisoning": "GERD",
        "Arthritis": "Arthritis",
        "Osteoarthritis": "Arthritis",
        "Rheumatoid Arthritis": "Arthritis",
        "Joint Pain": "Arthritis",
        "Gout": "Arthritis",
    }
    
    def __init__(self):
        """Initialize the drug database."""
        self.database = PHARMACEUTICAL_DATABASE
    
    def get_drugs_for_disease(self, disease: str) -> Dict:
        """Get all available drugs for a specific disease."""
        # First, try to map the disease name
        mapped_disease = self.DISEASE_MAPPING.get(disease.strip(), disease)
        disease_normalized = self._normalize_disease_name(mapped_disease)
        
        if disease_normalized in self.database:
            return self.database[disease_normalized]
        
        # Try partial match
        for key in self.database.keys():
            if disease_normalized.lower() in key.lower() or key.lower() in disease_normalized.lower():
                return self.database[key]
        
        return None
    
    def get_available_diseases(self) -> List[str]:
        """Get list of all diseases with drug information."""
        return list(self.database.keys())
    
    def get_drug_by_name(self, drug_name: str, disease: str = None) -> Dict:
        """Find a specific drug by name, optionally within a disease."""
        drug_name_lower = drug_name.lower()
        
        search_diseases = [disease] if disease else self.database.keys()
        
        for dis in search_diseases:
            disease_data = self.database.get(dis)
            if not disease_data:
                continue
            
            for drug in disease_data.get("drugs", []):
                if drug_name_lower in drug["name"].lower():
                    return drug
                
                for brand in drug.get("brand_names", []):
                    if drug_name_lower in brand.lower():
                        return drug
        
        return None
    
    def get_drugs_sorted_by_commonality(self, disease: str) -> List[Dict]:
        """Get drugs for a disease sorted by commonality/availability."""
        disease_data = self.get_drugs_for_disease(disease)
        if not disease_data:
            return []
        
        availability_order = [
            "Very Common - Medical Store (OTC)",
            "Very Common - Medical Store",
            "Common - Medical Store",
            "Common - Medical Store (OTC)",
            "Medical Store (OTC)",
            "Medical Store",
            "Hospital/Medical Store (Prescription)",
            "Hospital Only (Prescription)",
            "Medical Store (Prescription)"
        ]
        
        drugs = disease_data.get("drugs", [])
        
        def availability_score(drug):
            availability = drug.get("availability", "")
            try:
                return availability_order.index(availability)
            except ValueError:
                return len(availability_order)
        
        return sorted(drugs, key=availability_score)
    
    def _normalize_disease_name(self, disease: str) -> str:
        """Normalize disease name for matching."""
        return disease.strip().title()
    
    def export_to_csv(self, filename: str = "pharmaceutical_database.csv"):
        """Export database to CSV file."""
        rows = []
        
        for disease, data in self.database.items():
            for drug in data.get("drugs", []):
                row = {
                    "disease": disease,
                    "drug_name": drug.get("name"),
                    "brand_names": ", ".join(drug.get("brand_names", [])),
                    "type": drug.get("type"),
                    "dosage": drug.get("dosage"),
                    "purpose": drug.get("purpose"),
                    "availability": drug.get("availability"),
                    "price_range": drug.get("price_range"),
                    "side_effects": drug.get("side_effects")
                }
                rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        print(f"✅ Database exported to {filename}")
        return df


def get_drug_recommendations(disease: str, top_n: int = 5) -> List[Dict]:
    """
    Get top drug recommendations for a disease.
    
    Args:
        disease: Disease name
        top_n: Number of top recommendations to return
    
    Returns:
        List of drug recommendations sorted by commonality
    """
    db = DrugDatabase()
    drugs = db.get_drugs_sorted_by_commonality(disease)
    return drugs[:top_n]


if __name__ == "__main__":
    # Example usage
    db = DrugDatabase()
    
    print("Available Diseases:")
    print("-" * 50)
    for disease in db.get_available_diseases():
        print(f"  • {disease}")
    
    print("\n" + "="*50)
    print("Diabetes Medications:")
    print("="*50)
    
    diabetes_drugs = db.get_drugs_for_disease("Diabetes")
    if diabetes_drugs:
        for drug in diabetes_drugs["drugs"][:3]:
            print(f"\n{drug['name']}")
            print(f"  Brand Names: {', '.join(drug['brand_names'])}")
            print(f"  Dosage: {drug['dosage']}")
            print(f"  Availability: {drug['availability']}")
            print(f"  Price: {drug['price_range']}")
    
    # Export to CSV
    db.export_to_csv("data/pharmaceutical_database.csv")
