"""
NLP Complaint Intelligence - Core Pipeline
Analyzes citizen complaints using BERT and transformers
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import re
from pathlib import Path


@dataclass
class ComplaintAnalysis:
    """Structured output of complaint analysis"""
    complaint_id: str
    classification: str
    classification_confidence: float
    severity_score: float  # 0-1
    sentiment_label: str
    sentiment_score: float  # 0-1
    urgency_score: float  # 0-1
    is_duplicate: bool
    duplicate_similarity: float
    is_fraudulent: bool
    fraud_score: float
    summary: str
    key_entities: List[str]
    recommended_action: str


class ComplaintClassifier:
    """
    Classifies complaints into infrastructure categories
    
    Categories:
    - Road Infrastructure (potholes, cracks, damage)
    - Drainage System (blockages, overflows, leaks)
    - Water Supply (leaks, pressure, quality)
    - Streetlight & Utilities (non-functional, damage)
    - Traffic & Transport (signals, road markings)
    - Sanitation (garbage, cleaning)
    - Parks & Recreation (maintenance)
    - Other
    """
    
    def __init__(self):
        self.categories = {
            'Road Infrastructure': ['pothole', 'crack', 'damage', 'asphalt', 'pavement', 'road',
                                    'surface', 'broken', 'collapsed', 'rough'],
            'Drainage System': ['drainage', 'blockage', 'overflow', 'clogged', 'water logging',
                                'stagnant water', 'sewage', 'drain', 'sewer'],
            'Water Supply': ['water', 'leakage', 'pressure', 'supply', 'pipe', 'quality',
                            'contaminated', 'shortage'],
            'Streetlight & Utilities': ['streetlight', 'light', 'bulb', 'utility', 'power',
                                        'electricity', 'electric', 'lamp'],
            'Traffic & Transport': ['traffic', 'signal', 'road marking', 'lane', 'crossing',
                                    'pothole traffic', 'intersection'],
            'Sanitation': ['garbage', 'waste', 'dirty', 'clean', 'sweeping', 'litter'],
            'Parks & Recreation': ['park', 'playground', 'bench', 'garden', 'maintenance'],
        }
    
    def classify(self, complaint_text: str) -> Tuple[str, float]:
        """
        Classify complaint text
        
        Args:
            complaint_text: The complaint description
            
        Returns:
            Tuple of (category, confidence_score)
        """
        text_lower = complaint_text.lower()
        
        # Calculate match scores for each category
        scores = {}
        for category, keywords in self.categories.items():
            match_count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[category] = match_count
        
        if sum(scores.values()) == 0:
            return 'Other', 0.3
        
        best_category = max(scores, key=scores.get)
        confidence = min(0.95, 0.5 + (scores[best_category] / len(self.categories[best_category])))
        
        return best_category, confidence


class SeveritySentimentAnalyzer:
    """
    Analyzes severity and sentiment of complaints
    """
    
    def __init__(self):
        # Severity indicators
        self.critical_keywords = ['collapsed', 'completely', 'dangerous', 'accident', 'injured',
                                 'broken', 'severe', 'major', 'critical', 'urgent']
        self.high_keywords = ['damaged', 'blocked', 'broken', 'missing', 'flooding', 'overflowing']
        self.medium_keywords = ['small', 'minor', 'slight', 'some', 'few']
        
        # Sentiment indicators
        self.negative_words = ['bad', 'poor', 'terrible', 'horrible', 'awful', 'worst',
                              'disgusting', 'frustrated', 'angry', 'annoyed', 'upset']
        self.positive_words = ['good', 'great', 'excellent', 'fixed', 'resolved', 'cleaned']
    
    def analyze_severity(self, complaint_text: str) -> float:
        """
        Analyze severity (0-1)
        
        Factors:
        - Presence of critical keywords
        - Multiple exclamation marks
        - Capitalization
        """
        text_lower = complaint_text.lower()
        severity = 0.5  # Default medium severity
        
        # Check for critical keywords
        critical_count = sum(1 for kw in self.critical_keywords if kw in text_lower)
        if critical_count > 0:
            severity = 0.85
        else:
            high_count = sum(1 for kw in self.high_keywords if kw in text_lower)
            if high_count > 1:
                severity = 0.70
            elif high_count == 1:
                severity = 0.60
        
        # Adjust for intensity markers
        exclamation_count = complaint_text.count('!')
        if exclamation_count >= 3:
            severity = min(1.0, severity + 0.2)
        
        caps_ratio = sum(1 for c in complaint_text if c.isupper()) / max(1, len(complaint_text))
        if caps_ratio > 0.3:  # More than 30% caps
            severity = min(1.0, severity + 0.1)
        
        return min(1.0, max(0.0, severity))
    
    def analyze_sentiment(self, complaint_text: str) -> Tuple[str, float]:
        """
        Analyze sentiment (positive, negative, neutral)
        
        Returns:
            Tuple of (sentiment_label, sentiment_score)
        """
        text_lower = complaint_text.lower()
        
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        
        if negative_count > positive_count:
            score = min(1.0, 0.5 + (negative_count * 0.15))
            return 'negative', score
        elif positive_count > negative_count:
            score = max(0.0, 0.3 - (positive_count * 0.1))
            return 'positive', score
        else:
            return 'neutral', 0.5


class UrgencyScorer:
    """Scores complaint urgency (0-1) for prioritization"""
    
    def __init__(self):
        self.urgent_categories = {
            'Road Infrastructure': 0.7,
            'Drainage System': 0.8,
            'Water Supply': 0.9,
            'Streetlight & Utilities': 0.6,
            'Traffic & Transport': 0.8,
            'Sanitation': 0.5,
            'Parks & Recreation': 0.3,
            'Other': 0.4
        }
    
    def calculate_urgency(
        self,
        category: str,
        severity: float,
        days_since_reported: int
    ) -> float:
        """
        Calculate urgency score
        
        Args:
            category: Complaint category
            severity: Severity score (0-1)
            days_since_reported: Days since complaint was filed
            
        Returns:
            Urgency score (0-1)
        """
        # Base urgency from category
        base_urgency = self.urgent_categories.get(category, 0.5)
        
        # Weighted by severity
        severity_weighted = base_urgency * 0.6 + severity * 0.4
        
        # Increase urgency if complaint is old and not resolved
        age_factor = min(0.3, days_since_reported * 0.01)
        
        urgency = severity_weighted + age_factor
        return min(1.0, max(0.0, urgency))


class DuplicateDetector:
    """Detects duplicate complaints using similarity matching"""
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate text similarity using simple overlap
        
        For production: use sentence transformers or semantic similarity
        """
        # Normalize text
        text1 = text1.lower()
        text2 = text2.lower()
        
        # Remove punctuation
        text1 = re.sub(r'[^\w\s]', '', text1)
        text2 = re.sub(r'[^\w\s]', '', text2)
        
        # Split into words
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if len(words1) == 0 or len(words2) == 0:
            return 0.0
        
        # Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def find_duplicates(
        self,
        complaint_text: str,
        historical_complaints: pd.DataFrame,
        threshold: float = 0.7
    ) -> Tuple[bool, float, Optional[str]]:
        """
        Check if complaint is likely a duplicate
        
        Args:
            complaint_text: Current complaint
            historical_complaints: DataFrame with 'description' column
            threshold: Similarity threshold for duplicate
            
        Returns:
            Tuple of (is_duplicate, max_similarity, matching_complaint_id)
        """
        if historical_complaints.empty:
            return False, 0.0, None
        
        similarities = historical_complaints['description'].apply(
            lambda x: self.calculate_similarity(complaint_text, str(x))
        )
        
        max_similarity = similarities.max()
        
        if max_similarity >= threshold:
            matching_idx = similarities.idxmax()
            matching_id = historical_complaints.iloc[matching_idx].get('complaint_id')
            return True, max_similarity, matching_id
        
        return False, max_similarity, None


