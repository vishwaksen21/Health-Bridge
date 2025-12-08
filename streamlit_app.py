"""
Cure-Blend: AI-Powered Health Recommendation System
Streamlit Web Application with Advanced Features

Features:
- Multi-disease detection with comorbidity analysis
- Severity classification (0-100 scoring)
- Personalized recommendations for special populations
- Interactive patient profile creation
- Visual severity gauges and confidence charts
- Dual recommendations: Herbal + Pharmaceutical
"""

import streamlit as st
import sys
import os
import json
from typing import Optional, Dict, List
import traceback

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Core imports with error handling
try:
    from src.ai_assistant import load_knowledge_base, generate_comprehensive_answer
    CORE_OK = True
except ImportError as e:
    st.error(f"⚠️ Core module import error: {e}")
    CORE_OK = False

# Try to import advanced features
ADVANCED_FEATURES_OK = False
try:
    from src.multi_disease_detector import MultiDiseaseDetector, format_multi_disease_output
    from src.severity_classifier import SeverityClassifier, format_severity_output
    from src.personalized_recommender import (
        PersonalizedRecommender,
        PatientProfile,
        AgeGroup,
        format_personalized_output
    )
    from src.feedback_system import FeedbackSystem
    from src.explainability import SymptomMatcher, create_symptom_importance_chart
    ADVANCED_FEATURES_OK = True
except ImportError as e:
    # Advanced features are optional
    pass

