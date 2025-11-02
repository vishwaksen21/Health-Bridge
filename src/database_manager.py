"""
Database Manager for Medical Knowledge System
Provides centralized access to medical data with caching and optimization
"""

import sqlite3
import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

class DatabaseManager:
    """
    Manages medical knowledge database with SQLite backend.
    Handles diseases, symptoms, herbs, pharmaceuticals, and their relationships.
    """
    
    def __init__(self, db_path: str = "data/medical_knowledge.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self._cache = {}
        self._init_database()
    
    def _init_database(self):
        """Initialize database with schema if it doesn't exist."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
        # Enable foreign keys
        self.connection.execute("PRAGMA foreign_keys = ON")
        
        # Create tables if they don't exist
        self._create_schema()
    
    def _create_schema(self):
        """Create database schema."""
        cursor = self.connection.cursor()
        
        # Diseases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) UNIQUE NOT NULL,
                category VARCHAR(50),
                severity INTEGER DEFAULT 1,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Symptoms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) UNIQUE NOT NULL,
                description TEXT,
                severity INTEGER DEFAULT 1,
                duration_days INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Disease-Symptom relationships
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disease_symptoms (
                disease_id INTEGER NOT NULL,
                symptom_id INTEGER NOT NULL,
                occurrence_rate FLOAT DEFAULT 0.5,
                PRIMARY KEY (disease_id, symptom_id),
                FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE,
                FOREIGN KEY (symptom_id) REFERENCES symptoms(id) ON DELETE CASCADE
            )
        """)
        
        # Herbs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS herbs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) UNIQUE NOT NULL,
                scientific_name VARCHAR(150),
                properties TEXT,
                effectiveness_rating FLOAT DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Herb-Disease relationships
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS herb_diseases (
                herb_id INTEGER NOT NULL,
                disease_id INTEGER NOT NULL,
                effectiveness FLOAT DEFAULT 0.5,
                usage_method TEXT,
                PRIMARY KEY (herb_id, disease_id),
                FOREIGN KEY (herb_id) REFERENCES herbs(id) ON DELETE CASCADE,
                FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
            )
        """)
        
        # Pharmaceuticals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pharmaceuticals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                generic_name VARCHAR(100),
                disease_id INTEGER,
                dosage VARCHAR(50),
                side_effects TEXT,
                price_range VARCHAR(20),
                availability VARCHAR(50),
                brand_names TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE SET NULL
            )
        """)
        
        # Drug Interactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drug_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drug1_id INTEGER NOT NULL,
                drug2_id INTEGER NOT NULL,
                severity VARCHAR(20),
                effect TEXT,
                recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (drug1_id) REFERENCES pharmaceuticals(id) ON DELETE CASCADE,
                FOREIGN KEY (drug2_id) REFERENCES pharmaceuticals(id) ON DELETE CASCADE,
                UNIQUE(drug1_id, drug2_id)
            )
        """)
        
        # Symptom Patterns table (for enhanced predictions)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptom_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name VARCHAR(100) UNIQUE NOT NULL,
                keywords TEXT,
                likely_diseases TEXT,
                severity VARCHAR(20),
                clarification TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_disease_name ON diseases(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_symptom_name ON symptoms(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_herb_name ON herbs(name)")
        
        self.connection.commit()
    
    def add_disease(self, name: str, category: str = None, severity: int = 1, 
                   description: str = None) -> int:
        """Add a disease to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO diseases (name, category, severity, description)
                VALUES (?, ?, ?, ?)
            """, (name, category, severity, description))
            self.connection.commit()
            self._cache.clear()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return self.get_disease_id(name)
    
    def add_symptom(self, name: str, description: str = None, severity: int = 1,
                   duration_days: int = None) -> int:
        """Add a symptom to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO symptoms (name, description, severity, duration_days)
                VALUES (?, ?, ?, ?)
            """, (name, description, severity, duration_days))
            self.connection.commit()
            self._cache.clear()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return self.get_symptom_id(name)
    
    def link_disease_symptom(self, disease_id: int, symptom_id: int, 
                            occurrence_rate: float = 0.5):
        """Link a disease to a symptom."""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO disease_symptoms 
            (disease_id, symptom_id, occurrence_rate)
            VALUES (?, ?, ?)
        """, (disease_id, symptom_id, occurrence_rate))
        self.connection.commit()
        self._cache.clear()
    
    def get_disease_id(self, name: str) -> Optional[int]:
        """Get disease ID by name."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM diseases WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_symptom_id(self, name: str) -> Optional[int]:
        """Get symptom ID by name."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM symptoms WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_diseases_by_symptoms(self, symptoms: List[str]) -> List[Dict]:
        """
        Get diseases matching given symptoms.
        
        Args:
            symptoms: List of symptom names
            
        Returns:
            List of diseases with matching symptoms
        """
        cache_key = f"diseases_by_symptoms_{','.join(sorted(symptoms))}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        cursor = self.connection.cursor()
        
        # Get symptom IDs
        placeholders = ','.join('?' * len(symptoms))
        cursor.execute(f"""
            SELECT DISTINCT d.id, d.name, d.category, COUNT(ds.symptom_id) as match_count
            FROM diseases d
            JOIN disease_symptoms ds ON d.id = ds.disease_id
            JOIN symptoms s ON ds.symptom_id = s.id
            WHERE s.name IN ({placeholders})
            GROUP BY d.id, d.name, d.category
            ORDER BY match_count DESC
        """, symptoms)
        
        results = [dict(row) for row in cursor.fetchall()]
        self._cache[cache_key] = results
        return results
    
    def get_herbs_for_disease(self, disease_name: str) -> List[Dict]:
        """Get recommended herbs for a disease."""
        cache_key = f"herbs_for_{disease_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT h.name, h.scientific_name, h.properties, hd.effectiveness
            FROM herbs h
            JOIN herb_diseases hd ON h.id = hd.herb_id
            JOIN diseases d ON hd.disease_id = d.id
            WHERE d.name = ?
            ORDER BY hd.effectiveness DESC
        """, (disease_name,))
        
        results = [dict(row) for row in cursor.fetchall()]
        self._cache[cache_key] = results
        return results
    
    def get_drugs_for_disease(self, disease_name: str) -> List[Dict]:
        """Get recommended drugs for a disease."""
        cache_key = f"drugs_for_{disease_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT name, generic_name, dosage, side_effects, price_range, 
                   availability, brand_names
            FROM pharmaceuticals
            WHERE disease_id = (SELECT id FROM diseases WHERE name = ?)
            LIMIT 10
        """, (disease_name,))
        
        results = [dict(row) for row in cursor.fetchall()]
        self._cache[cache_key] = results
        return results
    
    def check_drug_interaction(self, drug1: str, drug2: str) -> Optional[Dict]:
        """Check if two drugs have known interactions."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT severity, effect, recommendation
            FROM drug_interactions
            WHERE (drug1_id = (SELECT id FROM pharmaceuticals WHERE name = ?)
                   AND drug2_id = (SELECT id FROM pharmaceuticals WHERE name = ?))
            OR (drug1_id = (SELECT id FROM pharmaceuticals WHERE name = ?)
                AND drug2_id = (SELECT id FROM pharmaceuticals WHERE name = ?))
        """, (drug1, drug2, drug2, drug1))
        
        result = cursor.fetchone()
        return dict(result) if result else None
    
    def get_symptom_pattern(self, pattern_name: str) -> Optional[Dict]:
        """Get symptom pattern information."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT pattern_name, keywords, likely_diseases, severity, clarification
            FROM symptom_patterns
            WHERE pattern_name = ?
        """, (pattern_name,))
        
        result = cursor.fetchone()
        if result:
            data = dict(result)
            # Parse JSON fields
            data['keywords'] = json.loads(data['keywords']) if data['keywords'] else []
            data['likely_diseases'] = json.loads(data['likely_diseases']) if data['likely_diseases'] else []
            return data
        return None
    
    def add_symptom_pattern(self, pattern_name: str, keywords: List[str],
                           likely_diseases: List[str], severity: str,
                           clarification: str = None):
        """Add or update symptom pattern."""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO symptom_patterns 
            (pattern_name, keywords, likely_diseases, severity, clarification)
            VALUES (?, ?, ?, ?, ?)
        """, (pattern_name, json.dumps(keywords), json.dumps(likely_diseases), 
              severity, clarification))
        self.connection.commit()
        self._cache.clear()
    
    def import_from_csv(self, csv_path: str, table_name: str):
        """Import data from CSV file."""
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, self.connection, if_exists='append', index=False)
        self.connection.commit()
        self._cache.clear()
    
    def export_to_csv(self, table_name: str, output_path: str):
        """Export table to CSV."""
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.connection)
        df.to_csv(output_path, index=False)
    
    def get_statistics(self) -> Dict:
        """Get database statistics."""
        cursor = self.connection.cursor()
        stats = {}
        
        for table in ['diseases', 'symptoms', 'herbs', 'pharmaceuticals']:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]
        
        return stats
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience functions for standalone usage
def init_database(db_path: str = "data/medical_knowledge.db") -> DatabaseManager:
    """Initialize and return database manager."""
    return DatabaseManager(db_path)


if __name__ == "__main__":
    # Test the database manager
    print("\n" + "="*70)
    print("🗄️ DATABASE MANAGER - INITIALIZATION TEST")
    print("="*70)
    
    with DatabaseManager() as db:
        # Add some test data
        print("\n✅ Creating database schema...")
        
        # Add diseases
        typhoid_id = db.add_disease("Typhoid", "Infection", 3, "Bacterial infection from contaminated water")
        malaria_id = db.add_disease("Malaria", "Parasitic", 3, "Mosquito-borne parasitic disease")
        dengue_id = db.add_disease("Dengue", "Viral", 2, "Mosquito-borne viral disease")
        
        # Add symptoms
        fever_id = db.add_symptom("Fever", "High body temperature", 2)
        chills_id = db.add_symptom("Chills", "Shivering sensation", 1)
        body_ache_id = db.add_symptom("Body Ache", "General muscle pain", 1)
        
        # Link diseases to symptoms
        db.link_disease_symptom(typhoid_id, fever_id, 0.9)
        db.link_disease_symptom(typhoid_id, body_ache_id, 0.8)
        db.link_disease_symptom(malaria_id, fever_id, 0.95)
        db.link_disease_symptom(malaria_id, chills_id, 0.9)
        
        # Get statistics
        stats = db.get_statistics()
        print("\n📊 Database Statistics:")
        for table, count in stats.items():
            print(f"   {table}: {count} records")
        
        # Test query
        print("\n🔍 Testing disease lookup by symptoms:")
        results = db.get_diseases_by_symptoms(["Fever", "Chills"])
        for result in results:
            print(f"   - {result['name']} ({result['match_count']} matching symptoms)")
    
    print("\n✅ Database initialized successfully at: data/medical_knowledge.db")
    print("="*70 + "\n")
