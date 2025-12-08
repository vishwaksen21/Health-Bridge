#!/usr/bin/env python3
"""
Test script to verify all Streamlit app connections and dependencies
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 70)
print("🧪 CURE-BLEND STREAMLIT CONNECTION TEST")
print("=" * 70)
print()

# Test 1: Check Python version
print("1️⃣  Testing Python version...")
print(f"   Python version: {sys.version}")
print("   ✅ Python OK")
print()

# Test 2: Check core dependencies
print("2️⃣  Testing core dependencies...")
missing_deps = []
required_deps = {
    'streamlit': 'Streamlit web framework',
    'pandas': 'Data manipulation',
    'numpy': 'Numerical computing',
    'sklearn': 'Machine learning',
    'joblib': 'Model persistence',
    'networkx': 'Graph processing',
    'gensim': 'Word embeddings'
}

for dep, desc in required_deps.items():
    try:
        __import__(dep)
        print(f"   ✅ {dep:12s} - {desc}")
    except ImportError:
        print(f"   ❌ {dep:12s} - {desc} (MISSING)")
        missing_deps.append(dep)

if missing_deps:
    print(f"\n   ⚠️  Missing dependencies: {', '.join(missing_deps)}")
    print(f"   💡 Install with: pip install {' '.join(missing_deps)}")
else:
    print("   ✅ All core dependencies OK")
print()

# Test 3: Check project modules
print("3️⃣  Testing project modules...")
modules = {
    'src.ai_assistant': 'Core AI assistant',
    'src.enhanced_symptom_predictor': 'Enhanced predictor',
    'src.multi_disease_detector': 'Multi-disease detection',
    'src.severity_classifier': 'Severity classification',
    'src.personalized_recommender': 'Personalized recommendations',
    'src.feedback_system': 'Feedback system',
    'src.explainability': 'Explainability module',
    'src.drug_database': 'Drug database'
}

core_ok = True
advanced_ok = True

for mod, desc in modules.items():
    try:
        __import__(mod)
        print(f"   ✅ {mod:40s} - {desc}")
        if mod == 'src.ai_assistant':
            core_ok = core_ok and True
    except ImportError as e:
        print(f"   ⚠️  {mod:40s} - {desc} (Optional)")
        if mod in ['src.ai_assistant']:
            core_ok = False
        else:
            advanced_ok = False

print()
if core_ok:
    print("   ✅ Core modules OK")
else:
    print("   ❌ Core modules have issues")

if advanced_ok:
    print("   ✅ Advanced features available")
else:
    print("   ⚠️  Some advanced features unavailable (optional)")
print()

# Test 4: Check data files
print("4️⃣  Testing data files...")
data_files = {
    'data/symptom_disease.csv': 'Symptom-disease mapping',
    'data/symptom_model.pkl': 'Trained model (optional)',
    'data/HITD_network.edgelist': 'Network graph (optional)',
    'data/embeddings.kv': 'Word embeddings (optional)'
}

data_ok = False
for file, desc in data_files.items():
    if os.path.exists(file):
        size = os.path.getsize(file)
        size_str = f"{size:,} bytes" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
        print(f"   ✅ {file:40s} - {size_str}")
        if file == 'data/symptom_disease.csv':
            data_ok = True
    else:
        print(f"   ⚠️  {file:40s} - {desc} (Not found)")

print()
if data_ok:
    print("   ✅ Essential data files present")
else:
    print("   ❌ Missing essential data files")
print()

# Test 5: Test core functionality
print("5️⃣  Testing core functionality...")
try:
    from src.ai_assistant import load_knowledge_base, generate_comprehensive_answer
    
    print("   Loading knowledge base...")
    kb = load_knowledge_base()
    
    if kb:
        print("   ✅ Knowledge base loaded successfully")
        
        # Test a simple prediction
        print("   Testing symptom analysis...")
        test_symptoms = "fever headache body ache"
        result = generate_comprehensive_answer(
            test_symptoms, 
            kb, 
            use_ai=False, 
            include_drugs=True
        )
        
        if result and 'detected_disease' in result:
            print(f"   ✅ Analysis working (Test result: {result['detected_disease']})")
        else:
            print("   ⚠️  Analysis returned unexpected result")
    else:
        print("   ⚠️  Knowledge base is None")
        
except Exception as e:
    print(f"   ❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 6: Streamlit availability
print("6️⃣  Testing Streamlit...")
try:
    import streamlit as st
    print(f"   ✅ Streamlit version: {st.__version__}")
    print("   ✅ Ready to run Streamlit app")
except Exception as e:
    print(f"   ❌ Streamlit error: {e}")

print()

# Summary
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print()

if not missing_deps and core_ok and data_ok:
    print("✅ ALL SYSTEMS GO! Ready to run Streamlit app")
    print()
    print("🚀 Run the app with:")
    print("   bash launch_streamlit.sh")
    print("   OR")
    print("   streamlit run streamlit_app.py")
else:
    print("⚠️  SYSTEM CHECK COMPLETED WITH WARNINGS")
    print()
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print(f"   Fix: pip install {' '.join(missing_deps)}")
        print()
    if not core_ok:
        print("❌ Core modules have issues")
        print("   Check src/ directory and Python path")
        print()
    if not data_ok:
        print("❌ Missing essential data files")
        print("   Run setup scripts or check data/ directory")
        print()
    
    print("💡 You can still try running the app - it may work with limited features")
    print("   bash launch_streamlit.sh")

print()
print("=" * 70)