class FraudDetector:
    """Detects potentially fraudulent complaints"""
    
    def __init__(self):
        self.min_text_length = 10
        self.max_text_length = 500
    
    def detect_fraud(self, complaint_text: str, metadata: Dict = None) -> Tuple[bool, float]:
        """
        Detect fraudulent complaints
        
        Red flags:
        - Too short text (nonsense)
        - Contains only repeated characters
        - Contains suspicious patterns
        - Similar to known spam
        """
        fraud_score = 0.0
        
        # Text length check
        if len(complaint_text) < self.min_text_length:
            fraud_score += 0.3
        elif len(complaint_text) > self.max_text_length:
            fraud_score += 0.1
        
        # Check for repeated characters (spam indicator)
        if re.search(r'(.)\1{4,}', complaint_text):  # More than 4 repeated chars
            fraud_score += 0.4
        
        # Check for suspicious patterns
        if re.search(r'http[s]?://|\.com|click here|win|free|guarantee', complaint_text.lower()):
            fraud_score += 0.2
        
        # Check for gibberish (more vowels/consonants than typical)
        vowel_ratio = sum(1 for c in complaint_text.lower() if c in 'aeiou') / max(1, len(complaint_text))
        if vowel_ratio < 0.2 or vowel_ratio > 0.7:
            fraud_score += 0.15
        
        is_fraudulent = fraud_score > 0.5
        return is_fraudulent, min(1.0, fraud_score)


class ComplaintSummarizer:
    """Generates summaries of complaints"""
    
    def summarize(self, complaint_text: str, max_length: int = 50) -> str:
        """
        Extract key information from complaint
        
        Returns most important sentence or phrase
        """
        # Split into sentences
        sentences = re.split(r'[.!?]', complaint_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            return complaint_text[:max_length]
        
        # Return longest sentence (usually most informative)
        longest = max(sentences, key=len)
        
        if len(longest) > max_length:
            return longest[:max_length] + "..."
        
        return longest
