"""
Advanced Dataset Expansion for Priority 2

Generates high-quality synthetic training data using:
1. Medical synonym substitution
2. Symptom intensity variations  
3. Temporal patterns (sudden, gradual, recurring)
4. Contextual modifiers (location, timing, triggers)
5. Negation handling

Target: Expand from 1935 → 4000+ samples (50-100 variations per disease)
"""

import pandas as pd
import random
import re
from collections import defaultdict

# ===================================
# Medical Synonym Dictionaries
# ===================================

SYMPTOM_SYNONYMS = {
    'pain': ['ache', 'discomfort', 'soreness', 'hurting', 'throbbing', 'sharp pain', 'dull ache'],
    'severe': ['extreme', 'intense', 'acute', 'terrible', 'unbearable', 'excruciating', 'very bad'],
    'mild': ['slight', 'minor', 'gentle', 'weak', 'low-grade', 'little bit of'],
    'fever': ['high temperature', 'elevated temperature', 'hot', 'burning up', 'pyrexia'],
    'fatigue': ['tiredness', 'exhaustion', 'weakness', 'feeling weak', 'lack of energy', 'lethargy'],
    'nausea': ['feeling sick', 'queasy', 'upset stomach', 'want to vomit', 'sick feeling'],
    'headache': ['head pain', 'head hurting', 'pain in head', 'cranial pain'],
    'cough': ['coughing', 'hacking', 'throat irritation with cough'],
    'breathing': ['respiration', 'air intake', 'taking breaths'],
    'difficulty': ['trouble', 'hard time', 'struggling with', 'unable to', 'problem with'],
    'swelling': ['inflammation', 'puffiness', 'swollen', 'edema', 'bloating'],
    'rash': ['skin irritation', 'red spots', 'skin eruption', 'hives', 'skin redness'],
    'chest': ['thorax', 'chest area', 'upper body', 'rib cage area'],
    'abdomen': ['stomach', 'belly', 'abdominal area', 'tummy', 'gut'],
    'joint': ['joints', 'articulation', 'knee/elbow', 'bone connections'],
    'muscle': ['muscular', 'tissue', 'muscle tissue'],
    'chronic': ['long-term', 'persistent', 'ongoing', 'continuous', 'lasting'],
    'sudden': ['abrupt', 'acute', 'immediate', 'unexpected', 'out of nowhere'],
    'gradual': ['slowly developing', 'progressive', 'worsening over time', 'getting worse'],
}

INTENSITY_MODIFIERS = {
    'high': ['very high', 'extremely high', 'dangerously high', 'significantly elevated'],
    'low': ['very low', 'extremely low', 'dangerously low', 'significantly reduced'],
    'frequent': ['very frequent', 'constant', 'recurring often', 'multiple times'],
    'occasional': ['sometimes', 'intermittent', 'sporadic', 'once in a while'],
}

TEMPORAL_PATTERNS = [
    'for the past {time}',
    'since {time} ago',
    'lasting {time}',
    'ongoing for {time}',
    'started {time} ago',
    'began {time} back',
]

TIME_UNITS = [
    '2 days', '3 days', '1 week', '2 weeks', '1 month', 
    'few days', 'several days', 'couple weeks'
]

CONTEXTUAL_ADDITIONS = [
    'especially at night',
    'worse in the morning',
    'gets worse after eating',
    'triggered by activity',
    'constant throughout the day',
    'comes and goes',
    'worsening gradually',
    'suddenly appeared',
]

# ===================================
# Augmentation Functions
# ===================================

def replace_with_synonym(text, word, synonyms):
    """Replace a word with a random synonym"""
    if word in text.lower():
        synonym = random.choice(synonyms)
        # Handle word boundaries
        pattern = r'\b' + re.escape(word) + r'\b'
        return re.sub(pattern, synonym, text, flags=re.IGNORECASE, count=1)
    return text

def add_intensity_modifier(text):
    """Add intensity modifiers to symptoms"""
    for base, modifiers in INTENSITY_MODIFIERS.items():
        if base in text.lower():
            modifier = random.choice(modifiers)
            text = text.replace(base, modifier, 1)
            break
    return text

def add_temporal_context(text):
    """Add time-based context"""
    if random.random() < 0.4:  # 40% chance
        pattern = random.choice(TEMPORAL_PATTERNS)
        time = random.choice(TIME_UNITS)
        temporal = pattern.format(time=time)
        text = f"{text} {temporal}"
    return text

def add_contextual_modifier(text):
    """Add contextual information"""
    if random.random() < 0.3:  # 30% chance
        context = random.choice(CONTEXTUAL_ADDITIONS)
        text = f"{text} {context}"
    return text

def rephrase_sentence(text):
    """Rephrase the sentence structure"""
    rephrasing_templates = [
        lambda t: f"I have {t}",
        lambda t: f"I'm experiencing {t}",
        lambda t: f"I've been having {t}",
        lambda t: f"I suffer from {t}",
        lambda t: f"I've noticed {t}",
        lambda t: f"There is {t}",
        lambda t: f"Experiencing {t}",
    ]
    
    if random.random() < 0.3:  # 30% chance to rephrase
        template = random.choice(rephrasing_templates)
        return template(text)
    return text

