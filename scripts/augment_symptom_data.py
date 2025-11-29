#!/usr/bin/env python3
"""
Data Augmentation Script - Week 2 Improvement
Augments symptom descriptions using template-based paraphrasing and synonym substitution
Target: 3x original dataset size with natural variations
"""

import pandas as pd
import random
import re
from collections import defaultdict

# Seed for reproducibility
random.seed(42)

# Templates for natural language variations
SYMPTOM_TEMPLATES = [
    "{symptoms}",
    "I have {symptoms}",
    "I'm experiencing {symptoms}",
    "I've been having {symptoms}",
    "Suffering from {symptoms}",
    "{symptoms} for the past few days",
    "Recently developed {symptoms}",
    "Feeling {symptoms}",
    "{symptoms} that won't go away",
    "Been dealing with {symptoms}",
    "{symptoms} for a while now",
    "Started experiencing {symptoms}",
    "{symptoms} and it's getting worse",
    "Having issues with {symptoms}",
    "{symptoms} since yesterday",
]

# Synonym dictionary for common medical terms
SYMPTOM_SYNONYMS = {
    'pain': ['ache', 'discomfort', 'soreness', 'hurt', 'painful'],
    'severe': ['intense', 'extreme', 'acute', 'sharp', 'bad'],
    'fever': ['high temperature', 'temperature', 'hot', 'burning up', 'feverish'],
    'tired': ['fatigued', 'exhausted', 'weak', 'drained', 'worn out'],
    'nausea': ['feeling sick', 'queasy', 'sick to stomach', 'sick', 'nauseous'],
    'cough': ['coughing', 'hacking cough', 'persistent cough', 'dry cough'],
    'headache': ['head pain', 'head hurts', 'head ache', 'pain in head'],
    'difficulty': ['trouble', 'hard to', 'problems', 'can\'t', 'unable to'],
    'breathing': ['breath', 'breathing', 'breathe', 'respiration'],
    'stomach': ['belly', 'abdomen', 'tummy', 'gut'],
    'swollen': ['swelling', 'puffy', 'enlarged', 'inflamed'],
    'rash': ['skin rash', 'rash', 'bumps', 'skin irritation', 'red spots'],
    'dizziness': ['dizzy', 'lightheaded', 'vertigo', 'spinning sensation'],
    'vomiting': ['vomit', 'throwing up', 'puking', 'being sick'],
    'diarrhea': ['loose stools', 'watery stools', 'frequent bowel movements'],
    'weakness': ['weak', 'weakness', 'fatigue', 'lack of strength'],
    'chest': ['chest', 'thorax', 'upper body', 'breastbone area'],
    'throat': ['throat', 'neck', 'pharynx'],
    'joint': ['joint', 'joints', 'articulation'],
    'muscle': ['muscle', 'muscles', 'muscular'],
}

# Time expressions for variation
TIME_EXPRESSIONS = [
    'for the past few days',
    'since yesterday',
    'for over a week',
    'recently',
    'for several days',
    'for a while',
    'that started today',
    'that began suddenly',
    'for the last couple of days',
    'since this morning',
]

def substitute_synonyms(text, substitution_rate=0.4):
    """
    Replace words with synonyms while maintaining medical meaning
    
    Args:
        text: Original symptom text
        substitution_rate: Probability of substituting each word (0-1)
    
    Returns:
        Text with some words replaced by synonyms
    """
    words = text.split()
    result = []
    
    for word in words:
        word_lower = word.lower().strip('.,!?')
        
        # Check if word has synonyms
        if word_lower in SYMPTOM_SYNONYMS and random.random() < substitution_rate:
            # Replace with random synonym
            synonym = random.choice(SYMPTOM_SYNONYMS[word_lower])
            # Preserve capitalization
            if word[0].isupper():
                synonym = synonym.capitalize()
            result.append(synonym)
        else:
            result.append(word)
    
    return ' '.join(result)

def apply_template(symptom_text, avoid_duplicate=None):
    """
    Apply random template to symptom text
    
    Args:
        symptom_text: Original symptom description
        avoid_duplicate: Template to avoid (for variation)
    
    Returns:
        Symptom text with template applied
    """
    available_templates = [t for t in SYMPTOM_TEMPLATES if t != avoid_duplicate]
    template = random.choice(available_templates)
    
    # If template has {symptoms} placeholder
    if '{symptoms}' in template:
        return template.format(symptoms=symptom_text)
    else:
        return symptom_text

def add_time_expression(text, probability=0.3):
    """
    Randomly add time expression to symptom description
    """
    if random.random() < probability:
        time_expr = random.choice(TIME_EXPRESSIONS)
        # Add at end if not already present
        if not any(expr in text.lower() for expr in ['for', 'since', 'recently']):
            return f"{text} {time_expr}"
    return text

