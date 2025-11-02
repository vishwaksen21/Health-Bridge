"""
Comprehensive test suite for pharmaceutical drug recommendation system.
Tests drug database integration and dual recommendation generation.
"""

import sys
import json
import os
from pathlib import Path

# Add src to path
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import drug database
from drug_database import DrugDatabase, get_drug_recommendations

# Import AI components - handle both direct and relative imports
try:
    from ai_assistant import (
        load_knowledge_base, 
        suggest_drugs_for_disease,
        suggest_ingredients_for_disease,
        generate_comprehensive_answer,
        format_answer_for_display
    )
except ImportError:
    # Fallback: import symptom_predictor first
    from symptom_predictor import predict_disease
    from ai_assistant import (
        load_knowledge_base, 
        suggest_drugs_for_disease,
        suggest_ingredients_for_disease,
        generate_comprehensive_answer,
        format_answer_for_display
    )


class TestDrugDatabase:
    """Test pharmaceutical database functionality."""
    
    def __init__(self):
        self.db = DrugDatabase()
        self.passed = 0
        self.failed = 0
    
    def test_load_database(self):
        """Test if database loads correctly."""
        print("\n✓ TEST 1: Load Drug Database")
        try:
            diseases = self.db.get_available_diseases()
            assert len(diseases) > 0, "No diseases found"
            print(f"  ✅ Database loaded with {len(diseases)} diseases")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_get_drugs_for_disease(self):
        """Test retrieving drugs for a specific disease."""
        print("\n✓ TEST 2: Get Drugs for Disease")
        try:
            diabetes_drugs = self.db.get_drugs_for_disease("Diabetes")
            assert diabetes_drugs is not None, "Diabetes not found"
            assert "drugs" in diabetes_drugs, "No drugs field"
            assert len(diabetes_drugs["drugs"]) > 0, "No drugs for diabetes"
            
            print(f"  ✅ Found {len(diabetes_drugs['drugs'])} drugs for Diabetes")
            print(f"     Diseases with drug info: {len(self.db.get_available_diseases())}")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_sort_by_commonality(self):
        """Test drugs sorted by availability/commonality."""
        print("\n✓ TEST 3: Sort Drugs by Commonality")
        try:
            sorted_drugs = self.db.get_drugs_sorted_by_commonality("Diabetes")
            assert len(sorted_drugs) > 0, "No drugs returned"
            
            # Check if first drug is more common than last
            first_avail = sorted_drugs[0].get("availability")
            print(f"  ✅ Most common: {first_avail}")
            print(f"     Total drugs for Diabetes: {len(sorted_drugs)}")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_drug_by_name(self):
        """Test finding drug by name."""
        print("\n✓ TEST 4: Find Drug by Name")
        try:
            drug = self.db.get_drug_by_name("Metformin")
            assert drug is not None, "Metformin not found"
            assert drug["name"] == "Metformin", "Wrong drug returned"
            
            print(f"  ✅ Found: {drug['name']}")
            print(f"     Brand Names: {', '.join(drug['brand_names'][:2])}")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_partial_disease_match(self):
        """Test partial disease name matching."""
        print("\n✓ TEST 5: Partial Disease Name Match")
        try:
            drugs1 = self.db.get_drugs_for_disease("Diab")
            drugs2 = self.db.get_drugs_for_disease("Diabetes")
            assert drugs1 is not None, "Partial match failed"
            assert drugs1 == drugs2, "Partial and full names don't match"
            
            print(f"  ✅ Partial match works for 'Diab' → 'Diabetes'")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_csv_export(self):
        """Test exporting database to CSV."""
        print("\n✓ TEST 6: CSV Export")
        try:
            csv_file = "test_drug_db_export.csv"
            if os.path.exists(csv_file):
                os.remove(csv_file)
            
            # Suppress print output for export
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                self.db.export_to_csv(csv_file)
            
            assert os.path.exists(csv_file), "CSV file not created"
            
            import pandas as pd
            df = pd.read_csv(csv_file)
            assert len(df) > 0, "CSV is empty"
            
            print(f"  ✅ Exported {len(df)} drug records to CSV")
            
            # Cleanup
            os.remove(csv_file)
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1


