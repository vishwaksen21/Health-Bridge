# 🏥 Cure-Blend Streamlit App - Complete Guide

## 🚀 Quick Start

### Method 1: Using the Launch Script (Recommended)
```bash
bash launch_streamlit.sh
```

### Method 2: Direct Streamlit Command
```bash
streamlit run streamlit_app.py
```

### Method 3: With Custom Port
```bash
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
```

---

## 📋 Pre-requisites

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning
- `joblib` - Model persistence
- `networkx` - Graph processing
- `gensim` - Word embeddings
- `matplotlib` - Plotting (optional)
- `shap` - Explainability (optional)

### 2. Verify Installation
```bash
python3 test_streamlit_connections.py
```

This will check:
- ✅ Python version
- ✅ All dependencies
- ✅ Project modules
- ✅ Data files
- ✅ Core functionality

---

## 🎯 Features

### Core Features (Always Available)
- **Symptom Analysis**: Enter symptoms and get disease predictions
- **Dual Recommendations**: Both herbal and pharmaceutical options
- **Confidence Scoring**: Know how reliable each prediction is
- **Interactive UI**: User-friendly web interface
- **Medical Disclaimer**: Important safety information

### Advanced Features (When Dependencies Available)
- **Multi-Disease Detection**: Identify comorbidities and overlapping conditions
- **Severity Classification**: 0-100 scoring system with emergency alerts
- **Personalized Recommendations**: Based on age, gender, and medical conditions
- **Safety Warnings**: Contraindications for special populations
- **Explainability**: See which symptoms contributed to diagnosis
- **Feedback System**: Help improve the system with your input

---

## 📱 Using the App

### Step 1: Access the App
Once running, open your browser to:
```
http://localhost:8501
```

### Step 2: Describe Symptoms
- Enter your symptoms in the text area
- Be specific: include duration, intensity, location
- Try example buttons for quick demos

### Step 3: (Optional) Create Patient Profile
Enable in sidebar for personalized recommendations:
- Age and gender
- Pregnancy/breastfeeding status
- Existing conditions (diabetes, hypertension, etc.)

### Step 4: Get Analysis
Click "Analyze Symptoms" and review:
- Primary diagnosis with confidence score
- Herbal remedy suggestions
- Pharmaceutical medication options
- AI-powered insights
- Severity assessment (if advanced features enabled)

### Step 5: Review Recommendations
Compare options in tabs:
- 🌿 **Herbal**: Natural ingredients with benefits
- 💊 **Pharmaceutical**: Clinically proven medications
- 🤖 **AI Insights**: Detailed explanations

---

## ⚙️ Configuration

### Sidebar Settings

**Enable Advanced Features**
- Turn on for multi-disease detection, severity scoring
- Requires additional modules to be installed
- Status shown in "System Status" expander

**Enable AI Insights**
- Get detailed AI-powered explanations
- Requires Azure AI credentials (optional)
- Works without AI in basic mode

**Personalized Recommendations**
- Create patient profile for safety warnings
- Get contraindication alerts
- Age-appropriate dosing considerations

---

## 🔧 Troubleshooting

### Issue: "Core modules not loaded"
**Solution:**
```bash
# Check if src/__init__.py exists
ls src/__init__.py

# If missing, create it
touch src/__init__.py

# Verify Python path
python3 -c "import sys; print(sys.path)"
```

### Issue: "Advanced features not available"
**Solution:**
```bash
# Install optional dependencies
pip install shap matplotlib

# Check if modules exist
ls src/multi_disease_detector.py
ls src/severity_classifier.py
ls src/personalized_recommender.py
```

### Issue: "Knowledge base not loaded"
**Solution:**
```bash
# Check data files
ls data/symptom_disease.csv
ls data/symptom_model.pkl

# If missing, run setup
python3 setup_complete_datasets.py
```

### Issue: Port already in use
**Solution:**
```bash
# Kill existing process
pkill -f "streamlit run"

# Or use different port
streamlit run streamlit_app.py --server.port=8502
```

### Issue: Module import errors
**Solution:**
```bash
# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/workspaces/Cure-Blend"

# Or install as package
pip install -e .
```

---