def augment_symptom_text(text, num_variations=5):
    """Generate multiple variations of a symptom text"""
    variations = [text]  # Include original
    
    for _ in range(num_variations - 1):
        augmented = text
        
        # Apply synonym substitution (1-3 words)
        num_synonyms = random.randint(1, 3)
        for _ in range(num_synonyms):
            word = random.choice(list(SYMPTOM_SYNONYMS.keys()))
            if word in augmented.lower():
                augmented = replace_with_synonym(
                    augmented, 
                    word, 
                    SYMPTOM_SYNONYMS[word]
                )
        
        # Apply transformations with probability
        if random.random() < 0.4:
            augmented = add_intensity_modifier(augmented)
        
        if random.random() < 0.4:
            augmented = add_temporal_context(augmented)
        
        if random.random() < 0.3:
            augmented = add_contextual_modifier(augmented)
        
        if random.random() < 0.3:
            augmented = rephrase_sentence(augmented)
        
        # Ensure variation is different from original
        if augmented != text and augmented not in variations:
            variations.append(augmented)
    
    return variations

# ===================================
# Main Expansion Logic
# ===================================

def load_current_dataset():
    """Load the current augmented dataset"""
    try:
        df = pd.read_csv("data/symptom_disease_augmented.csv")
        print(f"✅ Loaded current dataset: {len(df)} samples")
        return df
    except FileNotFoundError:
        print("❌ Could not find symptom_disease_augmented.csv")
        return None

def expand_dataset(df, target_samples_per_disease=100):
    """Expand dataset with advanced augmentation"""
    
    print(f"\n🚀 Starting dataset expansion...")
    print(f"Current: {len(df)} samples")
    print(f"Target: ~{len(df['disease'].unique()) * target_samples_per_disease} samples")
    
    expanded_data = []
    
    # Group by disease
    disease_groups = df.groupby('disease')
    
    for disease, group in disease_groups:
        current_count = len(group)
        needed = target_samples_per_disease - current_count
        
        print(f"\n📊 {disease}:")
        print(f"   Current: {current_count} samples")
        print(f"   Target: {target_samples_per_disease} samples")
        print(f"   Generating: {needed} new samples")
        
        # Keep all original samples
        for _, row in group.iterrows():
            expanded_data.append({
                'symptom_text': row['symptom_text'],
                'disease': disease
            })
        
        # Generate new samples
        if needed > 0:
            # Calculate variations per original sample (increase to generate more)
            variations_per_sample = max(3, needed // current_count + 2)
            
            generated = 0
            iteration = 0
            # Keep generating until we hit target
            while generated < needed and iteration < 10:  # Max 10 iterations
                for _, row in group.iterrows():
                    if generated >= needed:
                        break
                    
                    # Generate variations with higher count
                    variations = augment_symptom_text(
                        row['symptom_text'], 
                        num_variations=variations_per_sample + iteration
                    )
                    
                    # Skip the first one (original already added)
                    for variation in variations[1:]:
                        if generated >= needed:
                            break
                        
                        expanded_data.append({
                            'symptom_text': variation,
                            'disease': disease
                        })
                        generated += 1
                
                iteration += 1
    
    # Create new dataframe
    expanded_df = pd.DataFrame(expanded_data)
    
    print(f"\n✅ Expansion complete!")
    print(f"Final dataset: {len(expanded_df)} samples")
    print(f"Expansion ratio: {len(expanded_df) / len(df):.2f}x")
    
    return expanded_df

def analyze_expanded_dataset(df):
    """Analyze the expanded dataset"""
    print("\n" + "="*70)
    print("EXPANDED DATASET ANALYSIS")
    print("="*70)
    
    print(f"\n📊 Overall Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"Total diseases: {df['disease'].nunique()}")
    print(f"Average samples per disease: {len(df) / df['disease'].nunique():.1f}")
    
    print(f"\n📈 Distribution:")
    disease_counts = df['disease'].value_counts()
    print(f"Max samples per disease: {disease_counts.max()}")
    print(f"Min samples per disease: {disease_counts.min()}")
    print(f"Std deviation: {disease_counts.std():.2f}")
    
    if disease_counts.std() < 5:
        print("✅ Well-balanced distribution!")
    
    print(f"\n📝 Sample Length Statistics:")
    text_lengths = df['symptom_text'].str.len()
    print(f"Average text length: {text_lengths.mean():.1f} characters")
    print(f"Min length: {text_lengths.min()}")
    print(f"Max length: {text_lengths.max()}")
    
    print(f"\n🔍 Sample Examples (5 random):")
    samples = df.sample(min(5, len(df)))
    for idx, row in samples.iterrows():
        print(f"\n  Disease: {row['disease']}")
        print(f"  Symptoms: {row['symptom_text'][:100]}...")

def save_expanded_dataset(df, filename="data/symptom_disease_expanded_v2.csv"):
    """Save the expanded dataset"""
    df.to_csv(filename, index=False)
    print(f"\n💾 Saved expanded dataset to: {filename}")

# ===================================
# Main Execution
# ===================================

if __name__ == "__main__":
    print("="*70)
    print("PRIORITY 2: ADVANCED DATASET EXPANSION")
    print("="*70)
    
    # Load current dataset
    df = load_current_dataset()
    
    if df is not None:
        # Expand dataset (target: 100 samples per disease = ~4300 total)
        expanded_df = expand_dataset(df, target_samples_per_disease=100)
        
        # Analyze results
        analyze_expanded_dataset(expanded_df)
        
        # Save
        save_expanded_dataset(expanded_df)
        
        print("\n✅ Dataset expansion complete!")
        print("\nNext steps:")
        print("1. Train new model: python scripts/train_model_v2.py")
        print("2. Evaluate improvement: python scripts/compare_models.py")
    else:
        print("\n❌ Could not load dataset. Please check file path.")
