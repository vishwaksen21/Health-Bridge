#!/usr/bin/env python3
"""
Simple Streamlit launcher with pre-checks
"""
import os
import sys
import subprocess

print("=" * 70)
print("🏥 CURE-BLEND STREAMLIT APP LAUNCHER")
print("=" * 70)
print()

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Quick checks
print("📋 Pre-flight checks...")
print()

# Check Streamlit
try:
    import streamlit
    print(f"✅ Streamlit {streamlit.__version__} installed")
except ImportError:
    print("❌ Streamlit not found")
    print("   Installing Streamlit...")
    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "-q"])
    import streamlit
    print(f"✅ Streamlit {streamlit.__version__} installed")

# Check core deps
deps = ['pandas', 'numpy', 'sklearn']
missing = []
for dep in deps:
    try:
        __import__(dep)
        print(f"✅ {dep} available")
    except ImportError:
        missing.append(dep)
        print(f"⚠️  {dep} not found")

if missing:
    print()
    print(f"💡 Install missing: pip install {' '.join(missing)}")
    print()

# Check data
if os.path.exists('data/symptom_disease.csv'):
    print("✅ Data files found")
else:
    print("⚠️  Some data files missing (will use fallbacks)")

print()
print("=" * 70)
print("🚀 Starting Streamlit...")
print("=" * 70)
print()
print("📱 Opening at: http://localhost:8501")
print("🛑 Press Ctrl+C to stop")
print()

# Launch Streamlit
try:
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "streamlit_app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ])
except KeyboardInterrupt:
    print()
    print("✅ Server stopped")