def augment_symptom(original_text, original_template=None):
    """
    Create augmented version of symptom text using multiple techniques
    
    Args:
        original_text: Original symptom description
        original_template: Template used for original (to avoid)
    
    Returns:
        Augmented symptom text
    """
    # Step 1: Synonym substitution
    text = substitute_synonyms(original_text, substitution_rate=0.4)
    
    # Step 2: Apply different template
    text = apply_template(text, avoid_duplicate=original_template)
    
    # Step 3: Optionally add time expression
    text = add_time_expression(text, probability=0.3)
    
    # Step 4: Clean up formatting
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = text.strip()
    
    return text

def augment_dataset(df, augmentation_factor=3):
    """
    Augment entire dataset by generating variations
    
    Args:
        df: Original DataFrame with 'symptom_text' and 'disease' columns
        augmentation_factor: Total multiplier (3 = original + 2 augmented versions)
    
    Returns:
        Augmented DataFrame
    """
    print(f"🔄 Augmenting dataset with factor {augmentation_factor}x...")
    
    augmented_rows = []
    
    # Track original templates to avoid exact duplicates
    original_templates = {}
    
    for idx, row in df.iterrows():
        original_text = row['symptom_text']
        disease = row['disease']
        
        # Keep original
        augmented_rows.append({
            'symptom_text': original_text,
            'disease': disease,
            'is_augmented': False
        })
        
        # Determine original template (if any)
        original_template = None
        for template in SYMPTOM_TEMPLATES:
            if '{symptoms}' in template:
                pattern = template.replace('{symptoms}', '(.+)')
                if re.match(pattern, original_text, re.IGNORECASE):
                    original_template = template
                    break
        
        # Generate augmented versions
        for aug_num in range(augmentation_factor - 1):
            augmented_text = augment_symptom(original_text, original_template)
            
            # Ensure we didn't create exact duplicate
            attempts = 0
            while augmented_text == original_text and attempts < 5:
                augmented_text = augment_symptom(original_text, original_template)
                attempts += 1
            
            augmented_rows.append({
                'symptom_text': augmented_text,
                'disease': disease,
                'is_augmented': True
            })
        
        if (idx + 1) % 100 == 0:
            print(f"   Processed {idx + 1}/{len(df)} samples...")
    
    augmented_df = pd.DataFrame(augmented_rows)
    
    print(f"✅ Augmentation complete!")
    print(f"   Original samples: {len(df)}")
    print(f"   Augmented samples: {len(augmented_df) - len(df)}")
    print(f"   Total samples: {len(augmented_df)}")
    
    return augmented_df

def show_augmentation_examples(df, num_examples=5):
    """
    Show examples of augmented symptom descriptions
    """
    print(f"\n📖 Augmentation Examples:")
    print("="*70)
    
    # Group by disease to show variations
    diseases = df['disease'].unique()
    sample_disease = random.choice(diseases)
    
    disease_samples = df[df['disease'] == sample_disease]
    original = disease_samples[~disease_samples['is_augmented']].iloc[0]['symptom_text']
    augmented = disease_samples[disease_samples['is_augmented']].head(num_examples)
    
    print(f"\nDisease: {sample_disease}")
    print(f"\n  Original: {original}")
    print(f"\n  Augmented versions:")
    for idx, row in augmented.iterrows():
        print(f"    {idx+1}. {row['symptom_text']}")

def main():
    """
    Main augmentation pipeline
    """
    print("\n" + "="*70)
    print("📊 DATA AUGMENTATION - Week 2 Improvement")
    print("="*70)
    
    # Load expanded dataset
    input_path = 'data/symptom_disease_expanded.csv'
    print(f"\n📂 Loading dataset: {input_path}")
    
    df = pd.read_csv(input_path)
    print(f"✅ Loaded: {len(df)} samples, {df['disease'].nunique()} diseases")
    
    # Augment dataset
    augmented_df = augment_dataset(df, augmentation_factor=3)
    
    # Show examples
    show_augmentation_examples(augmented_df, num_examples=4)
    
    # Save augmented dataset
    output_path = 'data/symptom_disease_augmented.csv'
    
    # Remove is_augmented flag before saving
    final_df = augmented_df[['symptom_text', 'disease']].copy()
    
    # Shuffle
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    final_df.to_csv(output_path, index=False)
    
    print(f"\n💾 Saved augmented dataset to: {output_path}")
    
    # Show final statistics
    print(f"\n📊 Final Dataset Statistics:")
    print(f"   Total samples: {len(final_df)}")
    print(f"   Total diseases: {final_df['disease'].nunique()}")
    print(f"   Avg samples per disease: {len(final_df) / final_df['disease'].nunique():.1f}")
    
    # Show sample distribution
    print(f"\n📋 Sample Distribution (top 10 diseases):")
    disease_counts = final_df['disease'].value_counts()
    for disease, count in disease_counts.head(10).items():
        print(f"   {disease:<35s} {count:3d} samples")
    
    print(f"\n✅ Data augmentation complete!")
    print(f"   Next step: Retrain model with augmented dataset")

if __name__ == '__main__':
    main()
