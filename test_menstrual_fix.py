#!/usr/bin/env python3
"""
Quick test to verify the improved detect_condition_v2() function
Tests the three main menstrual/hormonal condition detection improvements
"""

import sys
sys.path.insert(0, '/Users/vishwaksen/Desktop/research/src')

from ai_assistant import detect_condition_v2

# Test Case 1: PCOS/Hormonal Disorder detection
print("=" * 80)
print("TEST 1: PCOS/Hormonal Disorder Detection")
print("=" * 80)
user_input1 = "I have missed my periods for 3 months, slight hair loss, and acne."
detected1, confidence1 = detect_condition_v2(user_input1)
print(f"Input: {user_input1}")
print(f"Detected: {detected1}")
print(f"Confidence: {confidence1:.2%}")
print(f"✓ PASS" if "Hormonal Disorder" in detected1 or "PCOS" in detected1 else f"✗ FAIL - Expected Hormonal Disorder/PCOS")
print()

# Test Case 2: Menorrhagia detection (heavy bleeding with weakness/dizziness)
print("=" * 80)
print("TEST 2: Menorrhagia Detection")
print("=" * 80)
user_input2 = "My bleeding lasts more than a week, and I feel weak and dizzy."
detected2, confidence2 = detect_condition_v2(user_input2)
print(f"Input: {user_input2}")
print(f"Detected: {detected2}")
print(f"Confidence: {confidence2:.2%}")
print(f"✓ PASS" if "Menorrhagia" in detected2 else f"✗ FAIL - Expected Menorrhagia")
print()

# Test Case 3: Dysmenorrhea should still work (period pain/cramps)
print("=" * 80)
print("TEST 3: Dysmenorrhea Detection (Period Pain)")
print("=" * 80)
user_input3 = "I have severe period pain and lower abdominal cramps during my cycle."
detected3, confidence3 = detect_condition_v2(user_input3)
print(f"Input: {user_input3}")
print(f"Detected: {detected3}")
print(f"Confidence: {confidence3:.2%}")
print(f"✓ PASS" if "Dysmenorrhea" in detected3 else f"✗ FAIL - Expected Dysmenorrhea")
print()

# Test Case 4: Ensure Influenza is NOT detected for menstrual symptoms
print("=" * 80)
print("TEST 4: Influenza NOT Detected for Menstrual Symptoms")
print("=" * 80)
user_input4 = "My bleeding lasts more than a week, and I feel weak."
detected4, confidence4 = detect_condition_v2(user_input4)
print(f"Input: {user_input4}")
print(f"Detected: {detected4}")
print(f"Confidence: {confidence4:.2%}")
print(f"✓ PASS" if "Menorrhagia" in detected4 and "Influenza" not in detected4 else f"✗ FAIL - Expected Menorrhagia, NOT Influenza")
print()

# Test Case 5: Ensure other conditions still work (preserved mappings)
print("=" * 80)
print("TEST 5: Fever/Influenza Detection (Preserved Mapping)")
print("=" * 80)
user_input5 = "I have high fever, body ache, and chills."
detected5, confidence5 = detect_condition_v2(user_input5)
print(f"Input: {user_input5}")
print(f"Detected: {detected5}")
print(f"Confidence: {confidence5:.2%}")
print(f"✓ PASS" if "Influenza" in detected5 or "Viral" in detected5 else f"✗ FAIL - Expected Influenza/Viral Fever")
print()

# Test Case 6: Arthritis (joint pain) - preserved mapping
print("=" * 80)
print("TEST 6: Arthritis Detection (Preserved Mapping)")
print("=" * 80)
user_input6 = "I have joint pain and morning stiffness in my knees."
detected6, confidence6 = detect_condition_v2(user_input6)
print(f"Input: {user_input6}")
print(f"Detected: {detected6}")
print(f"Confidence: {confidence6:.2%}")
print(f"✓ PASS" if "Arthritis" in detected6 else f"✗ FAIL - Expected Arthritis")
print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
results = [
    ("PCOS Detection", "Hormonal Disorder" in detected1 or "PCOS" in detected1),
    ("Menorrhagia Detection", "Menorrhagia" in detected2),
    ("Dysmenorrhea Detection", "Dysmenorrhea" in detected3),
    ("Menorrhagia (not Influenza)", "Menorrhagia" in detected4 and "Influenza" not in detected4),
    ("Influenza Preserved", "Influenza" in detected5 or "Viral" in detected5),
    ("Arthritis Preserved", "Arthritis" in detected6),
]

passed = sum(1 for _, result in results if result)
total = len(results)

for test_name, result in results:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status}: {test_name}")

print(f"\n{passed}/{total} tests passed")
