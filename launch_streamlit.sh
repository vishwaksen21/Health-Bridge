#!/bin/bash

# Streamlit Web UI - Quick Start Guide

echo "======================================================================"
echo "🌿 CURE-BLEND STREAMLIT WEB UI - LAUNCH SCRIPT"
echo "======================================================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📂 Working directory: $SCRIPT_DIR"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python3 --version || python --version
echo ""

# Check if streamlit is installed
echo "📦 Checking Streamlit installation..."
if ! python3 -m streamlit --version &> /dev/null && ! python -m streamlit --version &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing..."
    pip install streamlit -q || pip3 install streamlit -q
else
    python3 -m streamlit --version 2>/dev/null || python -m streamlit --version
fi
echo ""

# Check if requirements are met
echo "📋 Checking dependencies..."
python3 -c "import pandas, numpy, sklearn, joblib; print('✅ Core dependencies OK')" 2>/dev/null || \
python -c "import pandas, numpy, sklearn, joblib; print('✅ Core dependencies OK')" 2>/dev/null || \
echo "⚠️  Some dependencies missing. Run: pip install -r requirements.txt"
echo ""

# Kill any existing streamlit processes
echo "🧹 Cleaning up existing processes..."
pkill -f "streamlit run" 2>/dev/null
sleep 2

# Check if data files exist
echo "📊 Checking data files..."
if [ -f "data/symptom_disease.csv" ]; then
    echo "✅ symptom_disease.csv found"
else
    echo "⚠️  symptom_disease.csv not found"
fi

if [ -f "data/symptom_model.pkl" ]; then
    echo "✅ symptom_model.pkl found"
else
    echo "⚠️  symptom_model.pkl not found (will be created on first run)"
fi
echo ""

# Start Streamlit app
echo "======================================================================"
echo "🚀 Starting Streamlit Web UI..."
echo "======================================================================"
echo ""
echo "📱 The app will open in your browser at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the server"
echo ""
echo "======================================================================"
echo ""

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 -m streamlit run streamlit_app.py --server.headless=true --server.port=8501 --server.address=0.0.0.0
else
    python -m streamlit run streamlit_app.py --server.headless=true --server.port=8501 --server.address=0.0.0.0
fi

echo ""
echo "======================================================================"
echo "✅ Streamlit server stopped"
echo "======================================================================"
echo "======================================================================"
echo "✅ Streamlit stopped"
echo "======================================================================"