# Page configuration
st.set_page_config(
    page_title="Cure-Blend - AI Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI (mobile-responsive)
st.markdown("""
    <style>
    .main-header {
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #fff 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            font-size: 1.1rem;
            padding: 0.75rem;
        }
        .stTextInput input {
            font-size: 1rem;
        }
        div[data-testid="column"] {
            padding: 0.5rem !important;
        }
    }
    .stAlert {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .severity-emergency {
        background-color: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .severity-severe {
        background-color: #ff8800;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .severity-moderate {
        background-color: #ffbb33;
        color: black;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .severity-mild {
        background-color: #00c851;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .confidence-high {
        color: #00c851;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffbb33;
        font-weight: bold;
    }
    .confidence-low {
        color: #ff4444;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = None
if 'patient_profile' not in st.session_state:
    st.session_state.patient_profile = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'feedback_system' not in st.session_state:
    if ADVANCED_FEATURES_OK:
        st.session_state.feedback_system = FeedbackSystem()
    else:
        st.session_state.feedback_system = None
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False

@st.cache_resource
def load_system():
    """Load the knowledge base (cached)"""
    try:
        if not CORE_OK:
            st.error("⚠️ Core modules not loaded. Please check installation.")
            return None
        kb = load_knowledge_base()
        return kb
    except Exception as e:
        st.error(f"Error loading knowledge base: {e}")
        st.info("The system will continue with limited functionality.")
        return None

def create_patient_profile_sidebar():
    """Create patient profile input in sidebar"""
    with st.sidebar:
        st.header("👤 Patient Profile")
        
        use_profile = st.checkbox("Enable Personalized Recommendations", value=False, 
                                  help="Get safety warnings and contraindications based on your profile")
        
        if not use_profile:
            return None
        
        with st.expander("📋 Enter Patient Information", expanded=True):
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=30, step=1)
            gender = st.selectbox("Gender", ["male", "female", "other"])
            
            st.subheader("Special Conditions")
            is_pregnant = st.checkbox("Currently pregnant", value=False)
            is_breastfeeding = st.checkbox("Currently breastfeeding", value=False)
            
            st.subheader("Existing Health Conditions")
            has_diabetes = st.checkbox("Diabetes", value=False)
            has_hypertension = st.checkbox("Hypertension (High Blood Pressure)", value=False)
            has_kidney_disease = st.checkbox("Kidney Disease", value=False)
            has_liver_disease = st.checkbox("Liver Disease", value=False)
        
        # Create PatientProfile object
        profile = PatientProfile(
            age=age,
            gender=gender,
            is_pregnant=is_pregnant,
            is_breastfeeding=is_breastfeeding,
            has_diabetes=has_diabetes,
            has_hypertension=has_hypertension,
            has_kidney_disease=has_kidney_disease,
            has_liver_disease=has_liver_disease
        )
        
        # Show profile summary
        st.success("✅ Profile Created")
        special_pops = []
        if profile.is_pregnant:
            special_pops.append("Pregnant")
        if profile.is_breastfeeding:
            special_pops.append("Breastfeeding")
        if profile.age_group and profile.age_group.value in ['infant', 'child']:
            special_pops.append("Child")
        if profile.age_group and profile.age_group.value == 'elderly':
            special_pops.append("Elderly")
        if profile.has_diabetes:
            special_pops.append("Diabetic")
        if profile.has_hypertension:
            special_pops.append("Hypertensive")
        if profile.has_kidney_disease:
            special_pops.append("Kidney Disease")
        if profile.has_liver_disease:
            special_pops.append("Liver Disease")
        
        if special_pops:
            st.info(f"**Special Considerations**: {', '.join(special_pops)}")
        
        return profile

def display_severity_gauge(severity_score: int, severity_level: str):
    """Display severity as a visual gauge"""
    # Color mapping
    color_map = {
        "Emergency": "#ff4444",
        "Severe": "#ff8800",
        "Moderate-Severe": "#ffbb33",
        "Moderate": "#ffbb33",
        "Mild": "#00c851"
    }
    
    color = color_map.get(severity_level, "#00c851")
    
    # Create gauge visualization
    st.markdown(f"""
        <div style="padding: 1rem; background-color: {color}; color: white; 
                    border-radius: 10px; text-align: center; margin: 1rem 0;">
            <h2 style="margin: 0; color: white;">🚨 Severity: {severity_level}</h2>
            <h1 style="margin: 0.5rem 0; color: white; font-size: 3rem;">{severity_score}/100</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(severity_score / 100)

def display_confidence_badge(confidence: float):
    """Display confidence as a colored badge"""
    if confidence >= 0.7:
        level = "High"
        color = "confidence-high"
    elif confidence >= 0.4:
        level = "Medium"
        color = "confidence-medium"
    else:
        level = "Low"
        color = "confidence-low"
    
    st.markdown(f"""
        <span class="{color}">Confidence: {level} ({confidence*100:.1f}%)</span>
    """, unsafe_allow_html=True)

def display_multi_disease_chart(disease_analysis: dict):
    """Display multi-disease predictions as a bar chart"""
    if not disease_analysis.get('all_predictions'):
        return
    
    st.subheader("📊 Disease Probability Distribution")
    
    # Prepare data for chart
    diseases = []
    confidences = []
    
    for pred in disease_analysis['all_predictions'][:5]:  # Top 5
        diseases.append(pred['disease'])
        confidences.append(pred['confidence'] * 100)
    
    # Create bar chart
    chart_data = {
        'Disease': diseases,
        'Confidence (%)': confidences
    }
    
    st.bar_chart(chart_data, x='Disease', y='Confidence (%)', use_container_width=True)

def display_herbal_recommendations(ingredients: list):
    """Display herbal ingredients in a nice format"""
    if not ingredients:
        st.info("No herbal recommendations available.")
        return
    
    st.subheader("🌿 Herbal Ingredients")
    
    for i, ingredient in enumerate(ingredients, 1):
        name = ingredient.get('ingredient', ingredient.get('herb', 'Unknown'))
        with st.expander(f"**{i}. {name.upper()}**", expanded=(i <= 2)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Relevance**: {ingredient.get('relevance_score', 0)*100:.1f}%")
                st.progress(ingredient.get('relevance_score', 0))
                
                benefits = ingredient.get('benefits', 'General health support')
                st.markdown(f"**Benefits**: {benefits}")
                
                compounds = ingredient.get('active_compounds', 'Various compounds')
                st.markdown(f"**Active Compounds**: {compounds}")
            
            with col2:
                usage = ingredient.get('usage', ingredient.get('usage_guidelines', 'Consult herbalist'))
                st.info(f"**Usage**\n\n{usage}")

def display_pharmaceutical_recommendations(medications: list):
    """Display pharmaceutical medications in a nice format"""
    if not medications:
        st.info("No pharmaceutical recommendations available.")
        return
    
    st.subheader("💊 Pharmaceutical Medications")
    
    for i, med in enumerate(medications, 1):
        with st.expander(f"**{i}. {med.get('name', 'Unknown').upper()}**", expanded=(i <= 2)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Brand Names**: {med.get('brand_names', 'N/A')}")
                st.markdown(f"**Type**: {med.get('type', 'N/A')}")
                st.markdown(f"**Purpose**: {med.get('purpose', 'N/A')}")
                st.markdown(f"**Dosage**: {med.get('dosage', 'As prescribed')}")
            
            with col2:
                availability = med.get('availability', 'Unknown')
                st.markdown(f"**Availability**: {availability}")
                
                price = med.get('price_range', 'Varies')
                st.markdown(f"**Price Range**: {price}")
                
                side_effects = med.get('side_effects', 'Consult doctor')
                st.warning(f"**Side Effects**: {side_effects}")

def display_personalized_warnings(recommendations: dict):
    """Display personalized safety warnings"""
    warnings = recommendations.get('warnings', [])
    contraindications = recommendations.get('contraindications', [])
    
    if warnings:
        st.error("⚠️ **IMPORTANT WARNINGS**")
        for warning in warnings:
            st.markdown(f"- {warning}")
    
    if contraindications:
        st.error("❌ **AVOID THESE MEDICATIONS**")
        for contra in contraindications:
            with st.expander(f"**{contra['medication']}**", expanded=True):
                st.markdown(f"**Reason**: {contra['reason']}")
                if 'alternative' in contra:
                    st.info(f"**Alternative**: {contra['alternative']}")

def analyze_symptoms(symptoms: str, patient_profile: Optional[PatientProfile], 
                     use_ai: bool, use_advanced: bool):
    """Analyze symptoms with optional advanced features"""
    
    if not CORE_OK:
        return {
            'basic_response': {'error': 'System not initialized properly'},
            'disease_analysis': None,
            'severity': None,
            'recommendations': None
        }
    
    knowledge = st.session_state.knowledge_base
    
    if knowledge is None:
        return {
            'basic_response': {'error': 'Knowledge base not loaded'},
            'disease_analysis': None,
            'severity': None,
            'recommendations': None
        }
    
    # Basic prediction
    try:
        response = generate_comprehensive_answer(
            symptoms,
            knowledge,
            use_ai=use_ai,
            include_drugs=True
        )
    except Exception as e:
        st.error(f"Error during analysis: {e}")
        response = {
            'detected_disease': 'Unknown',
            'confidence': 0.0,
            'herbal_recommendations': [],
            'drug_recommendations': [],
            'ai_insights': f'Error: {str(e)}'
        }
    
    results = {
        'basic_response': response,
        'disease_analysis': None,
        'severity': None,
        'recommendations': None
    }
    
    if use_advanced and ADVANCED_FEATURES_OK:
        try:
            # Multi-disease detection
            detector = MultiDiseaseDetector()
            results['disease_analysis'] = detector.analyze_symptom_overlap(symptoms)
            
            # Severity assessment
            classifier = SeverityClassifier()
            primary_disease = response.get('detected_disease', 'Unknown')
            results['severity'] = classifier.analyze_severity(symptoms, primary_disease)
            
            # Personalized recommendations
            if patient_profile:
                recommender = PersonalizedRecommender()
                results['recommendations'] = recommender.personalize_recommendations(
                    disease=primary_disease,
                    severity_level=results['severity'].level,
                    patient=patient_profile
                )
        except Exception as e:
            st.warning(f"⚠️ Advanced features encountered an issue: {e}")
            st.info("Continuing with basic analysis...")
    
    return results

def main():
    """Main Streamlit application"""
    
    # Check if core modules are available
    if not CORE_OK:
        st.error("⚠️ **System Error**: Core modules are not loaded properly.")
        st.info("Please ensure all dependencies are installed: `pip install -r requirements.txt`")
        st.stop()
    
    # Header
    st.markdown('<div class="main-header">🏥 Cure-Blend 🌿<br/>AI-Powered Health Recommendation System</div>', 
                unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # System status
        with st.expander("📊 System Status", expanded=False):
            st.markdown(f"**Core System**: {'✅ Active' if CORE_OK else '❌ Error'}")
            st.markdown(f"**Advanced Features**: {'✅ Active' if ADVANCED_FEATURES_OK else '⚠️ Disabled'}")
            st.markdown(f"**Knowledge Base**: {'✅ Loaded' if st.session_state.knowledge_base else '⚠️ Not Loaded'}")
        
        # Advanced features toggle
        use_advanced = st.checkbox("Enable Advanced Features", value=ADVANCED_FEATURES_OK, 
                                    help="Multi-disease detection, severity scoring, personalized warnings")
        
        if not ADVANCED_FEATURES_OK and use_advanced:
            st.warning("⚠️ Advanced features not available. Install additional dependencies.")
            use_advanced = False
        
        # AI insights toggle
        use_ai = st.checkbox("Enable AI Insights", value=True,
                            help="Generate detailed explanations using AI")
        
        st.divider()
    
    # Patient profile (in sidebar)
    patient_profile = create_patient_profile_sidebar()
    
    # Main content area
    st.header("💬 Describe Your Symptoms")
    
    # Quick example buttons
    st.markdown("**💡 Try an Example:**")
    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    
    example_clicked = None
    with col_ex1:
        if st.button("🤒 Flu", key="ex1"):
            example_clicked = "fever headache body aches fatigue cough"
    with col_ex2:
        if st.button("🤕 Migraine", key="ex2"):
            example_clicked = "severe headache sensitivity to light nausea vomiting"
    with col_ex3:
        if st.button("😷 Cold", key="ex3"):
            example_clicked = "runny nose sneezing sore throat cough congestion"
    with col_ex4:
        if st.button("💔 Chest Pain", key="ex4"):
            example_clicked = "chest pain difficulty breathing shortness of breath"
    
    symptoms = st.text_area(
        "Enter your symptoms or health concerns:",
        value=example_clicked if example_clicked else "",
        height=100,
        placeholder="Example: frequent urination, burning sensation, lower abdominal discomfort",
        help="Describe your symptoms in detail. The more specific you are, the better the recommendations."
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        analyze_button = st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🔄 Clear Results", use_container_width=True)
    
    if clear_button:
        st.session_state.analysis_results = None
        st.rerun()
    
    # Load knowledge base
    if st.session_state.knowledge_base is None:
        with st.spinner("📚 Loading medical knowledge base..."):
            st.session_state.knowledge_base = load_system()
        st.success("✅ System ready!")
    
    # Analyze symptoms
    if analyze_button:
        if not symptoms.strip():
            st.error("⚠️ Please enter your symptoms first.")
        else:
            with st.spinner("🔍 Analyzing your symptoms..."):
                results = analyze_symptoms(symptoms, patient_profile, use_ai, use_advanced)
                st.session_state.analysis_results = results
                st.session_state.last_symptoms = symptoms  # Save for feedback
            st.success("✅ Analysis complete!")
    
    # Display results
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        response = results['basic_response']
        
        # Check for errors
        if 'error' in response:
            st.error(f"⚠️ Analysis Error: {response['error']}")
            st.info("Please try again or rephrase your symptoms.")
            return
        
        st.divider()
        st.header("📋 Analysis Results")
        
        # Primary diagnosis
        disease = response.get('detected_disease', 'Unknown')
        confidence = response.get('confidence', 0.5)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"🎯 Primary Diagnosis: {disease}")
        
        with col2:
            display_confidence_badge(confidence)
        
        # Explainability section
        if ADVANCED_FEATURES_OK and st.session_state.knowledge_base:
            try:
                import joblib
                vectorizer, model = joblib.load("data/symptom_model.pkl")
                matcher = SymptomMatcher(vectorizer, model)
                
                explanation = matcher.explain_prediction(
                    st.session_state.get('last_symptoms', ''),
                    disease,
                    confidence
                )
                
                with st.expander("🔍 Why This Diagnosis? (Click to see explanation)", expanded=False):
                    st.markdown("### Symptom Analysis")
                    
                    if explanation['matched_symptoms']:
                        st.markdown("**✅ Symptoms That Matched:**")
                        symptom_df = create_symptom_importance_chart(explanation, top_n=8)
                        st.bar_chart(symptom_df.set_index('Symptom'))
                    
                    if explanation['missing_symptoms']:
                        st.markdown("**⚠️ Common Symptoms Not Mentioned:**")
                        for symptom in explanation['missing_symptoms']:
                            st.markdown(f"- {symptom}")
                        st.info("💡 Tip: Mentioning these symptoms (if you have them) can improve accuracy")
                    
                    breakdown = explanation['confidence_breakdown']
                    st.markdown(f"**📊 Confidence Analysis:**")
                    st.write(f"- Overall: {breakdown['overall_confidence']:.1%}")
                    st.write(f"- Symptom Match Rate: {breakdown['match_rate']:.1%}")
                    st.info(breakdown['recommendation'])
            except Exception as e:
                pass  # Silently skip if explainability fails
        
        # Advanced features section
        if use_advanced and results.get('severity'):
            st.divider()
            st.header("🔬 Advanced Analysis")
            
            # Severity assessment
            severity = results['severity']
            display_severity_gauge(severity.score, severity.level)
            
            # Show severity factors
            if severity.factors:
                with st.expander("📊 Contributing Factors", expanded=False):
                    for factor in severity.factors:
                        st.markdown(f"- {factor}")
            
            # Show recommendations
            if severity.recommendations:
                st.markdown("**💡 Recommended Actions:**")
                for action in severity.recommendations:
                    st.markdown(f"- {action}")
            
            # Emergency warning
            if severity.level == "Emergency":
                st.error("🚨 **EMERGENCY: CALL AMBULANCE IMMEDIATELY (911/112/108)**")
                st.error("Do not wait or drive yourself. Time is critical.")
            
            st.divider()
            
            # Multi-disease analysis
            if results.get('disease_analysis'):
                st.subheader("🔍 Multi-Disease Analysis")
                disease_analysis = results['disease_analysis']
                
                if disease_analysis.get('has_multiple_conditions'):
                    st.warning("⚠️ **Possible Comorbidities Detected**")
                    st.markdown(f"Confidence gap: {disease_analysis['confidence_gap']:.1f}%")
                    
                    for comorbidity in disease_analysis['comorbidities']:
                        st.markdown(f"- **{comorbidity['disease']}**: {comorbidity['confidence']*100:.1f}%")
                else:
                    st.success("✅ Single condition likely")
                
                # Show chart
                display_multi_disease_chart(disease_analysis)
            
            st.divider()
            
            # Personalized recommendations
            if results.get('recommendations') and patient_profile:
                st.subheader("👤 Personalized Safety Recommendations")
                display_personalized_warnings(results['recommendations'])
                
                # Lifestyle advice
                lifestyle = results['recommendations'].get('lifestyle_advice', [])
                if lifestyle:
                    with st.expander("💡 Lifestyle Advice", expanded=False):
                        for advice in lifestyle:
                            st.markdown(f"- {advice}")
        
        # Basic recommendations section
        st.divider()
        st.header("💊 Treatment Recommendations")
        
        tab1, tab2, tab3 = st.tabs(["🌿 Herbal", "💊 Pharmaceutical", "🤖 AI Insights"])
        
        with tab1:
            ingredients = response.get('herbal_recommendations', [])
            display_herbal_recommendations(ingredients)
        
        with tab2:
            medications = response.get('drug_recommendations', [])
            display_pharmaceutical_recommendations(medications)
        
        with tab3:
            ai_insights = response.get('ai_insights', 'No AI insights available.')
            st.markdown(ai_insights)
        
        # Comparison
        with st.expander("🔄 Herbal vs Pharmaceutical Comparison", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🌿 Herbal")
                st.markdown("""
                - ✓ Natural ingredients
                - ✓ Fewer synthetic additives
                - ✓ Milder with fewer side effects
                - ✓ Long-term preventive care
                - ✗ Slower acting
                - ✗ Quality varies by brand
                """)
            
            with col2:
                st.markdown("### 💊 Pharmaceutical")
                st.markdown("""
                - ✓ Clinically proven
                - ✓ Faster symptom relief
                - ✓ Precise dosing
                - ✓ Well-researched effects
                - ✗ More pronounced side effects
                - ✗ May require prescription
                """)
        
        # Low confidence warning
        if confidence < 0.5:
            st.warning(f"""
            ⚠️ **LOW CONFIDENCE WARNING**
            
            The system's confidence in this diagnosis is LOW ({confidence*100:.1f}%).
            
            This could mean:
            - Your symptoms don't clearly match a known condition
            - The description is too vague or incomplete
            - You may have a rare or complex condition
            
            **RECOMMENDATION**: Consult a healthcare professional for proper diagnosis.
            """)
        
        # Medical disclaimer
        st.divider()
        st.error("""
        ⚠️ **MEDICAL DISCLAIMER**
        
        This is an AI-powered informational tool only.
        
        - Always consult a qualified healthcare professional
        - Do not use for diagnosis or treatment decisions
        - Herbal remedies can interact with medications
        - Individual results may vary
        - If symptoms persist or worsen, seek immediate medical care
        
        This tool does NOT replace professional medical advice, diagnosis, or treatment.
        """)
        
        # Feedback collection
        if st.session_state.feedback_system:
            st.divider()
            st.subheader("📊 Help Us Improve!")
            st.write("Was this prediction helpful?")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("👍 Helpful", use_container_width=True):
                    st.session_state.feedback_system.record_feedback(
                        symptoms=st.session_state.get('last_symptoms', ''),
                        predicted_disease=disease,
                        confidence=confidence,
                        helpful=True
                    )
                    st.success("Thank you for your feedback!")
            
            with col2:
                if st.button("👎 Not Helpful", use_container_width=True):
                    st.session_state.show_feedback = True
            
            # Extended feedback form
            if st.session_state.show_feedback:
                with st.expander("📝 Tell us more (optional)", expanded=True):
                    actual = st.text_input("What did your doctor diagnose?")
                    rating = st.slider("Rate accuracy (1-5 stars)", 1, 5, 3)
                    comments = st.text_area("Additional comments")
                    
                    if st.button("Submit Feedback"):
                        st.session_state.feedback_system.record_feedback(
                            symptoms=st.session_state.get('last_symptoms', ''),
                            predicted_disease=disease,
                            confidence=confidence,
                            helpful=False,
                            rating=rating,
                            actual_diagnosis=actual if actual else None,
                            comments=comments if comments else None
                        )
                        st.success("✅ Thank you! Your feedback helps improve the system.")
                        st.session_state.show_feedback = False
    
    # Footer with helpful information
    st.divider()
    with st.expander("ℹ️ About Cure-Blend", expanded=False):
        st.markdown("""
        ### 🏥 Cure-Blend - AI-Powered Health Recommendation System
        
        **Features:**
        - 🔍 Multi-disease detection with comorbidity analysis
        - 📊 Severity classification (0-100 scoring)
        - 👤 Personalized recommendations for special populations
        - 🌿 Herbal remedy suggestions
        - 💊 Pharmaceutical medication recommendations
        - 🤖 AI-powered insights and explanations
        
        **How to Use:**
        1. Describe your symptoms in detail
        2. (Optional) Create a patient profile for personalized recommendations
        3. Click "Analyze Symptoms" to get recommendations
        4. Review both herbal and pharmaceutical options
        5. Provide feedback to help improve the system
        
        **Important:**
        - This is an informational tool only
        - Always consult a healthcare professional
        - Do not use for emergency situations
        - Report serious symptoms to medical services immediately
        
        **Version:** 2.0 | **Last Updated:** December 2025
        """)
    
    # Quick help section
    with st.expander("❓ Need Help?", expanded=False):
        st.markdown("""
        **Common Issues:**
        
        **Q: The system says "Low Confidence"**
        - Try describing symptoms in more detail
        - Mention duration, intensity, and location
        - Include any recent events (travel, food, exposure)
        
        **Q: I want to enable advanced features**
        - Check the sidebar for "Enable Advanced Features"
        - If disabled, some dependencies may be missing
        
        **Q: How do I create a patient profile?**
        - Enable "Personalized Recommendations" in the sidebar
        - Fill in age, gender, and medical conditions
        - This helps identify contraindications
        
        **Q: Are the recommendations safe?**
        - Recommendations are informational only
        - Always verify with a healthcare provider
        - Check for allergies and drug interactions
        - Follow prescribed medications first
        """)

if __name__ == "__main__":
    # Show startup information
    if 'app_started' not in st.session_state:
        st.session_state.app_started = True
        
        # Display startup banner
        st.info("""
        ### 🚀 Welcome to Cure-Blend!
        
        **System Loading...**
        - Core modules: Loading...
        - Advanced features: Checking...
        - Knowledge base: Preparing...
        """)
    
    main()