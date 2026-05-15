"""
NLP Pipeline Runner
Orchestrates complaint intelligence analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import json

from src.nlp.complaint_analysis import (
    ComplaintAnalysis,
    ComplaintClassifier,
    SeveritySentimentAnalyzer,
    UrgencyScorer,
    DuplicateDetector,
    FraudDetector,
    ComplaintSummarizer
)


class NLPComplaintPipeline:
    """
    Complete NLP pipeline for complaint intelligence
    
    Flow:
    1. Fraud detection (filter spam)
    2. Classification (categorize issue type)
    3. Severity & Sentiment analysis
    4. Duplicate detection
    5. Urgency scoring
    6. Summarization
    """
    
    def __init__(self):
        self.classifier = ComplaintClassifier()
        self.sentiment_analyzer = SeveritySentimentAnalyzer()
        self.urgency_scorer = UrgencyScorer()
        self.duplicate_detector = DuplicateDetector()
        self.fraud_detector = FraudDetector()
        self.summarizer = ComplaintSummarizer()
    
    def process_complaint(
        self,
        complaint_text: str,
        complaint_id: str,
        timestamp: datetime,
        historical_complaints: Optional[pd.DataFrame] = None,
        reference_date: Optional[datetime] = None
    ) -> ComplaintAnalysis:
        """
        Process single complaint through entire pipeline
        
        Args:
            complaint_text: The complaint description
            complaint_id: Unique complaint identifier
            timestamp: When complaint was filed
            historical_complaints: DataFrame for duplicate detection
            reference_date: Date to calculate days since reported (default: now)
            
        Returns:
            ComplaintAnalysis object with all intelligence
        """
        if reference_date is None:
            reference_date = datetime.now()
        
        # 1. Fraud Detection
        is_fraudulent, fraud_score = self.fraud_detector.detect_fraud(complaint_text)
        
        # 2. Classification
        classification, class_confidence = self.classifier.classify(complaint_text)
        
        # 3. Severity & Sentiment
        severity = self.sentiment_analyzer.analyze_severity(complaint_text)
        sentiment, sentiment_score = self.sentiment_analyzer.analyze_sentiment(complaint_text)
        
        # 4. Duplicate Detection
        is_duplicate = False
        duplicate_similarity = 0.0
        if historical_complaints is not None and not historical_complaints.empty:
            is_duplicate, duplicate_similarity, _ = self.duplicate_detector.find_duplicates(
                complaint_text,
                historical_complaints
            )
        
        # 5. Urgency Scoring
        days_since_reported = (reference_date - timestamp).days
        urgency = self.urgency_scorer.calculate_urgency(
            classification,
            severity,
            days_since_reported
        )
        
        # 6. Summarization
        summary = self.summarizer.summarize(complaint_text)
        
        # 7. Key entity extraction (simple approach)
        key_entities = self._extract_entities(complaint_text, classification)
        
        # 8. Recommended action
        recommended_action = self._recommend_action(
            classification,
            severity,
            urgency,
            is_fraudulent,
            is_duplicate
        )
        
        return ComplaintAnalysis(
            complaint_id=complaint_id,
            classification=classification,
            classification_confidence=class_confidence,
            severity_score=severity,
            sentiment_label=sentiment,
            sentiment_score=sentiment_score,
            urgency_score=urgency,
            is_duplicate=is_duplicate,
            duplicate_similarity=duplicate_similarity,
            is_fraudulent=is_fraudulent,
            fraud_score=fraud_score,
            summary=summary,
            key_entities=key_entities,
            recommended_action=recommended_action
        )
    
    def process_batch(
        self,
        complaints_df: pd.DataFrame,
        text_column: str = 'description',
        id_column: str = 'complaint_id',
        timestamp_column: str = 'timestamp'
    ) -> pd.DataFrame:
        """
        Process batch of complaints
        
        Args:
            complaints_df: DataFrame with complaint data
            text_column: Column name with complaint text
            id_column: Column name with complaint IDs
            timestamp_column: Column name with timestamps
            
        Returns:
            DataFrame with NLP analysis results
        """
        results = []
        historical_complaints = complaints_df[[id_column, text_column]].rename(
            columns={id_column: 'complaint_id', text_column: 'description'}
        )
        
        for idx, row in complaints_df.iterrows():
            try:
                complaint_id = row[id_column]
                text = str(row[text_column])
                timestamp = pd.to_datetime(row[timestamp_column])
                
                # Exclude current complaint from duplicate detection
                hist_complaints = historical_complaints[
                    historical_complaints['complaint_id'] != complaint_id
                ]
                
                analysis = self.process_complaint(
                    text,
                    complaint_id,
                    timestamp,
                    hist_complaints
                )
                
                results.append({
                    'complaint_id': analysis.complaint_id,
                    'classification': analysis.classification,
                    'classification_confidence': analysis.classification_confidence,
                    'severity_score': analysis.severity_score,
                    'sentiment': analysis.sentiment_label,
                    'sentiment_score': analysis.sentiment_score,
                    'urgency_score': analysis.urgency_score,
                    'is_duplicate': analysis.is_duplicate,
                    'duplicate_similarity': analysis.duplicate_similarity,
                    'is_fraudulent': analysis.is_fraudulent,
                    'fraud_score': analysis.fraud_score,
                    'summary': analysis.summary,
                    'key_entities': ','.join(analysis.key_entities),
                    'recommended_action': analysis.recommended_action
                })
            except Exception as e:
                print(f"Error processing complaint {row.get(id_column)}: {e}")
                continue
        
        return pd.DataFrame(results)
    
    @staticmethod
    def _extract_entities(text: str, category: str) -> List[str]:
        """Extract key entities from complaint text"""
        entities = []
        
        # Extract location references
        location_keywords = ['near', 'at', 'along', 'on', 'near', 'beside', 'outside']
        words = text.split()
        
        for i, word in enumerate(words):
            if word.lower() in location_keywords and i + 1 < len(words):
                location = words[i + 1]
                if len(location) > 3 and not location.endswith(','):
                    entities.append(location)
        
        # Add category as entity
        if category and category != 'Other':
            entities.append(category)
        
        # Remove duplicates and limit
        entities = list(set(entities))[:5]
        
        return entities
    
    @staticmethod
    def _recommend_action(
        classification: str,
        severity: float,
        urgency: float,
        is_fraudulent: bool,
        is_duplicate: bool
    ) -> str:
        """Generate recommended action"""
        if is_fraudulent:
            return "Flag as spam - investigate user account"
        
        if is_duplicate:
            return "Merge with existing complaint - avoid duplicate work"
        
        if urgency > 0.8 and severity > 0.7:
            return "URGENT: Escalate to senior management - immediate action required"
        
        if urgency > 0.6 and severity > 0.5:
            return "High priority: Assign dedicated team within 24 hours"
        
        if urgency > 0.4:
            return "Medium priority: Schedule for resolution within 1 week"
        
        return "Low priority: Regular complaint handling procedures"


def run_nlp_pipeline(
    input_csv: Path,
    output_csv: Path,
    text_column: str = 'description',
    id_column: str = 'complaint_id',
    timestamp_column: str = 'timestamp'
) -> None:
    """
    Run NLP pipeline on complaint CSV file
    
    Args:
        input_csv: Path to input CSV with complaints
        output_csv: Path to save analyzed complaints
        text_column: Name of column with complaint text
        id_column: Name of column with complaint IDs
        timestamp_column: Name of column with timestamps
    """
    print(f"Loading complaints from {input_csv}...")
    complaints_df = pd.read_csv(input_csv)
    
    print(f"Processing {len(complaints_df)} complaints through NLP pipeline...")
    pipeline = NLPComplaintPipeline()
    
    nlp_results = pipeline.process_batch(
        complaints_df,
        text_column=text_column,
        id_column=id_column,
        timestamp_column=timestamp_column
    )
    
    # Merge results with original data
    output_df = complaints_df.merge(nlp_results, on=id_column, how='left')
    
    print(f"Saving results to {output_csv}...")
    output_df.to_csv(output_csv, index=False)
    
    # Print statistics
    print("\n=== NLP Analysis Summary ===")
    print(f"Total complaints: {len(output_df)}")
    print(f"Fraudulent complaints: {output_df['is_fraudulent'].sum()}")
    print(f"Duplicate complaints: {output_df['is_duplicate'].sum()}")
    print(f"\nComplaint Classification Distribution:")
    print(output_df['classification'].value_counts())
    print(f"\nAverage Urgency Score: {output_df['urgency_score'].mean():.2f}")
    print(f"Average Severity Score: {output_df['severity_score'].mean():.2f}")
