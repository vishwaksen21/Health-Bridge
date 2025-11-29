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
    },
    
    "Hypertension": {
        "description": "High blood pressure management",
        "drugs": [
            {
                "name": "Amlodipine",
                "brand_names": ["Norvasc", "Amlong", "Stamlo"],
                "type": "Calcium Channel Blocker",
                "dosage": "5-10 mg once daily",
                "purpose": "Lower blood pressure, prevent cardiovascular events",
                "availability": "Very Common - Medical Store",
                "price_range": "₹15-100 per tablet",
                "side_effects": "Ankle swelling, headache, dizziness"
            },
            {
                "name": "Telmisartan",
                "brand_names": ["Telma", "Telmikind", "Telmi"],
                "type": "ARB (Angiotensin Receptor Blocker)",
                "dosage": "40-80 mg once daily",
                "purpose": "Blood pressure control, kidney protection",
                "availability": "Very Common - Medical Store",
                "price_range": "₹30-150 per tablet",
                "side_effects": "Dizziness, hyperkalemia, kidney issues"
            },
            {
                "name": "Losartan",
                "brand_names": ["Cozaar", "Losacar", "Repace"],
                "type": "ARB",
                "dosage": "50-100 mg once daily",
                "purpose": "Blood pressure control",
                "availability": "Very Common - Medical Store",
                "price_range": "₹25-120 per tablet",
                "side_effects": "Dizziness, hyperkalemia"
            },
            {
                "name": "Atenolol",
                "brand_names": ["Tenormin", "Aten", "Atecor"],
                "type": "Beta Blocker",
                "dosage": "25-100 mg once daily",
                "purpose": "Blood pressure and heart rate control",
                "availability": "Very Common - Medical Store",
                "price_range": "₹10-60 per tablet",
                "side_effects": "Fatigue, cold hands, dizziness"
            },
            {
                "name": "Hydrochlorothiazide",
                "brand_names": ["Aquazide", "HCZ"],
                "type": "Diuretic",
                "dosage": "12.5-25 mg once daily",
                "purpose": "Blood pressure control via fluid reduction",
                "availability": "Very Common - Medical Store",
                "price_range": "₹5-40 per tablet",
                "side_effects": "Electrolyte imbalance, increased urination"
            }
        ]
    },
    
    "Urinary Tract Infection": {
        "description": "UTI and bladder infection treatment",
        "drugs": [
            {
                "name": "Nitrofurantoin",
                "brand_names": ["Macrobid", "Macrodantin"],
                "type": "Antibiotic",
                "dosage": "100 mg twice daily for 5-7 days",
                "purpose": "UTI treatment",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per course",
                "side_effects": "Nausea, brown urine, pulmonary toxicity (long-term)"
            },
            {
                "name": "Trimethoprim-Sulfamethoxazole",
                "brand_names": ["Bactrim", "Septran", "Co-trimoxazole"],
                "type": "Antibiotic",
                "dosage": "160/800 mg twice daily for 3-7 days",
                "purpose": "UTI treatment",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹30-150 per course",
                "side_effects": "Allergic reactions, GI upset, photosensitivity"
            },
            {
                "name": "Ciprofloxacin",
                "brand_names": ["Cifran", "Ciplox", "Cipro"],
                "type": "Fluoroquinolone Antibiotic",
                "dosage": "250-500 mg twice daily for 3-7 days",
                "purpose": "UTI and complicated infections",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹40-200 per course",
                "side_effects": "Tendon rupture risk, GI upset, photosensitivity"
            },
            {
                "name": "Phenazopyridine",
                "brand_names": ["Pyridium", "Uristat"],
                "type": "Urinary Analgesic",
                "dosage": "200 mg three times daily for 2 days",
                "purpose": "UTI pain relief (not antibiotic)",
                "availability": "Medical Store (OTC/Prescription)",
                "price_range": "₹50-150 per pack",
                "side_effects": "Orange urine, GI upset, kidney stones"
            }
        ]
    },
    
    "Kidney Stones": {
        "description": "Renal calculi treatment and prevention",
        "drugs": [
            {
                "name": "Tamsulosin",
                "brand_names": ["Flomax", "Urimax", "Contiflo"],
                "type": "Alpha Blocker",
                "dosage": "0.4 mg once daily",
                "purpose": "Facilitate stone passage, reduce urinary obstruction",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per tablet",
                "side_effects": "Dizziness, ejaculation problems, orthostatic hypotension"
            },
            {
                "name": "Diclofenac",
                "brand_names": ["Voveran", "Diclo", "Voltaren"],
                "type": "NSAID",
                "dosage": "50-75 mg twice daily as needed",
                "purpose": "Pain relief from kidney stone",
                "availability": "Very Common - Medical Store",
                "price_range": "₹10-50 per tablet",
                "side_effects": "GI upset, kidney issues with overuse"
            },
            {
                "name": "Potassium Citrate",
                "brand_names": ["K-Cit", "Urocit-K"],
                "type": "Alkalinizer",
                "dosage": "10-20 mEq twice daily",
                "purpose": "Prevent stone formation, alkalinize urine",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹100-300 per pack",
                "side_effects": "GI upset, hyperkalemia"
            },
            {
                "name": "Allopurinol",
                "brand_names": ["Zyloprim", "Zyloric"],
                "type": "Xanthine Oxidase Inhibitor",
                "dosage": "100-300 mg daily",
                "purpose": "Prevent uric acid stones",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹20-100 per tablet",
                "side_effects": "Rash, gout flare initially, liver issues"
            }
        ]
    },
    
    "Allergic Reaction": {
        "description": "Allergy and hypersensitivity management",
        "drugs": [
            {
                "name": "Cetirizine",
                "brand_names": ["Zyrtec", "Cetrizet", "Okacet"],
                "type": "Antihistamine",
                "dosage": "10 mg once daily",
                "purpose": "Allergic rhinitis, urticaria, itching",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "Drowsiness, dry mouth"
            },
            {
                "name": "Loratadine",
                "brand_names": ["Claritin", "Lorfast"],
                "type": "Non-sedating Antihistamine",
                "dosage": "10 mg once daily",
                "purpose": "Allergic symptoms without drowsiness",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹15-60 per tablet",
                "side_effects": "Minimal - headache rarely"
            },
            {
                "name": "Prednisolone",
                "brand_names": ["Omnacortil", "Wysolone"],
                "type": "Corticosteroid",
                "dosage": "20-60 mg daily (short course)",
                "purpose": "Severe allergic reactions",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "Immunosuppression, mood changes, weight gain"
            },
            {
                "name": "Epinephrine Auto-injector",
                "brand_names": ["EpiPen", "Anapen"],
                "type": "Emergency Injection",
                "dosage": "0.3 mg IM (single dose)",
                "purpose": "Anaphylaxis emergency treatment",
                "availability": "Hospital/Medical Store (Prescription)",
                "price_range": "₹2000-5000 per injector",
                "side_effects": "Tachycardia, anxiety, tremor"
            }
        ]
    },
    
    "Anemia": {
        "description": "Iron deficiency and blood disorder treatment",
        "drugs": [
            {
                "name": "Ferrous Sulfate",
                "brand_names": ["Fefol", "Ferium", "Dexorange"],
                "type": "Iron Supplement",
                "dosage": "325 mg once or twice daily",
                "purpose": "Iron deficiency anemia treatment",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹20-100 per pack",
                "side_effects": "Constipation, dark stools, nausea"
            },
            {
                "name": "Folic Acid",
                "brand_names": ["Folvite", "Acfol"],
                "type": "Vitamin B9",
                "dosage": "1-5 mg daily",
                "purpose": "Folate deficiency anemia",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-50 per pack",
                "side_effects": "Rare - GI upset"
            },
            {
                "name": "Vitamin B12 (Methylcobalamin)",
                "brand_names": ["Neurobion", "Methylcobal"],
                "type": "Vitamin B12",
                "dosage": "1000 mcg daily or injection",
                "purpose": "B12 deficiency anemia",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹50-200 per pack",
                "side_effects": "Rare - injection site reaction"
            },
            {
                "name": "Erythropoietin",
                "brand_names": ["Eprex", "NeoRecormon"],
                "type": "Injection",
                "dosage": "As prescribed (individualized)",
                "purpose": "Severe anemia, chronic kidney disease",
                "availability": "Hospital Only (Prescription)",
                "price_range": "₹1000-5000 per injection",
                "side_effects": "Hypertension, thrombosis risk"
            }
        ]
    },
    
    "Appendicitis": {
        "description": "Pre/post-operative appendicitis management",
        "drugs": [
            {
                "name": "Ceftriaxone + Metronidazole",
                "brand_names": ["Rocephin + Flagyl"],
                "type": "Antibiotic Combination",
                "dosage": "1-2g IV daily + 500mg IV 3x daily",
                "purpose": "Infection prevention/treatment",
                "availability": "Hospital Only (Prescription)",
                "price_range": "₹200-500 per day",
                "side_effects": "Allergic reactions, GI upset, C. diff risk"
            },
            {
                "name": "Morphine",
                "brand_names": ["MS Contin"],
                "type": "Opioid Analgesic",
                "dosage": "2-10 mg IV as needed",
                "purpose": "Severe abdominal pain relief",
                "availability": "Hospital Only (Prescription)",
                "price_range": "₹100-300 per dose",
                "side_effects": "Respiratory depression, constipation, addiction risk"
            },
            {
                "name": "Ondansetron",
                "brand_names": ["Zofran", "Emeset"],
                "type": "Antiemetic",
                "dosage": "4-8 mg IV as needed",
                "purpose": "Nausea and vomiting control",
                "availability": "Hospital/Medical Store (Prescription)",
                "price_range": "₹50-200 per dose",
                "side_effects": "Headache, constipation"
            }
        ]
    },
    
    "Typhoid": {
        "description": "Typhoid fever treatment",
        "drugs": [
            {
                "name": "Azithromycin",
                "brand_names": ["Azithral", "Zithromax", "Azee"],
                "type": "Macrolide Antibiotic",
                "dosage": "500 mg once daily for 7 days",
                "purpose": "First-line typhoid treatment",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹100-300 per course",
                "side_effects": "GI upset, QT prolongation"
            },
            {
                "name": "Ceftriaxone",
                "brand_names": ["Rocephin", "Monocef"],
                "type": "Cephalosporin Antibiotic",
                "dosage": "2-4g IV/IM daily for 7-14 days",
                "purpose": "Severe or resistant typhoid",
                "availability": "Hospital/Medical Store (Prescription)",
                "price_range": "₹200-600 per day",
                "side_effects": "Allergic reactions, diarrhea"
            },
            {
                "name": "Ciprofloxacin",
                "brand_names": ["Cifran", "Ciplox"],
                "type": "Fluoroquinolone Antibiotic",
                "dosage": "500 mg twice daily for 7-10 days",
                "purpose": "Typhoid treatment (if sensitive)",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹80-250 per course",
                "side_effects": "Tendon rupture, GI upset"
            }
        ]
    },
    
    "Sinusitis": {
        "description": "Sinus infection and inflammation treatment",
        "drugs": [
            {
                "name": "Amoxicillin-Clavulanate",
                "brand_names": ["Augmentin", "Clavam", "Moxclav"],
                "type": "Antibiotic",
                "dosage": "875/125 mg twice daily for 10 days",
                "purpose": "Bacterial sinusitis treatment",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹150-400 per course",
                "side_effects": "Diarrhea, allergic reactions"
            },
            {
                "name": "Nasal Decongestant Spray (Xylometazoline)",
                "brand_names": ["Otrivin", "Nasivion"],
                "type": "Nasal Spray",
                "dosage": "2-3 sprays per nostril twice daily (max 3 days)",
                "purpose": "Nasal congestion relief",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹80-150 per bottle",
                "side_effects": "Rebound congestion if overused"
            },
            {
                "name": "Fluticasone Nasal Spray",
                "brand_names": ["Flonase", "Flixonase"],
                "type": "Steroid Nasal Spray",
                "dosage": "2 sprays per nostril once daily",
                "purpose": "Inflammation and congestion reduction",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-400 per bottle",
                "side_effects": "Nosebleeds, irritation"
            }
        ]
    },
    
    "Tonsillitis": {
        "description": "Throat and tonsil infection treatment",
        "drugs": [
            {
                "name": "Penicillin V",
                "brand_names": ["Pen-VK", "Penicillin"],
                "type": "Antibiotic",
                "dosage": "250-500 mg four times daily for 10 days",
                "purpose": "Bacterial tonsillitis (strep throat)",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per course",
                "side_effects": "Allergic reactions, GI upset"
            },
            {
                "name": "Amoxicillin",
                "brand_names": ["Amoxil", "Mox", "Amoxy"],
                "type": "Antibiotic",
                "dosage": "500 mg three times daily for 10 days",
                "purpose": "Bacterial tonsillitis",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹80-250 per course",
                "side_effects": "Rash, diarrhea, allergic reactions"
            },
            {
                "name": "Throat Lozenges (Benzocaine)",
                "brand_names": ["Strepsils", "Vicks", "Cepacol"],
                "type": "Topical Anesthetic",
                "dosage": "1 lozenge every 2-3 hours as needed",
                "purpose": "Throat pain relief",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹30-100 per pack",
                "side_effects": "Rare - allergic reactions"
            }
        ]
    },
    
    "Peptic Ulcer": {
        "description": "Stomach and duodenal ulcer treatment",
        "drugs": [
            {
                "name": "Pantoprazole",
                "brand_names": ["Pantop", "Pan", "Protonix"],
                "type": "Proton Pump Inhibitor",
                "dosage": "40 mg once daily for 4-8 weeks",
                "purpose": "Reduce stomach acid, heal ulcers",
                "availability": "Very Common - Medical Store",
                "price_range": "₹30-150 per tablet",
                "side_effects": "Headache, diarrhea, B12 deficiency (long-term)"
            },
            {
                "name": "Sucralfate",
                "brand_names": ["Carafate", "Sucral"],
                "type": "Mucosal Protectant",
                "dosage": "1g four times daily on empty stomach",
                "purpose": "Coat and protect ulcer",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per pack",
                "side_effects": "Constipation"
            },
            {
                "name": "Triple Therapy (PPI + Antibiotics)",
                "brand_names": ["Various combinations"],
                "type": "Combination Therapy",
                "dosage": "PPI + Amoxicillin + Clarithromycin for 14 days",
                "purpose": "H. pylori eradication",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹500-1500 per course",
                "side_effects": "Diarrhea, metallic taste, GI upset"
            }
        ]
    },
    
    "Irritable Bowel Syndrome": {
        "description": "IBS symptom management",
        "drugs": [
            {
                "name": "Dicyclomine",
                "brand_names": ["Bentyl", "Meftal-Spas"],
                "type": "Antispasmodic",
                "dosage": "10-20 mg four times daily",
                "purpose": "Abdominal cramping and spasm relief",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹30-150 per pack",
                "side_effects": "Dry mouth, blurred vision, constipation"
            },
            {
                "name": "Loperamide",
                "brand_names": ["Imodium", "Lopamide"],
                "type": "Antidiarrheal",
                "dosage": "2-4 mg after each loose stool (max 16mg/day)",
                "purpose": "IBS-D (diarrhea predominant)",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹20-80 per pack",
                "side_effects": "Constipation, abdominal pain"
            },
            {
                "name": "Polyethylene Glycol (PEG)",
                "brand_names": ["MiraLAX", "Laxose"],
                "type": "Osmotic Laxative",
                "dosage": "17g once daily",
                "purpose": "IBS-C (constipation predominant)",
                "availability": "Medical Store (OTC)",
                "price_range": "₹100-300 per pack",
                "side_effects": "Bloating, gas, diarrhea"
            }
        ]
    },
    
    "Meningitis": {
        "description": "Emergency meningitis treatment (Hospital only)",
        "drugs": [
            {
                "name": "Ceftriaxone",
                "brand_names": ["Rocephin", "Monocef"],
                "type": "Cephalosporin Antibiotic",
                "dosage": "2g IV every 12 hours",
                "purpose": "Bacterial meningitis treatment",
                "availability": "Hospital Only (Prescription)",
                "price_range": "₹500-1500 per day",
                "side_effects": "Allergic reactions, diarrhea"
            },
            {
                "name": "Vancomycin",
                "brand_names": ["Vancocin"],
                "type": "Glycopeptide Antibiotic",
                "dosage": "15-20 mg/kg IV every 8-12 hours",
                "purpose": "MRSA or resistant bacterial meningitis",
                "availability": "Hospital Only (Prescription)",
                "price_range": "₹1000-3000 per day",
                "side_effects": "Red man syndrome, nephrotoxicity, ototoxicity"
            },
            {
                "name": "Dexamethasone",
                "brand_names": ["Decadron"],
                "type": "Corticosteroid",
                "dosage": "10 mg IV before antibiotics",
                "purpose": "Reduce inflammation and complications",
                "availability": "Hospital Only (Prescription)",
                "price_range": "₹100-300 per dose",
                "side_effects": "Hyperglycemia, immunosuppression"
            }
        ]
    },
    
    "Sepsis": {
        "description": "Critical care sepsis management (ICU only)",
        "drugs": [
            {
                "name": "Broad-spectrum Antibiotics (Piperacillin-Tazobactam)",
                "brand_names": ["Zosyn", "Piptaz"],
                "type": "Antibiotic Combination",
                "dosage": "4.5g IV every 6 hours",
                "purpose": "Empiric sepsis treatment",
                "availability": "Hospital Only (Prescription)",
                "price_range": "₹1000-3000 per day",
                "side_effects": "Allergic reactions, C. diff risk"
            },
            {
                "name": "Norepinephrine",
                "brand_names": ["Levophed"],
                "type": "Vasopressor",
                "dosage": "Continuous IV infusion (titrated)",
                "purpose": "Septic shock - maintain blood pressure",
                "availability": "Hospital Only (ICU)",
                "price_range": "₹500-2000 per vial",
                "side_effects": "Tissue necrosis if extravasates, arrhythmias"
            },
            {
                "name": "IV Fluids (Normal Saline/Lactated Ringer's)",
                "brand_names": ["NS", "LR"],
                "type": "Crystalloid",
                "dosage": "30 mL/kg bolus initially",
                "purpose": "Fluid resuscitation",
                "availability": "Hospital Only",
                "price_range": "₹50-200 per liter",
                "side_effects": "Fluid overload if excessive"
            }
        ]
    },
    
    "Heart Attack": {
        "description": "Emergency cardiac management (Hospital only)",
        "drugs": [
            {
                "name": "Aspirin",
                "brand_names": ["Disprin", "Ecosprin"],
                "type": "Antiplatelet",
                "dosage": "300 mg chewed immediately",
                "purpose": "Reduce clot formation during heart attack",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹5-30 per tablet",
                "side_effects": "GI bleeding, allergic reactions"
            },
            {
                "name": "Nitroglycerin",
                "brand_names": ["Nitrostat", "Angised"],
                "type": "Nitrate",
                "dosage": "0.4 mg sublingual every 5 min (max 3 doses)",
                "purpose": "Chest pain relief, reduce cardiac workload",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per pack",
                "side_effects": "Headache, hypotension, dizziness"
            },
            {
                "name": "Clopidogrel",
                "brand_names": ["Plavix", "Clopivas"],
                "type": "Antiplatelet",
                "dosage": "300-600 mg loading, then 75 mg daily",
                "purpose": "Prevent further clots after heart attack",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-300 per tablet",
                "side_effects": "Bleeding risk, GI upset"
            },
            {
                "name": "Thrombolytics (Streptokinase/tPA)",
                "brand_names": ["Streptase", "Alteplase"],
                "type": "Clot Buster",
                "dosage": "IV infusion (hospital protocol)",
                "purpose": "Dissolve blood clot during acute MI",
                "availability": "Hospital Only (Emergency)",
                "price_range": "₹5000-50000 per dose",
                "side_effects": "Bleeding (including intracranial), allergic reactions"
            }
        ]
    },
    
    "Stroke": {
        "description": "Emergency stroke management (Hospital only)",
        "drugs": [
            {
                "name": "Alteplase (tPA)",
                "brand_names": ["Actilyse"],
                "type": "Thrombolytic",
                "dosage": "0.9 mg/kg IV within 4.5 hours of onset",
                "purpose": "Ischemic stroke - dissolve clot",
                "availability": "Hospital Only (Emergency)",
                "price_range": "₹50000-150000 per dose",
                "side_effects": "Intracranial hemorrhage, bleeding"
            },
            {
                "name": "Aspirin",
                "brand_names": ["Disprin", "Ecosprin"],
                "type": "Antiplatelet",
                "dosage": "325 mg once (after imaging rules out bleed)",
                "purpose": "Prevent further clots",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹5-30 per tablet",
                "side_effects": "Bleeding risk"
            },
            {
                "name": "Atorvastatin",
                "brand_names": ["Lipitor", "Atorva"],
                "type": "Statin",
                "dosage": "80 mg daily",
                "purpose": "Stabilize plaques, prevent recurrent stroke",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per tablet",
                "side_effects": "Muscle pain, liver issues"
            }
        ]
    },
    
    "Angina": {
        "description": "Chest pain and cardiac ischemia management",
        "drugs": [
            {
                "name": "Nitroglycerin (Sublingual)",
                "brand_names": ["Nitrostat", "Angised"],
                "type": "Nitrate",
                "dosage": "0.4 mg under tongue as needed",
                "purpose": "Rapid angina relief",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per pack",
                "side_effects": "Headache, hypotension, dizziness"
            },
            {
                "name": "Isosorbide Mononitrate",
                "brand_names": ["Imdur", "Ismo"],
                "type": "Long-acting Nitrate",
                "dosage": "30-60 mg once daily",
                "purpose": "Angina prevention",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹80-300 per tablet",
                "side_effects": "Headache, tolerance development"
            },
            {
                "name": "Metoprolol",
                "brand_names": ["Lopressor", "Betaloc"],
                "type": "Beta Blocker",
                "dosage": "50-200 mg twice daily",
                "purpose": "Reduce cardiac workload, prevent angina",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹30-150 per tablet",
                "side_effects": "Fatigue, bradycardia, cold extremities"
            },
            {
                "name": "Ranolazine",
                "brand_names": ["Ranexa"],
                "type": "Metabolic Modulator",
                "dosage": "500-1000 mg twice daily",
                "purpose": "Chronic angina when other drugs insufficient",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-600 per tablet",
                "side_effects": "Dizziness, constipation, QT prolongation"
            }
        ]
    },
    
    "Osteoporosis": {
        "description": "Bone density and fracture prevention",
        "drugs": [
            {
                "name": "Alendronate",
                "brand_names": ["Fosamax", "Alenost"],
                "type": "Bisphosphonate",
                "dosage": "70 mg once weekly on empty stomach",
                "purpose": "Increase bone density, prevent fractures",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-600 per tablet",
                "side_effects": "GI irritation, jaw osteonecrosis (rare), atypical fractures"
            },
            {
                "name": "Calcium + Vitamin D3",
                "brand_names": ["Shelcal-500", "Calcimax"],
                "type": "Supplement",
                "dosage": "500-1000 mg Ca + 400-800 IU D3 daily",
                "purpose": "Bone health support",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹30-150 per tablet",
                "side_effects": "Constipation, kidney stones"
            },
            {
                "name": "Denosumab",
                "brand_names": ["Prolia", "Xgeva"],
                "type": "Monoclonal Antibody Injection",
                "dosage": "60 mg subcutaneous every 6 months",
                "purpose": "Severe osteoporosis, high fracture risk",
                "availability": "Hospital/Medical Store (Prescription)",
                "price_range": "₹15000-30000 per injection",
                "side_effects": "Infection risk, jaw osteonecrosis, hypocalcemia"
            }
        ]
    },
    
    "Gallstones": {
        "description": "Cholelithiasis management",
        "drugs": [
            {
                "name": "Ursodeoxycholic Acid",
                "brand_names": ["Ursodiol", "Actigall", "Udiliv"],
                "type": "Bile Acid",
                "dosage": "10-15 mg/kg/day in divided doses",
                "purpose": "Dissolve small cholesterol stones (limited efficacy)",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-600 per month",
                "side_effects": "Diarrhea, hepatotoxicity"
            },
            {
                "name": "Dicyclomine",
                "brand_names": ["Bentyl", "Meftal-Spas"],
                "type": "Antispasmodic",
                "dosage": "10-20 mg as needed",
                "purpose": "Biliary colic pain relief",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹30-150 per pack",
                "side_effects": "Dry mouth, blurred vision"
            },
            {
                "name": "Ketorolac (for acute pain)",
                "brand_names": ["Toradol"],
                "type": "NSAID",
                "dosage": "10-30 mg IV/IM as needed",
                "purpose": "Severe biliary colic pain",
                "availability": "Hospital/Medical Store (Prescription)",
                "price_range": "₹50-200 per dose",
                "side_effects": "GI bleeding, kidney issues"
            }
        ]
    },
    
    "Fibromyalgia": {
        "description": "Chronic pain and fatigue management",
        "drugs": [
            {
                "name": "Pregabalin",
                "brand_names": ["Lyrica", "Pregalin"],
                "type": "Anticonvulsant (Neuropathic Pain)",
                "dosage": "150-450 mg daily in divided doses",
                "purpose": "Fibromyalgia pain relief",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-800 per month",
                "side_effects": "Dizziness, weight gain, drowsiness, edema"
            },
            {
                "name": "Duloxetine",
                "brand_names": ["Cymbalta", "Duzela"],
                "type": "SNRI Antidepressant",
                "dosage": "60 mg once daily",
                "purpose": "Pain and mood improvement in fibromyalgia",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹150-500 per month",
                "side_effects": "Nausea, dry mouth, insomnia"
            },
            {
                "name": "Amitriptyline",
                "brand_names": ["Elavil", "Tryptomer"],
                "type": "Tricyclic Antidepressant",
                "dosage": "10-50 mg at bedtime",
                "purpose": "Pain relief, improve sleep",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹20-100 per month",
                "side_effects": "Drowsiness, dry mouth, weight gain, constipation"
            }
        ]
    },
    
    "Chronic Fatigue Syndrome": {
        "description": "Symptom management for CFS/ME",
        "drugs": [
            {
                "name": "Modafinil",
                "brand_names": ["Provigil", "Modvigil"],
                "type": "Wakefulness Promoter",
                "dosage": "100-200 mg once daily in morning",
                "purpose": "Reduce excessive daytime sleepiness",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹500-1500 per month",
                "side_effects": "Headache, nausea, anxiety, insomnia"
            },
            {
                "name": "Methylphenidate",
                "brand_names": ["Ritalin", "Concerta"],
                "type": "Stimulant",
                "dosage": "5-20 mg twice daily",
                "purpose": "Improve energy and concentration",
                "availability": "Medical Store (Prescription - Controlled)",
                "price_range": "₹300-800 per month",
                "side_effects": "Insomnia, loss of appetite, anxiety, tachycardia"
            },
            {
                "name": "Coenzyme Q10",
                "brand_names": ["Ubiquinol", "CoQ10"],
                "type": "Supplement",
                "dosage": "200-400 mg daily",
                "purpose": "Mitochondrial support (limited evidence)",
                "availability": "Medical Store (OTC)",
                "price_range": "₹500-1500 per month",
                "side_effects": "Minimal - GI upset"
            }
        ]
    },
    
    "Celiac Disease": {
        "description": "Gluten intolerance management",
        "drugs": [
            {
                "name": "Vitamin and Mineral Supplements",
                "brand_names": ["Various multivitamins"],
                "type": "Nutritional Support",
                "dosage": "As per deficiency (B12, Iron, Folate, Vitamin D)",
                "purpose": "Correct malabsorption-related deficiencies",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹100-500 per month",
                "side_effects": "Minimal if taken as directed"
            },
            {
                "name": "Prednisolone (for refractory cases)",
                "brand_names": ["Omnacortil", "Wysolone"],
                "type": "Corticosteroid",
                "dosage": "20-40 mg daily (short course)",
                "purpose": "Severe inflammation in refractory celiac disease",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "Immunosuppression, weight gain, mood changes"
            }
        ]
    },
    
    "Chickenpox": {
        "description": "Varicella zoster virus infection management",
        "drugs": [
            {
                "name": "Acyclovir",
                "brand_names": ["Zovirax", "Acivir"],
                "type": "Antiviral",
                "dosage": "800 mg five times daily for 7 days",
                "purpose": "Reduce severity and duration of chickenpox",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹200-600 per course",
                "side_effects": "Nausea, headache, kidney issues with dehydration"
            },
            {
                "name": "Calamine Lotion",
                "brand_names": ["Caladryl", "Calamine"],
                "type": "Topical Anti-itch",
                "dosage": "Apply to lesions 3-4 times daily",
                "purpose": "Reduce itching and discomfort",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹30-100 per bottle",
                "side_effects": "Rare - skin irritation"
            },
            {
                "name": "Cetirizine",
                "brand_names": ["Zyrtec", "Okacet"],
                "type": "Antihistamine",
                "dosage": "10 mg once daily",
                "purpose": "Reduce itching",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "Drowsiness"
            }
        ]
    },
    
    "Measles": {
        "description": "Measles symptom management (no specific antiviral)",
        "drugs": [
            {
                "name": "Paracetamol",
                "brand_names": ["Crocin", "Panadol"],
                "type": "Antipyretic/Analgesic",
                "dosage": "500-1000 mg every 4-6 hours",
                "purpose": "Fever and discomfort relief",
                "availability": "Very Common - Medical Store (OTC)",
                "price_range": "₹10-50 per tablet",
                "side_effects": "Liver toxicity in overdose"
            },
            {
                "name": "Vitamin A",
                "brand_names": ["Aquasol A"],
                "type": "Vitamin Supplement",
                "dosage": "200,000 IU daily for 2 days",
                "purpose": "Reduce severity and complications",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹50-200 per course",
                "side_effects": "Rare at therapeutic dose"
            },
            {
                "name": "Antibiotics (if secondary infection)",
                "brand_names": ["Various - Amoxicillin, Azithromycin"],
                "type": "Antibiotic",
                "dosage": "As prescribed for specific infection",
                "purpose": "Treat bacterial complications (pneumonia, ear infection)",
                "availability": "Medical Store (Prescription)",
                "price_range": "₹100-500 per course",
                "side_effects": "Varies by antibiotic"
            }
        ]
    },
    
    "Anaphylaxis": {
        "description": "Severe allergic reaction emergency treatment",
        "drugs": [
            {
                "name": "Epinephrine Auto-injector",
                "brand_names": ["EpiPen", "Anapen", "Adrenaclick"],
                "type": "Emergency IM Injection",
                "dosage": "0.3 mg IM (outer thigh) - repeat in 5-15 min if needed",
                "purpose": "Life-saving treatment for anaphylaxis",
                "availability": "Hospital/Medical Store (Prescription)",
                "price_range": "₹2000-5000 per injector",
                "side_effects": "Tachycardia, anxiety, tremor, hypertension"
            },
            {
                "name": "Diphenhydramine",
                "brand_names": ["Benadryl"],
                "type": "Antihistamine",
                "dosage": "25-50 mg IM/IV",
                "purpose": "Adjunct treatment after epinephrine",
                "availability": "Hospital/Medical Store",
                "price_range": "₹30-100 per dose",
                "side_effects": "Drowsiness"
            },
            {
                "name": "Methylprednisolone",
                "brand_names": ["Solu-Medrol"],
                "type": "Corticosteroid",
                "dosage": "125 mg IV",
                "purpose": "Prevent biphasic reaction",
                "availability": "Hospital Only",
                "price_range": "₹200-600 per dose",
                "side_effects": "Hyperglycemia, immunosuppression"
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
        "Muscle Strain": "Arthritis",
        "Muscle Pain": "Arthritis",
        "Back Pain": "Arthritis",
        "Neck Pain": "Arthritis",
        "Cervical Spondylosis": "Arthritis",
        "Lumbar Spondylosis": "Arthritis",
        "Sprain": "Arthritis",
        "Sports Injury": "Arthritis",
        "Muscle Spasm": "Arthritis",
        # New mappings for expanded disease coverage
        "High Blood Pressure": "Hypertension",
        "HTN": "Hypertension",
        "Elevated Blood Pressure": "Hypertension",
        "UTI": "Urinary Tract Infection",
        "Bladder Infection": "Urinary Tract Infection",
        "Cystitis": "Urinary Tract Infection",
        "Kidney Stone": "Kidney Stones",
        "Renal Calculi": "Kidney Stones",
        "Nephrolithiasis": "Kidney Stones",
        "Allergy": "Allergic Reaction",
        "Allergies": "Allergic Reaction",
        "Hay Fever": "Allergic Reaction",
        "Urticaria": "Allergic Reaction",
        "Hives": "Allergic Reaction",
        "Iron Deficiency": "Anemia",
        "Low Blood": "Anemia",
        "Hemolytic Anemia": "Anemia",
        "Pernicious Anemia": "Anemia",
        "Acute Appendicitis": "Appendicitis",
        "Enteric Fever": "Typhoid",
        "Typhoid Fever": "Typhoid",
        "Sinus Infection": "Sinusitis",
        "Rhinosinusitis": "Sinusitis",
        "Throat Infection": "Tonsillitis",
        "Strep Throat": "Tonsillitis",
        "Pharyngitis": "Tonsillitis",
        "Stomach Ulcer": "Peptic Ulcer",
        "Duodenal Ulcer": "Peptic Ulcer",
        "Gastric Ulcer": "Peptic Ulcer",
        "IBS": "Irritable Bowel Syndrome",
        "Spastic Colon": "Irritable Bowel Syndrome",
        "Bacterial Meningitis": "Meningitis",
        "Viral Meningitis": "Meningitis",
        "Septicemia": "Sepsis",
        "Blood Infection": "Sepsis",
        "Systemic Infection": "Sepsis",
        "Myocardial Infarction": "Heart Attack",
        "MI": "Heart Attack",
        "Cardiac Arrest": "Heart Attack",
        "Coronary Thrombosis": "Heart Attack",
        "CVA": "Stroke",
        "Cerebrovascular Accident": "Stroke",
        "Brain Attack": "Stroke",
        "Ischemic Stroke": "Stroke",
        "Hemorrhagic Stroke": "Stroke",
        "Chest Pain": "Angina",
        "Stable Angina": "Angina",
        "Unstable Angina": "Angina",
        "Angina Pectoris": "Angina",
        "Bone Loss": "Osteoporosis",
        "Low Bone Density": "Osteoporosis",
        "Brittle Bones": "Osteoporosis",
        "Cholelithiasis": "Gallstones",
        "Biliary Colic": "Gallstones",
        "Chronic Pain Syndrome": "Fibromyalgia",
        "FM": "Fibromyalgia",
        "CFS": "Chronic Fatigue Syndrome",
        "ME": "Chronic Fatigue Syndrome",
        "Myalgic Encephalomyelitis": "Chronic Fatigue Syndrome",
        "Gluten Intolerance": "Celiac Disease",
        "Gluten Sensitivity": "Celiac Disease",
        "Varicella": "Chickenpox",
        "Chicken Pox": "Chickenpox",
        "Rubeola": "Measles",
        "Anaphylactic Shock": "Anaphylaxis",
        "Severe Allergic Reaction": "Anaphylaxis",
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
        
        # Handle compound disease names (e.g., "Muscle Strain / Cervical Spondylosis")
        if '/' in disease:
            parts = [p.strip() for p in disease.split('/')]
            for part in parts:
                # Try mapping each part
                mapped_part = self.DISEASE_MAPPING.get(part, part)
                part_normalized = self._normalize_disease_name(mapped_part)
                if part_normalized in self.database:
                    return self.database[part_normalized]
                # Try partial match for each part
                for key in self.database.keys():
                    if part_normalized.lower() in key.lower() or key.lower() in part_normalized.lower():
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
