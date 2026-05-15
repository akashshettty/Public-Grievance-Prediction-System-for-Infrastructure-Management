
from typing import Dict, Any, List
from datetime import datetime
from backend.services.data_service import DataService
from backend.services.ai_service import AIService
import pandas as pd

class ReportService:
    def __init__(self):
        self.data_service = DataService()
        self.ai_service = AIService()
    
    def generate_report(self, report_type: str, title: str, ward: str = None) -> Dict[str, Any]:
        """
        Generate a comprehensive infrastructure report.
        """
        grievances = self.data_service.get_grievances_data()
        if ward:
            grievances = grievances[grievances['ward'] == ward]
            
        # Common stats
        total = len(grievances)
        resolved = len(grievances[grievances['status'].str.lower() == 'resolved'])
        
        # Get AI insights
        escalations = self.ai_service.predict_escalations()
        health = self.ai_service.assess_infrastructure_health()
        
        return {
            "report_id": f"REP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": title or f"{report_type} - {datetime.now().strftime('%B %Y')}",
            "generated_at": datetime.now().isoformat(),
            "type": report_type,
            "summary": {
                "total_complaints": int(total),
                "resolution_rate": float(resolved / total) if total > 0 else 0,
                "status": "Critical" if total > 100 and (resolved/total) < 0.5 else "Stable"
            },
            "ai_insights": {
                "top_escalation_risks": escalations.get('risks', [])[:5],
                "infrastructure_health_score": health.get('overall_health', 0),
                "critical_wards": health.get('critical_wards', [])
            },
            "recommendations": [
                "Prioritize high-severity road infrastructure complaints in central wards.",
                "Increase maintenance frequency for drainage systems before monsoon season.",
                "Implement automated fraud detection for suspicious complaint closures."
            ]
        }
