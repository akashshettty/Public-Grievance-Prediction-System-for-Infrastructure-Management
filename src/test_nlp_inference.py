"""
Inference script to verify NLP functionality.
"""

import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml_modules.nlp.classifier import ComplaintClassifierNLP

def test_inference():
    print("Initializing NLP Engine (this may take a moment to load DistilBERT)...")
    try:
        nlp = ComplaintClassifierNLP()
        
        test_cases = [
            "road fully damaged near apartment blocks in Whitefield",
            "sewage water is overflowing from a blocked manhole since morning",
            "all streetlights are off in our street, very dangerous at night for women and children",
            "garbage has been piling up at the street corner for 5 days, smelling bad",
            "drinking water supply has been contaminated with dirt"
        ]
        
        print("\n" + "="*50)
        print("NLP COMPLAINT INTELLIGENCE - INFERENCE TEST")
        print("="*50)
        
        for text in test_cases:
            result = nlp.analyze_complaint(text)
            print(f"\nText: {result['text']}")
            print(f"Category: {result['category']} (Conf: {result['category_confidence']:.2f})")
            print(f"Severity: {result['severity_label']} (Score: {result['severity_score']:.2f})")
            print(f"Urgency: {result['urgency']}")
            
    except Exception as e:
        print(f"Error during inference: {e}")

if __name__ == "__main__":
    test_inference()