## 🔍 Testing Connections

Run the comprehensive test:
```bash
python3 test_streamlit_connections.py
```

Expected output:
```
✅ Python OK
✅ All core dependencies OK
✅ Core modules OK
✅ Advanced features available
✅ Essential data files present
✅ Knowledge base loaded successfully
✅ Analysis working
✅ Ready to run Streamlit app
```

---

## 📊 System Status Indicators

In the sidebar, check "System Status" expander:

| Indicator | Meaning |
|-----------|---------|
| ✅ Core System: Active | Main functionality working |
| ✅ Advanced Features: Active | All optional features available |
| ✅ Knowledge Base: Loaded | Data successfully loaded |
| ⚠️ Advanced Features: Disabled | Some dependencies missing |
| ❌ Core System: Error | Critical issue - check logs |

---

## 💡 Tips for Best Results

### Describing Symptoms
- **Good**: "High fever (102°F) for 2 days, severe headache, body aches, chills, fatigue"
- **Poor**: "not feeling well"

### Using Patient Profiles
- Enable for personalized safety warnings
- Update profile if conditions change
- Helps identify contraindications

### Interpreting Confidence
- **High (>70%)**: Strong match, symptoms clearly indicate condition
- **Medium (40-70%)**: Possible match, consider alternatives
- **Low (<40%)**: Weak match, consult healthcare provider

### When to Seek Emergency Care
- Chest pain, difficulty breathing
- Severe bleeding, trauma
- Loss of consciousness
- Severe allergic reactions
- Any "Emergency" severity rating

---

## 🔒 Privacy & Safety

### Data Collection
- Symptoms are processed locally
- Feedback is optional
- No personal health data stored permanently

### Medical Disclaimer
⚠️ **This is an informational tool only**
- Always consult healthcare professionals
- Do not use for diagnosis or treatment decisions
- Verify all recommendations with your doctor
- Check for allergies and drug interactions

---

## 🆘 Getting Help

### Common Questions

**Q: Can I use this for diagnosis?**
A: No. This is an informational tool. Always consult a healthcare provider.

**Q: Are the medications safe for me?**
A: Check with your doctor. Enable patient profile for basic safety checks.

**Q: How accurate is the system?**
A: Accuracy varies. Check the confidence score. Low confidence = see a doctor.

**Q: Can I trust herbal recommendations?**
A: Herbal remedies should be discussed with your healthcare provider. Quality varies.

### Support
- Check documentation in the app ("About Cure-Blend")
- Review examples and help sections
- Run test script for technical issues
- Consult README files in the project

---

## 📈 Recent Improvements

### Version 2.0 Updates
✅ Enhanced error handling and fallbacks
✅ Better module connectivity checks
✅ Improved UI with system status indicators
✅ Comprehensive testing script
✅ Better documentation and help sections
✅ Mobile-responsive design
✅ Startup diagnostics
✅ Footer with quick help
✅ Expanded troubleshooting guide

### Bug Fixes
✅ Fixed module import issues
✅ Added graceful degradation for missing features
✅ Improved error messages
✅ Better handling of missing data files
✅ Enhanced connection validation

---

## 📝 File Structure

```
Cure-Blend/
├── streamlit_app.py              # Main Streamlit application
├── launch_streamlit.sh           # Launch script (improved)
├── test_streamlit_connections.py # Connection test script (new)
├── STREAMLIT_GUIDE.md           # This guide (new)
├── requirements.txt              # Dependencies
├── src/                          # Source modules
│   ├── ai_assistant.py          # Core AI logic
│   ├── enhanced_symptom_predictor.py
│   ├── multi_disease_detector.py
│   ├── severity_classifier.py
│   ├── personalized_recommender.py
│   └── ...
└── data/                         # Data files
    ├── symptom_disease.csv
    ├── symptom_model.pkl
    └── ...
```

---

## 🎓 Learn More

- Review example queries in the app
- Check "About Cure-Blend" in app footer
- Read "Need Help?" section in app
- Explore source code in `src/` directory
- Check main README.md for project overview

---

**Version:** 2.0  
**Last Updated:** December 8, 2025  
**Status:** ✅ Production Ready