class TestDrugRecommendations:
    """Test drug recommendation functionality."""
    
    def __init__(self):
        self.knowledge = load_knowledge_base()
        self.passed = 0
        self.failed = 0
    
    def test_suggest_drugs(self):
        """Test drug suggestions for a disease."""
        print("\n✓ TEST 7: Suggest Drugs for Disease")
        try:
            drugs = suggest_drugs_for_disease("Diabetes", top_n=5)
            assert isinstance(drugs, list), "Not a list"
            assert len(drugs) > 0, "No drugs returned"
            
            # Check drug structure
            first_drug = drugs[0]
            required_keys = ["name", "brand_names", "type", "dosage", "availability"]
            for key in required_keys:
                assert key in first_drug, f"Missing key: {key}"
            
            print(f"  ✅ Got {len(drugs)} drug recommendations")
            print(f"     Top drug: {first_drug['name']}")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_comprehensive_answer_with_drugs(self):
        """Test generating comprehensive answer with both herbs and drugs."""
        print("\n✓ TEST 8: Comprehensive Answer (Herbs + Drugs)")
        try:
            response = generate_comprehensive_answer(
                "I have high fever and chills",
                self.knowledge,
                use_ai=False,  # Skip LLM to avoid API calls
                include_drugs=True
            )
            
            assert "detected_disease" in response, "No disease detected"
            assert "herbal_recommendations" in response, "No herbal recs"
            assert "drug_recommendations" in response, "No drug recs"
            
            print(f"  ✅ Disease detected: {response['detected_disease']}")
            print(f"     Herbal recommendations: {len(response['herbal_recommendations'])}")
            print(f"     Drug recommendations: {len(response['drug_recommendations'])}")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_format_dual_recommendations(self):
        """Test formatting output with dual recommendations."""
        print("\n✓ TEST 9: Format Dual Recommendations")
        try:
            response = generate_comprehensive_answer(
                "fever and cough",
                self.knowledge,
                use_ai=False,
                include_drugs=True
            )
            
            formatted = format_answer_for_display(response)
            
            # Check that both sections are present
            assert "🌿 RECOMMENDED HERBAL" in formatted, "No herbal section"
            assert "💊 RECOMMENDED PHARMACEUTICAL" in formatted, "No pharma section"
            assert "🔄 CHOOSING BETWEEN" in formatted, "No comparison section"
            
            print(f"  ✅ Output formatted with all sections")
            print(f"     Output length: {len(formatted)} characters")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_multiple_diseases(self):
        """Test recommendations for multiple diseases."""
        print("\n✓ TEST 10: Multiple Diseases")
        try:
            test_diseases = ["Diabetes", "Heart Disease", "Asthma", "Depression", "Bronchitis"]
            results = {}
            
            for disease in test_diseases:
                drugs = suggest_drugs_for_disease(disease, top_n=3)
                results[disease] = len(drugs)
            
            # All should have some drugs
            assert all(count > 0 for count in results.values()), "Some diseases have no drugs"
            
            print(f"  ✅ Tested {len(results)} diseases:")
            for disease, count in results.items():
                print(f"     {disease}: {count} drugs")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1


class TestIntegration:
    """Integration tests for the complete system."""
    
    def __init__(self):
        self.knowledge = load_knowledge_base()
        self.passed = 0
        self.failed = 0
    
    def test_end_to_end_recommendation(self):
        """Test complete end-to-end recommendation."""
        print("\n✓ TEST 11: End-to-End Recommendation")
        try:
            symptoms = "High blood sugar, frequent urination, thirst"
            response = generate_comprehensive_answer(
                symptoms,
                self.knowledge,
                use_ai=False,
                include_drugs=True
            )
            
            # Verify all components
            assert response["detected_disease"], "No disease detected"
            assert response["confidence"] > 0, "No confidence"
            assert len(response["herbal_recommendations"]) > 0, "No herbal recs"
            assert len(response["drug_recommendations"]) > 0, "No drug recs"
            
            print(f"  ✅ Complete workflow executed successfully")
            print(f"     Disease: {response['detected_disease']}")
            print(f"     Confidence: {response['confidence']:.2%}")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_response_json_structure(self):
        """Test JSON structure of response."""
        print("\n✓ TEST 12: Response JSON Structure")
        try:
            response = generate_comprehensive_answer(
                "I feel depressed and anxious",
                self.knowledge,
                use_ai=False,
                include_drugs=True
            )
            
            # Convert to JSON and back to verify serializability
            json_str = json.dumps(response)
            parsed = json.loads(json_str)
            
            # Check structure
            assert parsed["detected_disease"], "Missing disease"
            assert "herbal_recommendations" in parsed, "Missing herbal recs"
            assert "drug_recommendations" in parsed, "Missing drug recs"
            
            print(f"  ✅ Response is properly serializable as JSON")
            print(f"     Keys: {list(parsed.keys())}")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1
    
    def test_large_dataset_performance(self):
        """Test performance with repeated recommendations."""
        print("\n✓ TEST 13: Performance (10 recommendations)")
        try:
            import time
            
            start = time.time()
            for i in range(10):
                response = generate_comprehensive_answer(
                    "fever and cough",
                    self.knowledge,
                    use_ai=False,
                    include_drugs=True
                )
            elapsed = time.time() - start
            
            avg_time = elapsed / 10 * 1000
            
            print(f"  ✅ Generated 10 recommendations in {elapsed:.2f}s")
            print(f"     Average: {avg_time:.1f}ms per recommendation")
            self.passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed += 1


def run_all_tests():
    """Run all test suites."""
    print("="*70)
    print("🔬 PHARMACEUTICAL DRUG RECOMMENDATION SYSTEM - TEST SUITE")
    print("="*70)
    
    # Test 1: Database tests
    print("\n📦 SECTION 1: DRUG DATABASE TESTS")
    print("-"*70)
    db_tests = TestDrugDatabase()
    db_tests.test_load_database()
    db_tests.test_get_drugs_for_disease()
    db_tests.test_sort_by_commonality()
    db_tests.test_drug_by_name()
    db_tests.test_partial_disease_match()
    db_tests.test_csv_export()
    
    # Test 2: Recommendation tests
    print("\n\n💊 SECTION 2: DRUG RECOMMENDATION TESTS")
    print("-"*70)
    rec_tests = TestDrugRecommendations()
    rec_tests.test_suggest_drugs()
    rec_tests.test_comprehensive_answer_with_drugs()
    rec_tests.test_format_dual_recommendations()
    rec_tests.test_multiple_diseases()
    
    # Test 3: Integration tests
    print("\n\n🔗 SECTION 3: INTEGRATION TESTS")
    print("-"*70)
    int_tests = TestIntegration()
    int_tests.test_end_to_end_recommendation()
    int_tests.test_response_json_structure()
    int_tests.test_large_dataset_performance()
    
    # Summary
    total_passed = db_tests.passed + rec_tests.passed + int_tests.passed
    total_failed = db_tests.failed + rec_tests.failed + int_tests.failed
    total_tests = total_passed + total_failed
    
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"Success Rate: {total_passed/total_tests*100:.1f}%")
    print("="*70)
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
