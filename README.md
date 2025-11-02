# 🏥 AI-Powered Herbal Medicine Assistant

An intelligent system that combines **machine learning**, **knowledge graphs**, and **AI** to provide personalized herbal medicine recommendations based on symptoms.

## 🌟 Features

### ✅ Current Capabilities

- **Symptom-to-Disease Prediction**: Uses TF-IDF + Logistic Regression to detect diseases from natural language symptoms
- **Herbal Recommendations**: Graph-based embedding approach (Node2Vec) to suggest relevant herbs
- **Knowledge Graph**: Network of herbs, ingredients, targets, and diseases
- **Professional Output**: Well-formatted, easy-to-read recommendations
- **Medical Disclaimers**: Built-in reminders to consult healthcare professionals

### 🚀 Optional: AI-Enhanced Insights

- **LLM Integration**: Optional integration with GitHub Models (OpenAI, Meta Llama, etc.)
- **Deep Analysis**: AI-generated explanations of how herbs work
- **Personalized Guidance**: Natural language recommendations
- **Cost-Free**: Uses GitHub's free model access tier

---

## 📦 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Assistant

```bash
# Dataset mode (no LLM)
python main.py

# Or pipe in symptoms
echo "high fever and chills" | python main.py
```

### 3. (Optional) Enable AI Insights

```bash
# Set your GitHub token
export GITHUB_TOKEN="your_github_pat_here"

# Run again
python main.py
```

---

## 🎯 Usage Examples

### Example 1: Fever & Chills

```
🧍 Enter your problem or symptoms: high fever and chills

╔════════════════════════════════════════════════════════════════╗
║           🏥 AI-POWERED HERBAL MEDICINE ASSISTANT             ║
╚════════════════════════════════════════════════════════════════╝

📋 SYMPTOM ANALYSIS
───────────────────────────────────────────────────────────────
Your Input: "high fever and chills"

🧠 Detected Condition: Malaria
   Confidence: 31.1%

🌿 RECOMMENDED HERBAL INGREDIENTS
───────────────────────────────────────────────────────────────

1. WITHAFERIN A
   • Relevance: 33.69%
   • Benefits: Traditional herbal remedy
   • Usage: Consult herbalist for dosage

2. EUGENOL
   • Relevance: 33.45%
   • Benefits: Traditional herbal remedy
   • Usage: Consult herbalist for dosage

3. AZADIRACHTIN
   • Relevance: 33.04%
   • Benefits: Traditional herbal remedy
   • Usage: Consult herbalist for dosage

4. CURCUMIN
   • Relevance: 32.08%
   • Benefits: Traditional herbal remedy
   • Usage: Consult herbalist for dosage
```

---

## 🏗️ System Architecture

```
INPUT: User Symptoms
    ↓
Symptom Predictor (TF-IDF + LogReg)
    ↓
Knowledge Graph (NetworkX + Node2Vec)
    ↓
AI LLM (Optional - GitHub Models)
    ↓
Beautiful Formatter
    ↓
OUTPUT: Professional Recommendation
```

---

## 📊 Components

| Component | Purpose | Technology |
|-----------|---------|-----------|
| Symptom Predictor | Disease detection | TF-IDF + Logistic Regression |
| Knowledge Graph | Herb relationships | NetworkX + Node2Vec |
| Ensemble Model | Herbal recommendations | Stacking Classifier |
| LLM Integration | AI insights (optional) | GitHub Models / Azure OpenAI |

---

## 🧪 Testing

Run the system test:

```bash
python test_system.py
```

Expected output: `✅ All systems operational!`

---

## 📚 Full Documentation

See **[AI_SETUP_GUIDE.md](AI_SETUP_GUIDE.md)** for:
- Complete LLM setup instructions
- GitHub Models free tier configuration
- Environment variables reference
- Troubleshooting guide
- Advanced Azure OpenAI integration

---

## 🚀 How to Use

### Basic Usage (Dataset Mode)

```bash
python main.py
# Enter symptoms and get herbal recommendations
```

### With AI Insights

```bash
export GITHUB_TOKEN="your_github_pat"
python main.py
# Get AI-enhanced explanations
```

### Batch Processing

```bash
cat symptoms.txt | python main.py
# Process multiple symptoms from file
```

---

## 🔧 Configuration

### GitHub Models (Free)

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

### Select Different AI Models

```bash
export GITHUB_MODELS_NAME="openai/gpt-4o-mini"      # Fast & cheap
export GITHUB_MODELS_NAME="openai/gpt-4o"           # Better quality
export GITHUB_MODELS_NAME="meta/llama-3.3-70b-instruct"  # Open source
```

### Azure OpenAI (Optional)

```bash
export AZURE_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_API_KEY="your_api_key"
```

---

## 📈 Model Details

- **Disease Prediction**: Trained on Kaggle dataset (41 diseases)
- **Herbal Recommendations**: Ensemble learning with graph embeddings
- **Graph Size**: 59 nodes, 53 edges
- **Embedding Dimension**: 64-dim Node2Vec vectors

---

## ⚠️ Medical Disclaimer

**This is for educational purposes only.** Not a substitute for professional medical advice. Always consult healthcare professionals before starting any herbal treatment.

---

## 📁 Project Structure

```
research/
├── main.py                              # Entry point
├── requirements.txt                     # Dependencies
├── test_system.py                       # System test
├── README.md                            # This file
├── AI_SETUP_GUIDE.md                   # LLM setup guide
├── src/
│   ├── ai_assistant.py                 # Main AI module (NEW)
│   ├── symptom_predictor.py            # Disease prediction
│   ├── train_predictor.py              # Model training
│   ├── embeddings.py                   # Node2Vec embeddings
│   ├── expand_graph_v2.py              # Graph expansion
│   └── ...
└── data/
    ├── diseases.csv                     # Disease data
    ├── ingredients.csv                  # Herbal ingredients
    ├── targets.csv                      # Molecular targets
    ├── herbs.csv                        # Herb properties
    ├── HITD_network_expanded_v2.edgelist  # Knowledge graph
    ├── embeddings.kv                    # Node2Vec embeddings
    ├── stack_model.pkl                  # Recommendation model
    └── symptom_model.pkl                # Disease prediction model
```

---

## 🎯 What's New

✨ **Version 1.0 - AI-Enhanced Release**

- ✅ Integrated AI LLM support (GitHub Models)
- ✅ Enhanced user interface with better formatting
- ✅ Batch processing support (stdin/pipe mode)
- ✅ System test suite
- ✅ Comprehensive setup guide
- ✅ LLM insights generation
- ✅ Multi-model support

---

## 🔄 Workflow

```
User Input (e.g., "fever and headache")
    ↓
Symptom Predictor → Disease (Malaria)
    ↓
Knowledge Graph → Top 5 Herbs
    ↓
[IF LLM ENABLED] AI Insights
    ↓
Professional Output with Recommendations
```

---

## 📞 Quick Help

**Test installation:**
```bash
python test_system.py
```

**Run the assistant:**
```bash
python main.py
```

**Enable AI:**
```bash
export GITHUB_TOKEN="your_token"
python main.py
```

**See detailed guide:**
```bash
cat AI_SETUP_GUIDE.md
```

---

**Status**: ✅ Operational  
**Last Updated**: October 2025  
**Version**: 1.0




# Test everything
python test_system.py

# Run the assistant
python main.py

# Enter symptoms: "high fever and chills"
# Get: Disease + herb recommendations

# (Optional) Enable AI
export GITHUB_TOKEN="ghp_xxxx..."
python main.py  # Now with AI insights!


# Steamlit
streamlit run streamlit_app.py
