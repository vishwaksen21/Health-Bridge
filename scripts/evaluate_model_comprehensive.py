#!/usr/bin/env python3
"""
Comprehensive Model Evaluation Script - Week 3 Improvement
Provides detailed metrics, per-disease performance, calibration analysis, and confusion matrix
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    log_loss
)
from sklearn.calibration import calibration_curve
from sklearn.model_selection import train_test_split
import os
import json
from datetime import datetime

class ComprehensiveModelEvaluator:
    """
    Complete evaluation suite for symptom prediction model
    """
    
    def __init__(self, model_path='data/symptom_model.pkl', data_path='data/symptom_disease_augmented.csv'):
        """Initialize evaluator with model and data paths"""
        self.model_path = model_path
        self.data_path = data_path
        self.results = {}
        
        print(f"📂 Loading model and data...")
        self.vectorizer, self.model = joblib.load(model_path)
        self.df = pd.read_csv(data_path)
        print(f"✅ Loaded: {len(self.model.classes_)} diseases, {len(self.df)} samples")
        
    def prepare_data(self, test_size=0.2, random_state=42):
        """Split data into train/test sets"""
        print(f"\n🔀 Splitting data: {int((1-test_size)*100)}% train, {int(test_size*100)}% test")
        
        import sys
        sys.path.insert(0, os.path.abspath('.'))
        from src.symptom_predictor import clean_text
        
        # Clean text
        X = self.df['symptom_text'].apply(clean_text).tolist()
        y = self.df['disease'].tolist()
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Vectorize
        X_train_vec = self.vectorizer.transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.X_test_vec = X_test_vec
        
        print(f"   Train: {len(X_train)} samples")
        print(f"   Test:  {len(X_test)} samples")
        
        return X_test_vec, y_test
    
    def evaluate_overall_metrics(self):
        """Calculate overall model performance"""
        print(f"\n{'='*70}")
        print(f"📊 OVERALL MODEL PERFORMANCE")
        print(f"{'='*70}")
        
        # Predictions
        y_pred = self.model.predict(self.X_test_vec)
        y_proba = self.model.predict_proba(self.X_test_vec)
        y_proba_max = y_proba.max(axis=1)
        
        # Accuracy
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"\n✅ Overall Accuracy: {accuracy*100:.2f}%")
        
        # Macro and weighted metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            self.y_test, y_pred, average=None, zero_division=0
        )
        
        macro_f1 = f1.mean()
        weighted_f1 = np.average(f1, weights=support)
        
        print(f"   Macro-averaged F1:    {macro_f1:.3f}")
        print(f"   Weighted-averaged F1: {weighted_f1:.3f}")
        
        # Log loss (calibration metric)
        logloss = log_loss(self.y_test, y_proba)
        print(f"   Log Loss:             {logloss:.3f} (lower is better)")
        
        # Confidence distribution
        print(f"\n📈 Confidence Distribution:")
        high_conf = np.sum(y_proba_max > 0.75)
        med_conf = np.sum((y_proba_max >= 0.45) & (y_proba_max <= 0.75))
        low_conf = np.sum(y_proba_max < 0.45)
        
        print(f"   High (>75%):      {high_conf:4d} predictions ({high_conf/len(y_pred)*100:5.1f}%)")
        print(f"   Moderate (45-75%): {med_conf:4d} predictions ({med_conf/len(y_pred)*100:5.1f}%)")
        print(f"   Low (<45%):       {low_conf:4d} predictions ({low_conf/len(y_pred)*100:5.1f}%)")
        
        self.results['overall'] = {
            'accuracy': float(accuracy),
            'macro_f1': float(macro_f1),
            'weighted_f1': float(weighted_f1),
            'log_loss': float(logloss),
            'high_confidence_pct': float(high_conf/len(y_pred)),
            'low_confidence_pct': float(low_conf/len(y_pred))
        }
        
        return y_pred, y_proba, y_proba_max
    
    def evaluate_per_disease_performance(self, y_pred):
        """Detailed per-disease metrics"""
        print(f"\n{'='*70}")
        print(f"🎯 PER-DISEASE PERFORMANCE")
        print(f"{'='*70}")
        
        # Calculate per-class metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            self.y_test, y_pred, average=None, zero_division=0
        )
        
        # Create DataFrame
        disease_names = self.model.classes_
        report_df = pd.DataFrame({
            'Disease': disease_names,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'Support': support
        })
        
        # Sort by F1 score
        report_df = report_df.sort_values('F1-Score', ascending=False)
        
        print(f"\n📋 Top 15 Best Performing Diseases:")
        print(report_df.head(15).to_string(index=False))
        
        # Identify poor performers
        poor_performers = report_df[report_df['F1-Score'] < 0.6]
        if len(poor_performers) > 0:
            print(f"\n⚠️  {len(poor_performers)} diseases with F1 < 0.6 (need attention):")
            print(poor_performers.to_string(index=False))
        else:
            print(f"\n✅ All diseases have F1-Score >= 0.6!")
        
        # Save full report
        report_path = 'data/per_disease_performance.csv'
        report_df.to_csv(report_path, index=False)
        print(f"\n💾 Full report saved to: {report_path}")
        
        self.results['per_disease'] = report_df.to_dict('records')
        
        return report_df
    
    def evaluate_calibration(self, y_proba):
        """Check probability calibration quality"""
        print(f"\n{'='*70}")
        print(f"📐 PROBABILITY CALIBRATION ANALYSIS")
        print(f"{'='*70}")
        
        # For multi-class, we need to binarize
        # Use One-vs-Rest approach for top 5 most common diseases
        from sklearn.preprocessing import label_binarize
        
        disease_counts = pd.Series(self.y_test).value_counts()
        top_diseases = disease_counts.head(5).index.tolist()
        
        print(f"\n🔍 Analyzing calibration for top 5 diseases:")
        
        calibration_results = []
        
        for disease in top_diseases:
            # Binarize: this disease vs rest
            y_binary = [1 if y == disease else 0 for y in self.y_test]
            
            # Get probabilities for this disease
            disease_idx = list(self.model.classes_).index(disease)
            y_prob_disease = y_proba[:, disease_idx]
            
            # Calculate calibration curve
            try:
                prob_true, prob_pred = calibration_curve(
                    y_binary, y_prob_disease, n_bins=5, strategy='uniform'
                )
                
                # Calculate calibration error
                calibration_error = np.abs(prob_true - prob_pred).mean()
                
                print(f"\n   {disease}:")
                print(f"      Avg Calibration Error: {calibration_error:.3f}")
                for true_p, pred_p in zip(prob_true, prob_pred):
                    diff = abs(true_p - pred_p)
                    status = "✅" if diff < 0.1 else "⚠️"
                    print(f"      {status} Predicted {pred_p:.2f} → Actual {true_p:.2f} (diff: {diff:.3f})")
                
                calibration_results.append({
                    'disease': disease,
                    'calibration_error': float(calibration_error)
                })
            except:
                print(f"   {disease}: Not enough samples for calibration curve")
        
        # Overall assessment
        avg_calibration_error = np.mean([r['calibration_error'] for r in calibration_results])
        print(f"\n📊 Average Calibration Error: {avg_calibration_error:.3f}")
        
        if avg_calibration_error < 0.1:
            print(f"   ✅ Excellent calibration!")
        elif avg_calibration_error < 0.15:
            print(f"   🟡 Good calibration")
        else:
            print(f"   ⚠️  Calibration needs improvement")
        
        self.results['calibration'] = {
            'avg_error': float(avg_calibration_error),
            'per_disease': calibration_results
        }
    
    def generate_confusion_matrix(self, y_pred):
        """Create confusion matrix for common diseases"""
        print(f"\n{'='*70}")
        print(f"🔲 CONFUSION MATRIX (Top 10 Diseases)")
        print(f"{'='*70}")
        
        # Get top 10 most common diseases
        disease_counts = pd.Series(self.y_test).value_counts()
        top_10 = disease_counts.head(10).index.tolist()
        
        # Filter to top 10
        mask = [y in top_10 for y in self.y_test]
        y_test_filtered = [y for y, m in zip(self.y_test, mask) if m]
        y_pred_filtered = [y for y, m in zip(y_pred, mask) if m]
        
        # Compute confusion matrix
        cm = confusion_matrix(y_test_filtered, y_pred_filtered, labels=top_10)
        
        # Calculate accuracy per disease
        print(f"\n📊 Accuracy for Top 10 Diseases:")
        for i, disease in enumerate(top_10):
            disease_accuracy = cm[i, i] / cm[i, :].sum() if cm[i, :].sum() > 0 else 0
            support = cm[i, :].sum()
            status = "✅" if disease_accuracy >= 0.8 else "⚠️" if disease_accuracy >= 0.6 else "❌"
            print(f"   {status} {disease:<30s} {disease_accuracy*100:5.1f}% ({support:3.0f} samples)")
        
        # Save confusion matrix as CSV
        cm_df = pd.DataFrame(cm, index=top_10, columns=top_10)
        cm_path = 'data/confusion_matrix_top10.csv'
        cm_df.to_csv(cm_path)
        print(f"\n💾 Confusion matrix saved to: {cm_path}")
    
    def test_emergency_detection(self):
        """Test emergency condition detection accuracy"""
        print(f"\n{'='*70}")
        print(f"🚨 EMERGENCY CONDITION DETECTION")
        print(f"{'='*70}")
        
        emergency_diseases = [
            'Heart Attack', 'Stroke', 'Sepsis', 'Meningitis', 
            'Anaphylaxis', 'Appendicitis'
        ]
        
        # Filter test set to emergency conditions
        emergency_mask = [y in emergency_diseases for y in self.y_test]
        if not any(emergency_mask):
            print("\n⚠️  No emergency conditions in test set")
            return
        
        y_test_emergency = [y for y, m in zip(self.y_test, emergency_mask) if m]
        X_test_emergency = self.X_test_vec[emergency_mask]
        
        # Predict
        y_pred_emergency = self.model.predict(X_test_emergency)
        y_proba_emergency = self.model.predict_proba(X_test_emergency).max(axis=1)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test_emergency, y_pred_emergency)
        avg_confidence = y_proba_emergency.mean()
        
        print(f"\n📊 Emergency Condition Performance:")
        print(f"   Test samples:     {len(y_test_emergency)}")
        print(f"   Accuracy:         {accuracy*100:.2f}%")
        print(f"   Avg Confidence:   {avg_confidence*100:.2f}%")
        
        # Per emergency disease
        print(f"\n🎯 Per Emergency Disease:")
        for disease in emergency_diseases:
            mask = [y == disease for y in y_test_emergency]
            if not any(mask):
                continue
            
            disease_pred = [p for p, m in zip(y_pred_emergency, mask) if m]
            disease_true = [t for t, m in zip(y_test_emergency, mask) if m]
            disease_acc = accuracy_score(disease_true, disease_pred)
            
            status = "✅" if disease_acc >= 0.8 else "⚠️"
            print(f"   {status} {disease:<25s} {disease_acc*100:5.1f}% ({sum(mask):2d} samples)")
        
        self.results['emergency'] = {
            'accuracy': float(accuracy),
            'avg_confidence': float(avg_confidence),
            'sample_count': len(y_test_emergency)
        }
    
    def save_results(self):
        """Save evaluation results to JSON"""
        output_path = 'data/evaluation_report.json'
        
        # Add metadata
        self.results['metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'model_path': self.model_path,
            'data_path': self.data_path,
            'total_diseases': len(self.model.classes_),
            'total_samples': len(self.df),
            'test_samples': len(self.y_test)
        }
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Full evaluation report saved to: {output_path}")
    
    def generate_summary(self):
        """Print executive summary"""
        print(f"\n{'='*70}")
        print(f"📋 EVALUATION SUMMARY")
        print(f"{'='*70}")
        
        overall = self.results['overall']
        
        print(f"\n✅ Model Coverage: {len(self.model.classes_)} diseases")
        print(f"✅ Overall Accuracy: {overall['accuracy']*100:.2f}%")
        print(f"✅ Macro F1-Score: {overall['macro_f1']:.3f}")
        print(f"✅ Weighted F1-Score: {overall['weighted_f1']:.3f}")
        
        if 'emergency' in self.results:
            print(f"✅ Emergency Detection Accuracy: {self.results['emergency']['accuracy']*100:.2f}%")
        
        print(f"\n🎯 Confidence Distribution:")
        print(f"   High confidence (>75%):   {overall['high_confidence_pct']*100:.1f}%")
        print(f"   Low confidence (<45%):    {overall['low_confidence_pct']*100:.1f}%")
        
        if 'calibration' in self.results:
            print(f"\n📐 Calibration:")
            print(f"   Avg calibration error: {self.results['calibration']['avg_error']:.3f}")
        
        print(f"\n{'='*70}")
        print(f"✅ Week 3 Evaluation Complete!")
        print(f"{'='*70}\n")


def main():
    """Run comprehensive evaluation"""
    print("\n" + "="*70)
    print("🔬 COMPREHENSIVE MODEL EVALUATION - Week 3")
    print("="*70)
    
    # Initialize evaluator
    evaluator = ComprehensiveModelEvaluator()
    
    # Prepare data
    evaluator.prepare_data(test_size=0.2)
    
    # Run evaluations
    y_pred, y_proba, y_proba_max = evaluator.evaluate_overall_metrics()
    evaluator.evaluate_per_disease_performance(y_pred)
    evaluator.evaluate_calibration(y_proba)
    evaluator.generate_confusion_matrix(y_pred)
    evaluator.test_emergency_detection()
    
    # Save and summarize
    evaluator.save_results()
    evaluator.generate_summary()


if __name__ == '__main__':
    main()
