"""
NLP Classifier Implementation - Complaint Intelligence
Uses DistilBERT for multiclass classification and sequence labeling.
"""

import torch
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List, Tuple, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplaintClassifierNLP:
    """
    Advanced NLP Classifier for UrbanPulse AI using DistilBERT.
    Handles:
    1. Category Classification
    2. Severity Detection
    3. Urgency Prediction
    4. Duplicate Detection (via embeddings)
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the NLP models.
        """
        self.device = 0 if torch.cuda.is_available() else -1
        logger.info(f"Using device: {'gpu' if self.device == 0 else 'cpu'}")
        
        # Categories as defined in BBMP context
        self.categories = [
            'Road Infrastructure', 
            'Drainage System', 
            'Water Supply', 
            'Streetlight & Utilities',
            'Traffic & Transport',
            'Sanitation',
            'Parks & Recreation',
            'Other'
        ]
        
        try:
            # Use sentiment analysis pipeline as a proxy for severity/urgency initially
            # specifically fine-tuned on SST-2 as it's small and fast
            self.severity_analyzer = pipeline(
                "sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=self.device
            )
            
            # For classification, we use zero-shot initially if no trained model
            self.zero_shot = pipeline(
                "zero-shot-classification",
                model="typeform/distilbert-base-uncased-mnli",
                device=self.device
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            
        except Exception as e:
            logger.error(f"Error initializing NLP models: {e}")
            raise

    def analyze_complaint(self, text: str) -> Dict[str, Any]:
        """
        Full analysis of a complaint text.
        """
        # 1. Classification
        classification = self.zero_shot(text, candidate_labels=self.categories)
        
        # 2. Severity & Urgency (Sentiment based)
        sevent = self.severity_analyzer(text)[0]
        
        # Heuristic: NEGATIVE sentiment = High Severity
        # Urgency is boosted by specific keywords
        urgency_score = sevent['score'] if sevent['label'] == 'NEGATIVE' else (1 - sevent['score'])
        
        critical_keywords = ['dangerous', 'accident', 'injury', 'emergency', 'collapsed', 'heavy leakage']
        if any(kw in text.lower() for kw in critical_keywords):
            urgency_score = min(1.0, urgency_score + 0.3)
            
        return {
            "text": text,
            "category": classification['labels'][0],
            "category_confidence": classification['scores'][0],
            "severity_score": float(urgency_score),
            "severity_label": "High" if urgency_score > 0.7 else "Medium" if urgency_score > 0.4 else "Low",
            "urgency": "Critical" if urgency_score > 0.8 else "Standard",
            "confidence_scores": dict(zip(classification['labels'], classification['scores']))
        }

if __name__ == "__main__":
    # Test
    nlp = ComplaintClassifierNLP()
    samples = [
        "road fully damaged near apartment",
        "sewage water overflowing from drain",
        "streetlight not working for 3 days"
    ]
    for s in samples:
        print(nlp.analyze_complaint(s))

