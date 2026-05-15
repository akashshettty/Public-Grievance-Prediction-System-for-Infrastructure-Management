"""
Complaint Service
Handles complaint-related business logic.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.services.data_service import DataService
import pandas as pd


class ComplaintService:
    """Service for complaint data management."""
    
    def __init__(self):
        """Initialize complaint service."""
        self.data_service = DataService()
    
    def get_complaints(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get complaints with optional filtering and pagination.
        
        Args:
            filters: Filter criteria and pagination params
            
        Returns:
            Dictionary with complaint records and metadata
        """
        df = self.data_service.get_grievances_data()
        
        if df.empty:
            return {"data": [], "count": 0, "total": 0}
        
        # Apply filters
        if filters.get("status"):
            df = df[df['status'].astype(str).str.lower() == filters["status"].lower()]
        
        if filters.get("area") or filters.get("ward"):
            area_val = filters.get("area") or filters.get("ward")
            df = df[df['ward'].astype(str) == area_val]
        
        if filters.get("issue_type"):
            df = df[df['issue_type'].astype(str) == filters["issue_type"]]
        
        total = len(df)
        
        # Apply pagination
        limit = filters.get("limit", 100)
        offset = filters.get("offset", 0)
        
        paginated_df = df.iloc[offset:offset+limit]
        
        return {
            "data": paginated_df.to_dict('records'),
            "count": len(paginated_df),
            "total": total,
            "offset": offset,
            "limit": limit
        }
    
    def get_complaint(self, complaint_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific complaint by ID.
        
        Args:
            complaint_id: Complaint identifier
            
        Returns:
            Complaint data or None if not found
        """
        df = self.data_service.get_grievances_data()
        
        if df.empty:
            return None
        
        # Check for both 'id' and 'complaint_id' for backward compatibility
        id_col = 'complaint_id' if 'complaint_id' in df.columns else 'id'
        
        complaint = df[df[id_col].astype(str) == str(complaint_id)]
        
        if complaint.empty:
            return None
        
        return complaint.iloc[0].to_dict()
    
    def get_statistics(self, group_by: str = "status") -> Dict[str, Any]:
        """
        Get complaint statistics grouped by specified field.
        
        Args:
            group_by: Field to group by (status, ward, issue_type)
            
        Returns:
            Aggregated statistics
        """
        df = self.data_service.get_grievances_data()
        
        # Map frontend 'area' to backend 'ward'
        actual_group_by = 'ward' if group_by == 'area' else group_by
        
        if df.empty or actual_group_by not in df.columns:
            return {"data": []}
        
        id_col = 'complaint_id' if 'complaint_id' in df.columns else 'id'
        
        stats = df.groupby(actual_group_by).agg({
            id_col: 'count'
        }).rename(columns={id_col: 'count'}).reset_index()
        
        return {
            "data": stats.to_dict('records'),
            "grouped_by": group_by
        }
