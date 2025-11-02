#!/usr/bin/env python3
"""
Quick test script for the AI-Powered Herbal Medicine Assistant
"""

import sys
import os

def test_imports():
    """Test if all required libraries are available."""
    print("🧪 Testing imports...")
    
    packages = {
        "pandas": "Data processing",
        "numpy": "Numerical computing",
        "networkx": "Graph analysis",
        "gensim": "Embeddings",
        "sklearn": "Machine learning",
        "joblib": "Model serialization",
    }
    
    failed = []
    for package, purpose in packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package} - {purpose}")
        except ImportError:
            print(f"  ❌ {package} - {purpose}")
            failed.append(package)
    
    return len(failed) == 0

def test_data_files():
    """Test if all required data files exist."""
    print("\n📁 Testing data files...")
    
    files = [
        "data/diseases.csv",
        "data/ingredients.csv",
        "data/targets.csv",
        "data/herbs.csv",
        "data/HITD_network_expanded_v2.edgelist",
        "data/embeddings.kv",
        "data/stack_model.pkl",
        "data/symptom_model.pkl",
    ]
    
    failed = []
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            print(f"  ❌ {file} (MISSING)")
            failed.append(file)
    
    return len(failed) == 0

def test_models():
    """Test if models load correctly."""
    print("\n🤖 Testing models...")
    
    try:
        from src.symptom_predictor import predict_disease
        print("  ✅ Symptom predictor loaded")
        
        # Test prediction
        disease, conf = predict_disease("fever and cough")
        print(f"  ✅ Test prediction: {disease} ({conf})")
        
        return True
    except Exception as e:
        print(f"  ❌ Model loading failed: {e}")
        return False

def test_knowledge_base():
    """Test if knowledge base loads correctly."""
    print("\n📚 Testing knowledge base...")
    
    try:
        from src.ai_assistant import load_knowledge_base
        knowledge = load_knowledge_base()
        
        print(f"  ✅ Diseases: {len(knowledge['diseases'])} records")
        print(f"  ✅ Ingredients: {len(knowledge['ingredients'])} records")
        print(f"  ✅ Targets: {len(knowledge['targets'])} records")
        
        return True
    except Exception as e:
        print(f"  ❌ Knowledge base loading failed: {e}")
        return False

def test_ai_assistant():
    """Test if AI assistant works."""
    print("\n🏥 Testing AI assistant...")
    
    try:
        from src.ai_assistant import load_knowledge_base, generate_comprehensive_answer
        
        knowledge = load_knowledge_base()
        response = generate_comprehensive_answer("fever and chills", knowledge, use_ai=False)
        
        print(f"  ✅ Response generated")
        print(f"  ✅ Detected: {response['detected_disease']}")
        print(f"  ✅ Confidence: {response['confidence']:.2%}")
        print(f"  ✅ Recommendations: {len(response['recommendations'])} herbs")
        
        return True
    except Exception as e:
        print(f"  ❌ AI assistant test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_config():
    """Test if LLM is configured."""
    print("\n🤖 Testing LLM configuration...")
    
    github_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT")
    
    if github_token:
        print(f"  ✅ GITHUB_TOKEN is set ({github_token[:10]}...)")
        
        try:
            from azure.ai.inference import ChatCompletionsClient
            print("  ✅ Azure AI Inference SDK available")
            return True
        except ImportError:
            print("  ⚠️  Azure SDK not installed. Run: pip install azure-ai-inference")
            return False
    else:
        print("  ℹ️  GITHUB_TOKEN not set (LLM insights will be disabled)")
        print("     Set it with: export GITHUB_TOKEN='your_github_pat'")
        return True  # Not an error, just a warning

def main():
    """Run all tests."""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         🧪 AI HERBAL MEDICINE ASSISTANT - SYSTEM TEST         ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    results = {
        "Imports": test_imports(),
        "Data Files": test_data_files(),
        "Models": test_models(),
        "Knowledge Base": test_knowledge_base(),
        "AI Assistant": test_ai_assistant(),
        "LLM Config": test_llm_config(),
    }
    
    print("\n" + "=" * 64)
    print("📊 TEST SUMMARY")
    print("=" * 64)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("=" * 64)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All systems operational! You're ready to use the assistant.\n")
        print("   Run: python main.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix issues above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
