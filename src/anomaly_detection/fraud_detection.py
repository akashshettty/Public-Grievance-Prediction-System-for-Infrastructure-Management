"""
Anomaly Detection and Fraud Detection System
Identifies suspicious complaint closures and patterns
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.preprocessing import StandardScaler
from dataclasses import dataclass


@dataclass
class AnomalyResult:
    """Result of anomaly detection"""
    complaint_id: str
    anomaly_score: float  # 0-1
    is_anomalous: bool
    anomaly_type: str
    confidence: float
    reasons: List[str]


class IsolationForestAnomalyDetector:
    """
    Detects anomalies in complaint closure patterns
    Using Isolation Forest-like principles
    """
    
    def __init__(self, contamination_rate: float = 0.1):
        """
        Args:
            contamination_rate: Expected proportion of anomalies (0-1)
        """
        self.contamination_rate = contamination_rate
        self.scaler = StandardScaler()
    
    def detect_suspicious_closure(
        self,
        closure_time_hours: float,
        median_closure_time_hours: float,
        reopening_count: int,
        avg_reopening_count: float,
        severity_score: float,
        complaint_age_days: int
    ) -> Tuple[float, bool]:
        """
        Detect suspicious complaint closures
        
        Red flags:
        - Closed unusually fast (too good to be true)
        - Reopened multiple times
        - High severity closed quickly
        - Inconsistent with historical patterns
        
        Args:
            closure_time_hours: Hours from complaint to closure
            median_closure_time_hours: Historical median closure time
            reopening_count: Number of times reopened
            avg_reopening_count: Average reopening count
            severity_score: Complaint severity (0-1)
            complaint_age_days: Age of complaint in days
            
        Returns:
            Tuple of (anomaly_score, is_anomalous)
        """
        anomaly_score = 0.0
        
        # Unusually fast closure (especially for high severity)
        if closure_time_hours < median_closure_time_hours / 3:
            if severity_score > 0.5:
                anomaly_score += 0.4  # Suspicious - high severity closed too fast
            else:
                anomaly_score += 0.15  # Less suspicious for low severity
        
        # Excessive reopenings
        if reopening_count > avg_reopening_count + (2 * np.std([reopening_count, avg_reopening_count])):
            anomaly_score += 0.3
        
        # Pattern inconsistency
        expected_closure_time = median_closure_time_hours * (1 + severity_score * 0.5)
        closure_deviation = abs(closure_time_hours - expected_closure_time) / expected_closure_time
        
        if closure_deviation > 1.0:  # More than 2x different from expected
            anomaly_score += 0.25
        
        # High severity not given priority
        if severity_score > 0.7 and closure_time_hours > median_closure_time_hours * 2:
            anomaly_score += 0.2
        
        # Complaint still open but marked as closed
        if complaint_age_days > 30 and reopening_count == 0 and closure_time_hours > 0:
            # Possible premature closure
            anomaly_score += 0.1
        
        is_anomalous = anomaly_score > 0.5
        
        return min(1.0, anomaly_score), is_anomalous
    
    def detect_pattern_anomaly(
        self,
        features: np.ndarray,
        threshold_percentile: float = 90
    ) -> np.ndarray:
        """
        Detect anomalies in multi-dimensional feature space
        
        Args:
            features: 2D array of features (samples x features)
            threshold_percentile: Percentile for anomaly threshold
            
        Returns:
            Anomaly scores for each sample
        """
        # Normalize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Calculate anomaly scores using Manhattan distance from center
        center = np.median(features_scaled, axis=0)
        distances = np.sum(np.abs(features_scaled - center), axis=1)
        
        # Normalize scores to 0-1
        scores = distances / np.max(distances)
        
        return scores


class AutoencoderAnomalyDetector:
    """
    Simplified autoencoder-like anomaly detection
    Identifies patterns that deviate from normal behavior
    """
    
    def __init__(self):
        self.baseline_patterns = {}
    
    def learn_patterns(
        self,
        normal_data: pd.DataFrame,
        groupby_column: str = 'ward'
    ) -> None:
        """
        Learn normal patterns from historical data
        
        Args:
            normal_data: DataFrame with normal (non-anomalous) data
            groupby_column: Column to group patterns by
        """
        for group_name, group_data in normal_data.groupby(groupby_column):
            self.baseline_patterns[group_name] = {
                'mean_closure_time': group_data.get('closure_time_hours', pd.Series()).mean(),
                'std_closure_time': group_data.get('closure_time_hours', pd.Series()).std(),
                'mean_severity': group_data.get('severity_score', pd.Series()).mean(),
                'mean_reopenings': group_data.get('reopening_count', pd.Series()).mean()
            }
    
    def detect_deviation(
        self,
        data_point: Dict,
        group_name: str
    ) -> Tuple[float, bool, List[str]]:
        """
        Detect if data point deviates from learned patterns
        
        Args:
            data_point: Dictionary with complaint features
            group_name: Group identifier (e.g., ward name)
            
        Returns:
            Tuple of (anomaly_score, is_anomalous, reasons)
        """
        if group_name not in self.baseline_patterns:
            return 0.0, False, ["No baseline pattern available"]
        
        baseline = self.baseline_patterns[group_name]
        anomaly_score = 0.0
        reasons = []
        
        # Check closure time deviation
        if 'closure_time_hours' in data_point:
            closure_time = data_point['closure_time_hours']
            mean_closure = baseline['mean_closure_time']
            std_closure = baseline['std_closure_time']
            
            if std_closure > 0:
                z_score = abs(closure_time - mean_closure) / std_closure
                if z_score > 2:
                    anomaly_score += 0.3
                    reasons.append(f"Unusual closure time (z-score: {z_score:.2f})")
        
        # Check severity deviation
        if 'severity_score' in data_point:
            severity = data_point['severity_score']
            mean_severity = baseline['mean_severity']
            
            if severity > mean_severity * 1.5:
                anomaly_score += 0.2
                reasons.append("Unexpectedly high severity")
        
        # Check reopening patterns
        if 'reopening_count' in data_point:
            reopenings = data_point['reopening_count']
            mean_reopenings = baseline['mean_reopenings']
            
            if reopenings > mean_reopenings * 2:
                anomaly_score += 0.2
                reasons.append("Excessive reopenings")
        
        is_anomalous = anomaly_score > 0.5
        
        return min(1.0, anomaly_score), is_anomalous, reasons


class ComplaintAnomalyAnalyzer:
    """
    Comprehensive anomaly detection for complaints
    Combines multiple detection methods
    """
    
    def __init__(self):
        self.isolation_detector = IsolationForestAnomalyDetector()
        self.autoencoder_detector = AutoencoderAnomalyDetector()
    
    def analyze_complaint_closure(
        self,
        complaint_id: str,
        closure_metrics: Dict
    ) -> AnomalyResult:
        """
        Analyze complaint closure for anomalies
        
        Args:
            complaint_id: ID of complaint
            closure_metrics: Dictionary with closure metrics
            
        Returns:
            AnomalyResult with detection results
        """
        # Get metrics with defaults
        closure_time = closure_metrics.get('closure_time_hours', 0)
        median_closure = closure_metrics.get('median_closure_time', 100)
        reopenings = closure_metrics.get('reopening_count', 0)
        avg_reopenings = closure_metrics.get('avg_reopening_count', 0)
        severity = closure_metrics.get('severity_score', 0.5)
        age = closure_metrics.get('complaint_age_days', 0)
        
        # Detection
        iso_score, iso_anomalous = self.isolation_detector.detect_suspicious_closure(
            closure_time, median_closure, reopenings, avg_reopenings, severity, age
        )
        
        # Determine anomaly type and reasons
        reasons = []
        anomaly_type = 'normal'
        
        if closure_time < median_closure / 3 and severity > 0.5:
            anomaly_type = 'premature_closure'
            reasons.append("High severity closed unusually fast")
        
        if reopenings > avg_reopenings * 2:
            anomaly_type = 'recurring_issue'
            reasons.append("Excessive reopenings indicate unresolved issue")
        
        if closure_time > median_closure * 3:
            anomaly_type = 'delayed_closure'
            reasons.append("Unusual delay in closure")
        
        if not reasons:
            reasons.append("Pattern deviates from historical norms")
        
        confidence = 0.7 + (iso_score * 0.25)  # Higher score = higher confidence
        
        return AnomalyResult(
            complaint_id=complaint_id,
            anomaly_score=iso_score,
            is_anomalous=iso_anomalous,
            anomaly_type=anomaly_type,
            confidence=confidence,
            reasons=reasons
        )
    
    def detect_systemic_issues(
        self,
        complaint_data: pd.DataFrame,
        ward: str
    ) -> Dict:
        """
        Detect systemic issues in a ward
        
        E.g., multiple complaints of same type not being fixed
        """
        ward_complaints = complaint_data[complaint_data['area'] == ward]
        
        if ward_complaints.empty:
            return {'systemic_issues': []}
        
        # Identify recurring issues
        recurring_issues = ward_complaints[
            ward_complaints['reopening_count'] > 0
        ].groupby('issue_type').size()
        
        systemic_issues = []
        
        for issue_type, count in recurring_issues.items():
            if count > 5:  # Multiple recurring issues of same type
                systemic_issues.append({
                    'issue_type': issue_type,
                    'recurring_count': int(count),
                    'severity': 'high' if count > 10 else 'medium',
                    'recommendation': 'Systematic approach needed - investigate root cause'
                })
        
        return {
            'ward': ward,
            'systemic_issues': systemic_issues,
            'num_systemic_issues': len(systemic_issues)
        }
