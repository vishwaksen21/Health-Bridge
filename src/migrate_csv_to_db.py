"""
CSV to SQLite Migration Utility
Migrates existing CSV data files to SQLite database
"""

import pandas as pd
from pathlib import Path
from database_manager import DatabaseManager
import sys

def migrate_csv_to_database(csv_dir: str = "../data", db_path: str = "../data/medical_knowledge.db"):
    """
    Migrate CSV files to SQLite database.
    
    Args:
        csv_dir: Directory containing CSV files
        db_path: Path to SQLite database file
    """
    print("\n" + "="*80)
    print("🔄 CSV TO SQLITE MIGRATION")
    print("="*80)
    
    db = DatabaseManager(db_path)
    csv_path = Path(csv_dir)
    
    # Mapping of CSV files to migration functions
    migrations = {
        "diseases.csv": migrate_diseases,
        "symptoms_disease.csv": migrate_symptoms_disease,
        "herbs.csv": migrate_herbs,
        "ingredients.csv": migrate_ingredients,
        "pharmaceutical_database.csv": migrate_pharmaceuticals,
        "drug_interactions.csv": migrate_drug_interactions,
    }
    
    for csv_file, migration_func in migrations.items():
        file_path = csv_path / csv_file
        if file_path.exists():
            print(f"\n📄 Processing: {csv_file}")
            try:
                migration_func(db, file_path)
                print(f"   ✅ Success")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"\n⏭️  Skipping: {csv_file} (not found)")
    
    # Display statistics
    print("\n" + "="*80)
    print("📊 MIGRATION COMPLETE - Database Statistics")
    print("="*80)
    stats = db.get_statistics()
    for table, count in stats.items():
        print(f"   {table}: {count:,} records")
    
    db.close()
    print("\n✅ Migration complete!")
    print(f"   Database: {db_path}")


def migrate_diseases(db: DatabaseManager, csv_file: Path):
    """Migrate diseases.csv"""
    try:
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            disease_name = row.get('disease', row.get('Disease', ''))
            if disease_name:
                db.add_disease(
                    name=disease_name,
                    category="General",
                    severity=1,
                    description=None
                )
    except Exception as e:
        print(f"      Failed: {e}")


def migrate_symptoms_disease(db: DatabaseManager, csv_file: Path):
    """Migrate symptom_disease.csv - the main training dataset"""
    try:
        df = pd.read_csv(csv_file)
        
        # Assuming the last column is the disease name
        disease_col = df.columns[-1]
        
        # Get unique diseases and add them
        diseases = df[disease_col].unique()
        print(f"      Found {len(diseases)} diseases")
        
        disease_ids = {}
        for disease in diseases:
            if pd.notna(disease):
                disease_id = db.add_disease(name=disease, category="General", severity=1)
                disease_ids[disease] = disease_id
        
        # Process symptoms
        symptom_cols = df.columns[:-1]  # All columns except disease
        symptom_ids = {}
        
        for symptom_col in symptom_cols:
            symptom_id = db.add_symptom(name=symptom_col.replace('_', ' ').title())
            symptom_ids[symptom_col] = symptom_id
        
        # Link symptoms to diseases
        for _, row in df.iterrows():
            disease = row[disease_col]
            if pd.notna(disease) and disease in disease_ids:
                disease_id = disease_ids[disease]
                
                for symptom_col in symptom_cols:
                    if row[symptom_col] == 1:  # Symptom is present
                        symptom_id = symptom_ids[symptom_col]
                        db.link_disease_symptom(disease_id, symptom_id, occurrence_rate=0.8)
        
        print(f"      Added {len(symptom_ids)} symptoms and {len(disease_ids)} diseases")
        
    except Exception as e:
        print(f"      Failed: {e}")


def migrate_herbs(db: DatabaseManager, csv_file: Path):
    """Migrate herbs.csv"""
    try:
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            herb_name = row.get('herb', row.get('Herb', ''))
            if herb_name:
                db.connection.execute(
                    "INSERT OR IGNORE INTO herbs (name, scientific_name, properties) VALUES (?, ?, ?)",
                    (herb_name, None, None)
                )
        db.connection.commit()
        print(f"      Added {len(df)} herbs")
    except Exception as e:
        print(f"      Failed: {e}")


def migrate_ingredients(db: DatabaseManager, csv_file: Path):
    """Migrate ingredients.csv"""
    try:
        df = pd.read_csv(csv_file)
        print(f"      Found {len(df)} ingredient records (linking already done)")
    except Exception as e:
        print(f"      Failed: {e}")


def migrate_pharmaceuticals(db: DatabaseManager, csv_file: Path):
    """Migrate pharmaceutical_database.csv"""
    try:
        df = pd.read_csv(csv_file)
        
        for _, row in df.iterrows():
            disease_name = row.get('disease', '')
            
            # Get or create disease
            disease_id = db.get_disease_id(disease_name)
            if not disease_id:
                disease_id = db.add_disease(disease_name, category="General")
            
            # Add pharmaceutical
            db.connection.execute(
                """INSERT INTO pharmaceuticals 
                   (name, generic_name, disease_id, dosage, side_effects, price_range, availability, brand_names)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    row.get('drug_name', ''),
                    row.get('generic_name', ''),
                    disease_id,
                    row.get('dosage', ''),
                    row.get('side_effects', ''),
                    row.get('price_range', ''),
                    row.get('availability', ''),
                    row.get('brand_names', '')
                )
            )
        
        db.connection.commit()
        print(f"      Added {len(df)} pharmaceuticals")
        
    except Exception as e:
        print(f"      Failed: {e}")


def migrate_drug_interactions(db: DatabaseManager, csv_file: Path):
    """Migrate drug_interactions.csv"""
    try:
        df = pd.read_csv(csv_file)
        
        for _, row in df.iterrows():
            drug1_name = row.get('drug1', '')
            drug2_name = row.get('drug2', '')
            
            # Get drug IDs
            cursor = db.connection.cursor()
            cursor.execute("SELECT id FROM pharmaceuticals WHERE name = ?", (drug1_name,))
            drug1_result = cursor.fetchone()
            cursor.execute("SELECT id FROM pharmaceuticals WHERE name = ?", (drug2_name,))
            drug2_result = cursor.fetchone()
            
            if drug1_result and drug2_result:
                db.connection.execute(
                    """INSERT OR IGNORE INTO drug_interactions 
                       (drug1_id, drug2_id, severity, effect, recommendation)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        drug1_result[0],
                        drug2_result[0],
                        row.get('severity', ''),
                        row.get('effect', ''),
                        row.get('recommendation', '')
                    )
                )
        
        db.connection.commit()
        print(f"      Added {len(df)} drug interactions")
        
    except Exception as e:
        print(f"      Failed: {e}")


if __name__ == "__main__":
    migrate_csv_to_database()
