"""
Escalation Prediction System
Predicts which complaints are likely to escalate into social/media issues
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class EscalationPrediction:
    """Result of escalation prediction"""
    complaint_id: str
    escalation_risk_score: float  # 0-1
    escalation_probability: float  # 0-1
    risk_level: str  # low, medium, high, critical
    predicted_escalation_time_days: int
    likely_escalation_channels: List[str]  # social_media, news_media, legal, protest
    contributing_factors: List[str]
    mitigation_actions: List[str]


class EscalationPredictor:
    """
    Predicts escalation risk of complaints
    
    Factors:
    - Complaint age (unresolved duration)
    - Severity
    - Recurrence (reopenings)
    - Citizen engagement (views, shares)
    - Geographic concentration
    - Media sensitivity
    """
    
    def __init__(self):
        self.media_sensitive_terms = {
            'infrastructure_failure': ['collapsed', 'failure', 'dangerous', 'hazard', 'risk'],
            'water_crisis': ['water shortage', 'contaminated', 'disease', 'health'],
            'child_safety': ['school', 'child', 'playground', 'safety', 'injury'],
            'traffic_accident': ['accident', 'death', 'injury', 'collision', 'fatal'],
        }
    
    def calculate_escalation_risk(
        self,
        complaint_age_days: int,
        severity_score: float,
        reopening_count: int,
        complaint_text: str,
        views_count: int = 0,
        resolution_rate_percent: float = 75
    ) -> float:
        """
        Calculate escalation risk (0-1)
        
        Args:
            complaint_age_days: Days since complaint filed
            severity_score: Severity (0-1)
            reopening_count: Number of times reopened
            complaint_text: Complaint description
            views_count: Number of views (social/media engagement)
            resolution_rate_percent: Historical resolution rate for issue type
            
        Returns:
            Escalation risk score (0-1)
        """
        risk_score = 0.0
        
        # 1. Age factor (older unresolved complaints more likely to escalate)
        if complaint_age_days > 30:
            age_risk = min(0.4, (complaint_age_days - 30) / 180)
            risk_score += age_risk
        
        # 2. Severity multiplier (high severity complaints escalate faster)
        severity_multiplier = 0.3 + (severity_score * 0.3)
        risk_score *= (1 + severity_multiplier)
        
        # 3. Reopening penalty (recurring issues suggest systemic problems)
        if reopening_count > 0:
            reopening_risk = min(0.3, reopening_count * 0.1)
            risk_score += reopening_risk
        
        # 4. Public engagement (higher engagement = higher escalation)
        if views_count > 100:
            engagement_risk = min(0.25, (views_count / 1000) * 0.1)
            risk_score += engagement_risk
        
        # 5. Media sensitivity (check for sensitive keywords)
        media_risk = self._detect_media_sensitivity(complaint_text)
        risk_score += media_risk
        
        # 6. Resolution rate (poor resolution rate = higher escalation)
        if resolution_rate_percent < 50:
            resolution_risk = 0.25
            risk_score += resolution_risk
        
        return min(1.0, max(0.0, risk_score))
    
    def predict_escalation_channel(
        self,
        complaint_text: str,
        severity: float,
        complaint_age_days: int,
        geographic_concentration: float
    ) -> List[str]:
        """
        Predict likely escalation channels
        
        Returns:
            List of potential escalation channels
        """
        channels = []
        
        # Social media (high severity + age)
        if severity > 0.5 and complaint_age_days > 14:
            channels.append('social_media')
        
        # News media (very high severity or public safety)
        if severity > 0.8 or 'health' in complaint_text.lower() or 'safety' in complaint_text.lower():
            channels.append('news_media')
        
        # Legal issues (infrastructure damage affecting multiple properties)
        if 'damage' in complaint_text.lower() and geographic_concentration > 0.6:
            channels.append('legal')
        
        # Public protest (community-level issues)
        if geographic_concentration > 0.7 and complaint_age_days > 30:
            channels.append('protest')
        
        # Community organizing
        if complaint_age_days > 45 and severity > 0.6:
            channels.append('community_organizing')
        
        return channels if channels else ['social_media']
    
    def predict_escalation_time(
        self,
        severity: float,
        complaint_age_days: int,
        resolution_rate_percent: float
    ) -> int:
        """
        Predict when escalation might occur (days from now)
        
        Returns:
            Estimated days until escalation
        """
        if resolution_rate_percent > 85:
            # Good resolution rate - longer before escalation
            base_days = 60
        elif resolution_rate_percent > 60:
            base_days = 30
        elif resolution_rate_percent > 40:
            base_days = 14
        else:
            base_days = 7
        
        # Adjust based on severity
        severity_multiplier = 1.0 - (severity * 0.5)
        
        # Adjust based on current age
        if complaint_age_days > 30:
            time_until_escalation = max(1, base_days - (complaint_age_days - 30) / 3)
        else:
            time_until_escalation = base_days * severity_multiplier
        
        return max(1, int(time_until_escalation))
    
    def _detect_media_sensitivity(self, text: str) -> float:
        """Detect media-sensitive terms in complaint"""
        text_lower = text.lower()
        sensitivity_score = 0.0
        
        for category, keywords in self.media_sensitive_terms.items():
            if any(keyword in text_lower for keyword in keywords):
                sensitivity_score = 0.2
                break
        
        return sensitivity_score
    
    def generate_escalation_prediction(
        self,
        complaint_id: str,
        complaint_metrics: Dict
    ) -> EscalationPrediction:
        """
        Generate comprehensive escalation prediction
        
        Args:
            complaint_id: ID of complaint
            complaint_metrics: Dictionary with all relevant metrics
            
        Returns:
            EscalationPrediction object
        """
        # Calculate escalation risk
        risk_score = self.calculate_escalation_risk(
            complaint_metrics.get('complaint_age_days', 0),
            complaint_metrics.get('severity_score', 0.5),
            complaint_metrics.get('reopening_count', 0),
            complaint_metrics.get('description', ''),
            complaint_metrics.get('views_count', 0),
            complaint_metrics.get('resolution_rate_percent', 75)
        )
        
        # Classify risk level
        if risk_score > 0.8:
            risk_level = 'critical'
            probability = 0.85
        elif risk_score > 0.6:
            risk_level = 'high'
            probability = 0.65
        elif risk_score > 0.4:
            risk_level = 'medium'
            probability = 0.45
        else:
            risk_level = 'low'
            probability = 0.20
        
        # Predict escalation channels
        channels = self.predict_escalation_channel(
            complaint_metrics.get('description', ''),
            complaint_metrics.get('severity_score', 0.5),
            complaint_metrics.get('complaint_age_days', 0),
            complaint_metrics.get('geographic_concentration', 0.5)
        )
        
        # Predict escalation time
        escalation_time = self.predict_escalation_time(
            complaint_metrics.get('severity_score', 0.5),
            complaint_metrics.get('complaint_age_days', 0),
            complaint_metrics.get('resolution_rate_percent', 75)
        )
        
        # Contributing factors
        factors = []
        if complaint_metrics.get('complaint_age_days', 0) > 30:
            factors.append("Long unresolved duration")
        if complaint_metrics.get('reopening_count', 0) > 2:
            factors.append("Multiple reopenings indicate unresolved issue")
        if complaint_metrics.get('severity_score', 0) > 0.7:
            factors.append("High severity complaint")
        if complaint_metrics.get('views_count', 0) > 100:
            factors.append("High public engagement/awareness")
        
        # Mitigation actions
        actions = []
        if risk_level in ['critical', 'high']:
            actions.append("Escalate to senior management immediately")
            actions.append("Assign dedicated resolution team")
            actions.append("Establish direct communication with citizen")
            
            if 'news_media' in channels:
                actions.append("Prepare media statement")
                actions.append("Document resolution progress for transparency")
            
            if 'legal' in channels:
                actions.append("Consult legal team")
                actions.append("Document all correspondence")
            
            if 'protest' in channels:
                actions.append("Engage with community representatives")
                actions.append("Schedule public information meeting")
        
        elif risk_level == 'medium':
            actions.append("Increase monitoring frequency")
            actions.append("Communicate resolution timeline to citizen")
            actions.append("Consider accelerated resolution timeline")
        
        else:
            actions.append("Standard complaint handling")
            actions.append("Regular monitoring")
        
        return EscalationPrediction(
            complaint_id=complaint_id,
            escalation_risk_score=risk_score,
            escalation_probability=probability,
            risk_level=risk_level,
            predicted_escalation_time_days=escalation_time,
            likely_escalation_channels=channels,
            contributing_factors=factors,
            mitigation_actions=actions
        )


class EscalationMonitor:
    """
    Monitors complaints for signs of escalation
    Tracks sentiment, engagement, and public response
    """
    
    def __init__(self):
        self.escalation_keywords = {
            'viral': ['viral', 'trending', 'widespread', 'massive', 'outrage'],
            'anger': ['angry', 'furious', 'outraged', 'disgusted', 'unacceptable'],
            'legal': ['lawsuit', 'legal', 'court', 'compensation', 'damages'],
            'media': ['journalist', 'news', 'media', 'report', 'coverage']
        }
    
    def analyze_escalation_signals(
        self,
        complaint_id: str,
        social_media_mentions: int = 0,
        news_mentions: int = 0,
        sentiment_trend: str = 'neutral',  # negative, neutral, positive
        engagement_rate: float = 0.0
    ) -> Dict:
        """
        Analyze real-time escalation signals
        
        Returns:
            Dictionary with escalation signals
        """
        escalation_signals = {
            'complaint_id': complaint_id,
            'signal_count': 0,
            'signals_detected': [],
            'urgency': 'normal'
        }
        
        # Social media signal
        if social_media_mentions > 50:
            escalation_signals['signals_detected'].append('viral_social_media')
            escalation_signals['signal_count'] += 1
        
        if social_media_mentions > 100:
            escalation_signals['urgency'] = 'critical'
        
        # News media signal
        if news_mentions > 0:
            escalation_signals['signals_detected'].append('news_coverage')
            escalation_signals['signal_count'] += 1
            escalation_signals['urgency'] = 'critical'
        
        # Sentiment deterioration
        if sentiment_trend == 'negative':
            escalation_signals['signals_detected'].append('negative_sentiment')
            escalation_signals['signal_count'] += 1
        
        # High engagement
        if engagement_rate > 0.3:  # More than 30% of viewers engage
            escalation_signals['signals_detected'].append('high_engagement')
            escalation_signals['signal_count'] += 1
        
        if escalation_signals['signal_count'] > 2:
            escalation_signals['urgency'] = 'critical'
        elif escalation_signals['signal_count'] > 0:
            escalation_signals['urgency'] = 'high'
        
        return escalation_signals
