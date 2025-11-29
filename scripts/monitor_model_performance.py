#!/usr/bin/env python3
"""
Model Performance Monitoring System - Week 3 Improvement
Logs predictions, tracks performance over time, and generates analytics
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from collections import Counter, defaultdict
import pandas as pd


class ModelPerformanceMonitor:
    """
    Continuous monitoring system for symptom prediction model
    Logs predictions, user feedback, and generates performance reports
    """
    
    def __init__(self, log_file: str = "data/model_performance_log.json"):
        """Initialize monitor with log file path"""
        self.log_file = log_file
        self.history = []
        self.load_history()
    
    def log_prediction(
        self, 
        user_input: str, 
        predicted_disease: str, 
        confidence: float,
        method: str = "ml_model",
        feedback: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Log a single prediction
        
        Args:
            user_input: User's symptom description
            predicted_disease: Model's prediction
            confidence: Confidence score (0-1)
            method: Prediction method (ml_model, pattern_match, fallback)
            feedback: User feedback (correct/incorrect/unknown)
            metadata: Additional information (response_time, etc.)
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'input': user_input,
            'prediction': predicted_disease,
            'confidence': float(confidence),
            'method': method,
            'feedback': feedback
        }
        
        if metadata:
            entry['metadata'] = metadata
        
        self.history.append(entry)
        self.save_history()
    
    def add_feedback(self, prediction_id: int, feedback: str, correct_disease: Optional[str] = None):
        """
        Add user feedback to a prediction
        
        Args:
            prediction_id: Index of prediction in history
            feedback: User feedback (correct/incorrect)
            correct_disease: If incorrect, what was the actual disease
        """
        if 0 <= prediction_id < len(self.history):
            self.history[prediction_id]['feedback'] = feedback
            if correct_disease:
                self.history[prediction_id]['correct_disease'] = correct_disease
            self.save_history()
            return True
        return False
    
    def get_overall_stats(self) -> Dict:
        """Get overall performance statistics"""
        if not self.history:
            return {'error': 'No data logged yet'}
        
        total = len(self.history)
        
        # Count by feedback type
        with_feedback = [h for h in self.history if h.get('feedback')]
        correct = sum(1 for h in with_feedback if h['feedback'] == 'correct')
        incorrect = sum(1 for h in with_feedback if h['feedback'] == 'incorrect')
        
        # User-reported accuracy
        user_accuracy = correct / len(with_feedback) if with_feedback else None
        
        # Average confidence
        avg_confidence = sum(h['confidence'] for h in self.history) / total
        
        # Confidence by correctness
        correct_preds = [h for h in with_feedback if h['feedback'] == 'correct']
        incorrect_preds = [h for h in with_feedback if h['feedback'] == 'incorrect']
        
        avg_conf_correct = sum(h['confidence'] for h in correct_preds) / len(correct_preds) if correct_preds else None
        avg_conf_incorrect = sum(h['confidence'] for h in incorrect_preds) / len(incorrect_preds) if incorrect_preds else None
        
        # Method distribution
        methods = Counter(h['method'] for h in self.history)
        
        return {
            'total_predictions': total,
            'with_feedback': len(with_feedback),
            'user_reported_accuracy': user_accuracy,
            'correct_predictions': correct,
            'incorrect_predictions': incorrect,
            'avg_confidence': avg_confidence,
            'avg_confidence_correct': avg_conf_correct,
            'avg_confidence_incorrect': avg_conf_incorrect,
            'methods': dict(methods)
        }
    
    def get_disease_stats(self) -> pd.DataFrame:
        """Get per-disease prediction statistics"""
        if not self.history:
            return pd.DataFrame()
        
        disease_data = defaultdict(lambda: {
            'count': 0,
            'avg_confidence': [],
            'correct': 0,
            'incorrect': 0
        })
        
        for entry in self.history:
            disease = entry['prediction']
            disease_data[disease]['count'] += 1
            disease_data[disease]['avg_confidence'].append(entry['confidence'])
            
            if entry.get('feedback') == 'correct':
                disease_data[disease]['correct'] += 1
            elif entry.get('feedback') == 'incorrect':
                disease_data[disease]['incorrect'] += 1
        
        # Convert to DataFrame
        rows = []
        for disease, stats in disease_data.items():
            with_feedback = stats['correct'] + stats['incorrect']
            accuracy = stats['correct'] / with_feedback if with_feedback > 0 else None
            
            rows.append({
                'Disease': disease,
                'Predictions': stats['count'],
                'Avg_Confidence': sum(stats['avg_confidence']) / len(stats['avg_confidence']),
                'With_Feedback': with_feedback,
                'Correct': stats['correct'],
                'Incorrect': stats['incorrect'],
                'User_Accuracy': accuracy
            })
        
        df = pd.DataFrame(rows)
        df = df.sort_values('Predictions', ascending=False)
        return df
    
    def get_time_series_stats(self, days: int = 7) -> Dict:
        """Get statistics for recent time period"""
        if not self.history:
            return {'error': 'No data logged yet'}
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent = [
            h for h in self.history 
            if datetime.fromisoformat(h['timestamp']) > cutoff_date
        ]
        
        if not recent:
            return {'error': f'No predictions in last {days} days'}
        
        daily_counts = defaultdict(int)
        for entry in recent:
            date = datetime.fromisoformat(entry['timestamp']).date()
            daily_counts[str(date)] += 1
        
        return {
            'period_days': days,
            'total_predictions': len(recent),
            'avg_per_day': len(recent) / days,
            'daily_breakdown': dict(daily_counts)
        }
    
    def identify_problem_areas(self) -> Dict:
        """Identify diseases with poor performance"""
        disease_stats = self.get_disease_stats()
        
        if disease_stats.empty:
            return {'error': 'No data available'}
        
        # Filter diseases with feedback
        with_feedback = disease_stats[disease_stats['With_Feedback'] >= 3]
        
        if with_feedback.empty:
            return {'message': 'Not enough feedback data yet'}
        
        # Low accuracy diseases
        low_accuracy = with_feedback[
            with_feedback['User_Accuracy'] < 0.7
        ].sort_values('User_Accuracy')
        
        # Low confidence predictions
        low_confidence = disease_stats[
            disease_stats['Avg_Confidence'] < 0.5
        ].sort_values('Avg_Confidence')
        
        # High volume, low accuracy
        high_volume_low_acc = with_feedback[
            (with_feedback['Predictions'] >= 5) & 
            (with_feedback['User_Accuracy'] < 0.8)
        ].sort_values('User_Accuracy')
        
        return {
            'low_accuracy_diseases': low_accuracy.to_dict('records'),
            'low_confidence_diseases': low_confidence.head(10).to_dict('records'),
            'high_volume_issues': high_volume_low_acc.to_dict('records')
        }
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate comprehensive monitoring report"""
        report = []
        report.append("="*70)
        report.append("📊 MODEL PERFORMANCE MONITORING REPORT")
        report.append("="*70)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Overall stats
        overall = self.get_overall_stats()
        if 'error' not in overall:
            report.append(f"\n📈 OVERALL STATISTICS")
            report.append(f"   Total Predictions: {overall['total_predictions']}")
            report.append(f"   With Feedback: {overall['with_feedback']}")
            
            if overall['user_reported_accuracy'] is not None:
                report.append(f"   User-Reported Accuracy: {overall['user_reported_accuracy']*100:.2f}%")
                report.append(f"   Correct: {overall['correct_predictions']}")
                report.append(f"   Incorrect: {overall['incorrect_predictions']}")
            
            report.append(f"\n   Average Confidence: {overall['avg_confidence']:.3f}")
            if overall['avg_confidence_correct']:
                report.append(f"   Avg Confidence (Correct): {overall['avg_confidence_correct']:.3f}")
            if overall['avg_confidence_incorrect']:
                report.append(f"   Avg Confidence (Incorrect): {overall['avg_confidence_incorrect']:.3f}")
            
            report.append(f"\n   Prediction Methods:")
            for method, count in overall['methods'].items():
                pct = count / overall['total_predictions'] * 100
                report.append(f"      {method}: {count} ({pct:.1f}%)")
        
        # Disease stats
        disease_stats = self.get_disease_stats()
        if not disease_stats.empty:
            report.append(f"\n📋 TOP 10 MOST PREDICTED DISEASES")
            for _, row in disease_stats.head(10).iterrows():
                report.append(
                    f"   {row['Disease']:<30s} {row['Predictions']:3d} predictions, "
                    f"Avg Conf: {row['Avg_Confidence']:.2f}"
                )
                if row['User_Accuracy'] is not None:
                    report.append(f"      → User Accuracy: {row['User_Accuracy']*100:.1f}%")
        
        # Problem areas
        problems = self.identify_problem_areas()
        if 'low_accuracy_diseases' in problems and problems['low_accuracy_diseases']:
            report.append(f"\n⚠️  ATTENTION NEEDED - Low Accuracy Diseases")
            for disease_info in problems['low_accuracy_diseases'][:5]:
                report.append(
                    f"   {disease_info['Disease']:<30s} "
                    f"Accuracy: {disease_info['User_Accuracy']*100:.1f}% "
                    f"({disease_info['Correct']}/{disease_info['With_Feedback']})"
                )
        
        # Time series
        time_stats = self.get_time_series_stats(days=7)
        if 'error' not in time_stats:
            report.append(f"\n📅 LAST 7 DAYS")
            report.append(f"   Total Predictions: {time_stats['total_predictions']}")
            report.append(f"   Average per Day: {time_stats['avg_per_day']:.1f}")
        
        report.append("\n" + "="*70)
        
        report_text = "\n".join(report)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
        
        return report_text
    
    def load_history(self):
        """Load prediction history from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️  Warning: Could not load {self.log_file}, starting fresh")
                self.history = []
        else:
            self.history = []
    
    def save_history(self):
        """Save prediction history to file"""
        os.makedirs(os.path.dirname(self.log_file) if os.path.dirname(self.log_file) else '.', exist_ok=True)
        with open(self.log_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def export_to_csv(self, output_path: str = "data/prediction_log.csv"):
        """Export history to CSV for analysis"""
        if not self.history:
            print("No data to export")
            return
        
        df = pd.DataFrame(self.history)
        df.to_csv(output_path, index=False)
        print(f"✅ Exported {len(df)} predictions to {output_path}")


# Example usage
if __name__ == '__main__':
    monitor = ModelPerformanceMonitor()
    
    # Simulate some predictions
    print("📝 Simulating predictions for demonstration...")
    
    test_predictions = [
        ("fever and headache", "Influenza", 0.85, "ml_model"),
        ("chest pain radiating to arm", "Heart Attack", 0.92, "ml_model"),
        ("severe back pain with blood in urine", "Kidney Stones", 0.88, "ml_model"),
        ("feeling very tired all the time", "Chronic Fatigue Syndrome", 0.45, "ml_model"),
        ("sharp pain in lower right abdomen", "Appendicitis", 0.79, "ml_model"),
    ]
    
    for inp, pred, conf, method in test_predictions:
        monitor.log_prediction(inp, pred, conf, method)
    
    print(f"✅ Logged {len(test_predictions)} predictions")
    
    # Generate report
    print("\n" + monitor.generate_report())
    
    # Export to CSV
    monitor.export_to_csv()
