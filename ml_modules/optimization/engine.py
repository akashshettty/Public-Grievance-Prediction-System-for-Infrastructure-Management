"""
Optimization Engine - Resource & Route Intelligence
Uses Dijkstra and Greedy optimization for team recommendation and route planning.
"""

import numpy as np
import heapq
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResourceOptimizationEngine:
    """
    Optimizes team scheduling, worker recommendation, and route planning.
    """
    
    def __init__(self):
        # Simulated worker/team locations and specialties
        self.teams = [
            {"id": "TEAM_01", "name": "North Road Repair", "specialty": "Road Infrastructure", "location": (13.04, 77.58), "status": "Available"},
            {"id": "TEAM_02", "name": "East Drainage Crew", "specialty": "Drainage System", "location": (12.97, 77.71), "status": "Busy"},
            {"id": "TEAM_03", "name": "Power Utility Squad", "specialty": "Streetlight & Utilities", "location": (12.91, 77.62), "status": "Available"},
            {"id": "TEAM_04", "name": "Sanitation Fleet", "specialty": "Sanitation", "location": (12.93, 77.53), "status": "Available"}
        ]

    def haversine_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calculate the great circle distance between two points in km."""
        R = 6371.0  # Earth radius in km
        lat1, lon1 = np.radians(coord1)
        lat2, lon2 = np.radians(coord2)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        return R * c

    def find_nearest_teams(self, complaint_loc: Tuple[float, float], category: str, limit: int = 2) -> List[Dict[str, Any]]:
        """
        Greedy approach to find the best available team based on proximity and specialty.
        """
        candidates = []
        for team in self.teams:
            if team['status'] == "Available":
                dist = self.haversine_distance(complaint_loc, team['location'])
                # Preference score: distance + penalty for wrong specialty
                specialty_mult = 1.0 if team['specialty'] == category else 2.5
                score = dist * specialty_mult
                
                candidates.append({
                    **team,
                    "distance_km": round(dist, 2),
                    "preference_score": round(score, 2)
                })
        
        # Sort by preference score
        candidates.sort(key=lambda x: x['preference_score'])
        return candidates[:limit]

    def plan_route(self, team_loc: Tuple[float, float], waypoints: List[Tuple[float, float]]) -> Dict[str, Any]:
        """
        Simple Greedy TSP (Nearest Neighbor) which works as a Dijkstra-lite for sequencing.
        """
        if not waypoints:
            return {"route": [], "total_distance": 0}
            
        current_pos = team_loc
        unvisited = waypoints.copy()
        route = []
        total_dist = 0.0
        
        while unvisited:
            # Find nearest point
            next_point = min(unvisited, key=lambda p: self.haversine_distance(current_pos, p))
            dist = self.haversine_distance(current_pos, next_point)
            
            total_dist += dist
            route.append(next_point)
            current_pos = next_point
            unvisited.remove(next_point)
            
        return {
            "route": route,
            "total_distance_km": round(total_dist, 2),
            "est_travel_time_mins": round(total_dist * 4, 1) # Assumed 15km/h city traffic
        }

    def estimate_repair_time(self, category: str, severity: float) -> int:
        """Estimate repair duration in hours."""
        base_times = {
            'Road Infrastructure': 24,
            'Drainage System': 8,
            'Water Supply': 4,
            'Streetlight & Utilities': 2,
            'Sanitation': 1,
            'Other': 12
        }
        base = base_times.get(category, 12)
        # Severity increases time (severity 1-5)
        return int(base * (severity / 3.0))

    def get_recommendation(self, complaint_id: str, text: str, lat: float, lon: float, category: str, severity: float) -> Dict[str, Any]:
        """
        Comprehensive recommendation for a complaint.
        """
        loc = (lat, lon)
        nearest = self.find_nearest_teams(loc, category)
        
        repair_time = self.estimate_repair_time(category, severity)
        
        team_id = nearest[0]['id'] if nearest else "BUFFER_TEAM"
        team_name = nearest[0]['name'] if nearest else "General Maintenance"
        
        # Simulated route planning
        route_plan = self.plan_route(
            nearest[0]['location'] if nearest else (12.97, 77.59),
            [loc]
        )
        
        return {
            "complaint_id": complaint_id,
            "recommended_team": team_name,
            "team_id": team_id,
            "distance_to_site_km": nearest[0]['distance_km'] if nearest else 0,
            "est_travel_time_mins": route_plan['est_travel_time_mins'],
            "est_repair_duration_hours": repair_time,
            "total_eta_hours": round(repair_time + (route_plan['est_travel_time_mins'] / 60), 1),
            "priority": "High" if severity > 4 else "Normal"
        }

if __name__ == "__main__":
    engine = ResourceOptimizationEngine()
    # Test
    rec = engine.get_recommendation("C-123", "Pothole fix", 12.95, 77.6, "Road Infrastructure", 4.5)
    print(rec)

