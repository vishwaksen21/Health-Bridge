#!/usr/bin/env python3
"""
Herbal Safety Checker - Week 3 Improvement
Checks for contraindications, drug interactions, and safety warnings for herbal remedies
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SafetyWarning:
    """Structure for safety warnings"""
    severity: str  # "CRITICAL", "WARNING", "INFO"
    category: str  # "contraindication", "interaction", "precaution"
    message: str
    source: str = "Safety Database"


class HerbalSafetyChecker:
    """
    Comprehensive safety checking system for herbal remedies
    Includes contraindications, drug interactions, and patient-specific warnings
    """
    
    def __init__(self):
        """Initialize safety database"""
        self.contraindications = self._load_contraindications()
        self.drug_interactions = self._load_drug_interactions()
        self.herb_interactions = self._load_herb_interactions()
        self.pregnancy_safety = self._load_pregnancy_safety()
        self.dosage_limits = self._load_dosage_limits()
    
    def check_herb_safety(
        self, 
        herb_name: str, 
        patient_conditions: List[str] = None,
        current_medications: List[str] = None,
        is_pregnant: bool = False,
        is_breastfeeding: bool = False
    ) -> List[SafetyWarning]:
        """
        Comprehensive safety check for a single herb
        
        Args:
            herb_name: Name of the herb/ingredient
            patient_conditions: List of patient's medical conditions
            current_medications: List of medications patient is taking
            is_pregnant: Whether patient is pregnant
            is_breastfeeding: Whether patient is breastfeeding
            
        Returns:
            List of SafetyWarning objects
        """
        warnings = []
        herb_lower = herb_name.lower()
        
        # Check contraindications
        if patient_conditions:
            for condition in patient_conditions:
                condition_lower = condition.lower()
                if (herb_lower, condition_lower) in self.contraindications:
                    warnings.append(SafetyWarning(
                        severity="WARNING",
                        category="contraindication",
                        message=f"⚠️  {herb_name} may not be suitable for {condition}: {self.contraindications[(herb_lower, condition_lower)]}"
                    ))
        
        # Check drug interactions
        if current_medications:
            for medication in current_medications:
                med_lower = medication.lower()
                if (herb_lower, med_lower) in self.drug_interactions:
                    warnings.append(SafetyWarning(
                        severity="CRITICAL",
                        category="interaction",
                        message=f"🚨 {herb_name} may interact with {medication}: {self.drug_interactions[(herb_lower, med_lower)]}"
                    ))
        
        # Check pregnancy safety
        if is_pregnant and herb_lower in self.pregnancy_safety:
            safety_info = self.pregnancy_safety[herb_lower]
            if safety_info['safe'] == False:
                warnings.append(SafetyWarning(
                    severity="CRITICAL",
                    category="pregnancy",
                    message=f"🚨 {herb_name} is NOT SAFE during pregnancy: {safety_info['reason']}"
                ))
            elif safety_info['safe'] == 'caution':
                warnings.append(SafetyWarning(
                    severity="WARNING",
                    category="pregnancy",
                    message=f"⚠️  Use {herb_name} with caution during pregnancy: {safety_info['reason']}"
                ))
        
        # Check dosage information
        if herb_lower in self.dosage_limits:
            dosage_info = self.dosage_limits[herb_lower]
            warnings.append(SafetyWarning(
                severity="INFO",
                category="dosage",
                message=f"ℹ️  {herb_name} dosage: {dosage_info['recommended']}. Max: {dosage_info['maximum']}"
            ))
        
        return warnings
    
    def check_herb_combination(
        self, 
        herbs: List[str]
    ) -> List[SafetyWarning]:
        """
        Check for dangerous herb-herb interactions
        
        Args:
            herbs: List of herb names to check
            
        Returns:
            List of SafetyWarning objects
        """
        warnings = []
        
        # Check all pairs
        for i, herb1 in enumerate(herbs):
            for herb2 in herbs[i+1:]:
                herb1_lower = herb1.lower()
                herb2_lower = herb2.lower()
                
                # Check both orderings
                if (herb1_lower, herb2_lower) in self.herb_interactions:
                    interaction = self.herb_interactions[(herb1_lower, herb2_lower)]
                    warnings.append(SafetyWarning(
                        severity=interaction['severity'],
                        category="herb_interaction",
                        message=f"⚠️  {herb1} + {herb2}: {interaction['effect']}"
                    ))
                elif (herb2_lower, herb1_lower) in self.herb_interactions:
                    interaction = self.herb_interactions[(herb2_lower, herb1_lower)]
                    warnings.append(SafetyWarning(
                        severity=interaction['severity'],
                        category="herb_interaction",
                        message=f"⚠️  {herb1} + {herb2}: {interaction['effect']}"
                    ))
        
        return warnings
    
    def get_comprehensive_safety_report(
        self,
        herbs: List[str],
        patient_conditions: List[str] = None,
        current_medications: List[str] = None,
        is_pregnant: bool = False,
        is_breastfeeding: bool = False
    ) -> Dict:
        """
        Generate comprehensive safety report for multiple herbs
        
        Returns:
            Dict with warnings categorized by severity and type
        """
        all_warnings = []
        
        # Check each herb individually
        for herb in herbs:
            herb_warnings = self.check_herb_safety(
                herb, patient_conditions, current_medications, 
                is_pregnant, is_breastfeeding
            )
            all_warnings.extend(herb_warnings)
        
        # Check herb combinations
        if len(herbs) > 1:
            combination_warnings = self.check_herb_combination(herbs)
            all_warnings.extend(combination_warnings)
        
        # Categorize warnings
        critical = [w for w in all_warnings if w.severity == "CRITICAL"]
        warnings_list = [w for w in all_warnings if w.severity == "WARNING"]
        info = [w for w in all_warnings if w.severity == "INFO"]
        
        return {
            'safe_to_use': len(critical) == 0,
            'total_warnings': len(all_warnings),
            'critical': critical,
            'warnings': warnings_list,
            'info': info,
            'summary': self._generate_summary(critical, warnings_list, info)
        }
    
    def _generate_summary(self, critical, warnings, info) -> str:
        """Generate human-readable summary"""
        if critical:
            return f"🚨 CRITICAL: {len(critical)} serious safety concerns detected. Do NOT use without medical supervision."
        elif warnings:
            return f"⚠️  {len(warnings)} safety warnings found. Use with caution and consult healthcare provider."
        elif info:
            return f"✅ Generally safe. {len(info)} informational notes provided."
        else:
            return "✅ No safety concerns identified. Still recommend consulting healthcare provider."
    
    def _load_contraindications(self) -> Dict[Tuple[str, str], str]:
        """Load herb-condition contraindications database"""
        return {
            ('curcumin', 'blood clotting disorder'): "May increase bleeding risk",
            ('curcumin', 'gallbladder disease'): "May worsen gallbladder problems",
            ('ginger', 'bleeding disorder'): "May increase bleeding risk",
            ('ginger', 'heart condition'): "High doses may affect heart rhythm",
            ('licorice', 'hypertension'): "May raise blood pressure",
            ('licorice', 'heart disease'): "May cause fluid retention and worsen heart problems",
            ('licorice', 'kidney disease'): "May worsen kidney function",
            ('garlic', 'bleeding disorder'): "May increase bleeding risk",
            ('ginkgo', 'epilepsy'): "May increase seizure risk",
            ('ginkgo', 'bleeding disorder'): "May increase bleeding risk",
            ('st john\'s wort', 'depression'): "May interact with antidepressants",
            ('st john\'s wort', 'bipolar disorder'): "May trigger mania",
            ('valerian', 'liver disease'): "May affect liver function",
            ('echinacea', 'autoimmune disease'): "May stimulate immune system inappropriately",
            ('ashwagandha', 'hyperthyroidism'): "May increase thyroid hormone levels",
            ('ashwagandha', 'autoimmune disease'): "May stimulate immune system",
        }
    
    def _load_drug_interactions(self) -> Dict[Tuple[str, str], str]:
        """Load herb-drug interactions database"""
        return {
            ('curcumin', 'warfarin'): "May increase bleeding risk when combined with blood thinners",
            ('curcumin', 'aspirin'): "May increase bleeding risk",
            ('ginger', 'warfarin'): "May increase bleeding risk",
            ('ginger', 'diabetes medication'): "May affect blood sugar levels",
            ('garlic', 'warfarin'): "May increase bleeding risk significantly",
            ('garlic', 'saquinavir'): "May reduce effectiveness of HIV medication",
            ('st john\'s wort', 'ssri'): "May cause serotonin syndrome",
            ('st john\'s wort', 'birth control pills'): "May reduce effectiveness of contraceptives",
            ('st john\'s wort', 'immunosuppressants'): "May reduce effectiveness",
            ('ginkgo', 'blood thinners'): "May increase bleeding risk",
            ('licorice', 'digoxin'): "May increase risk of irregular heartbeat",
            ('licorice', 'diuretics'): "May cause low potassium levels",
            ('valerian', 'sedatives'): "May cause excessive drowsiness",
            ('valerian', 'anesthesia'): "May enhance sedative effects",
            ('echinacea', 'immunosuppressants'): "May counteract immunosuppressive effects",
        }
    
    def _load_herb_interactions(self) -> Dict[Tuple[str, str], Dict]:
        """Load herb-herb interactions database"""
        return {
            ('ginger', 'garlic'): {
                'severity': 'WARNING',
                'effect': 'Combined use may significantly increase bleeding risk'
            },
            ('ginkgo', 'garlic'): {
                'severity': 'WARNING',
                'effect': 'May increase bleeding risk when combined'
            },
            ('st john\'s wort', 'valerian'): {
                'severity': 'INFO',
                'effect': 'May have additive sedative effects'
            },
            ('licorice', 'aloe'): {
                'severity': 'WARNING',
                'effect': 'May cause low potassium levels'
            },
        }
    
    def _load_pregnancy_safety(self) -> Dict[str, Dict]:
        """Load pregnancy safety information"""
        return {
            'curcumin': {'safe': True, 'reason': 'Generally safe in food amounts'},
            'ginger': {'safe': True, 'reason': 'Safe for morning sickness in moderate amounts'},
            'licorice': {'safe': False, 'reason': 'May increase risk of preterm labor'},
            'st john\'s wort': {'safe': False, 'reason': 'Insufficient safety data'},
            'valerian': {'safe': 'caution', 'reason': 'Limited safety data available'},
            'echinacea': {'safe': 'caution', 'reason': 'Limited safety data available'},
            'ashwagandha': {'safe': False, 'reason': 'May cause miscarriage'},
            'fenugreek': {'safe': 'caution', 'reason': 'May stimulate uterine contractions'},
        }
    
    def _load_dosage_limits(self) -> Dict[str, Dict]:
        """Load recommended and maximum dosages"""
        return {
            'curcumin': {
                'recommended': '500-2000 mg per day',
                'maximum': '12g per day (higher doses may cause GI upset)'
            },
            'ginger': {
                'recommended': '1-4g per day',
                'maximum': '5g per day (higher doses may cause heartburn)'
            },
            'garlic': {
                'recommended': '600-1200 mg per day',
                'maximum': '7200 mg per day (may cause odor and GI upset)'
            },
            'st john\'s wort': {
                'recommended': '300 mg three times daily',
                'maximum': '1800 mg per day'
            },
            'valerian': {
                'recommended': '300-600 mg before bedtime',
                'maximum': '900 mg per day'
            },
            'ginkgo': {
                'recommended': '120-240 mg per day',
                'maximum': '600 mg per day'
            },
        }


# Example usage and testing
if __name__ == '__main__':
    print("="*70)
    print("🛡️  HERBAL SAFETY CHECKER - Week 3")
    print("="*70)
    
    checker = HerbalSafetyChecker()
    
    # Test case 1: Patient with hypertension taking blood thinners
    print("\n📋 Test Case 1: Hypertension patient on Warfarin")
    print("-"*70)
    
    report = checker.get_comprehensive_safety_report(
        herbs=['Curcumin', 'Licorice', 'Ginger'],
        patient_conditions=['Hypertension'],
        current_medications=['Warfarin']
    )
    
    print(f"\n{report['summary']}\n")
    
    if report['critical']:
        print("🚨 CRITICAL WARNINGS:")
        for warning in report['critical']:
            print(f"   {warning.message}")
    
    if report['warnings']:
        print("\n⚠️  WARNINGS:")
        for warning in report['warnings']:
            print(f"   {warning.message}")
    
    if report['info']:
        print("\nℹ️  INFORMATION:")
        for warning in report['info']:
            print(f"   {warning.message}")
    
    # Test case 2: Pregnant woman
    print("\n\n📋 Test Case 2: Pregnant Patient")
    print("-"*70)
    
    report2 = checker.get_comprehensive_safety_report(
        herbs=['Ginger', 'Ashwagandha'],
        is_pregnant=True
    )
    
    print(f"\n{report2['summary']}\n")
    
    if report2['critical']:
        print("🚨 CRITICAL WARNINGS:")
        for warning in report2['critical']:
            print(f"   {warning.message}")
    
    if report2['warnings']:
        print("\n⚠️  WARNINGS:")
        for warning in report2['warnings']:
            print(f"   {warning.message}")
    
    # Test case 3: Herb combination check
    print("\n\n📋 Test Case 3: Multiple Herbs for Inflammation")
    print("-"*70)
    
    report3 = checker.get_comprehensive_safety_report(
        herbs=['Ginger', 'Garlic', 'Curcumin'],
        patient_conditions=[]
    )
    
    print(f"\n{report3['summary']}\n")
    
    if report3['warnings']:
        print("⚠️  COMBINATION WARNINGS:")
        for warning in report3['warnings']:
            print(f"   {warning.message}")
    
    if report3['info']:
        print("\nℹ️  DOSAGE INFORMATION:")
        for warning in report3['info']:
            print(f"   {warning.message}")
    
    print("\n" + "="*70)
    print("✅ Safety checker demonstration complete")
    print("="*70)
