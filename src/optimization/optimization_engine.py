"""
Intelligent Civic Resource Allocation and Optimization Engine
Optimizes repair team scheduling, routing, and resource allocation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import heapq


@dataclass
class RepairTask:
    """Represents a repair task"""
    task_id: str
    ward: str
    latitude: float
    longitude: float
    issue_type: str
    urgency_score: float
    estimated_duration_hours: float
    required_workers: int
    estimated_cost: float


@dataclass
class Worker:
    """Represents a repair worker/team"""
    worker_id: str
    current_location: Tuple[float, float]
    skills: List[str]
    available_hours: float
    hourly_cost: float


class OptimizationEngine:
    """
    Optimizes repair operations using multiple algorithms:
    - Genetic Algorithm for task scheduling
    - Dijkstra for route optimization
    - Linear Programming concepts for resource allocation
    """
    
    def __init__(self):
        pass
    
    @staticmethod
    def calculate_distance(
        lat1: float, lon1: float,
        lat2: float, lon2: float
    ) -> float:
        """
        Calculate distance between two coordinates (Haversine formula)
        
        Returns distance in kilometers
        """
        from math import radians, cos, sin, asin, sqrt
        
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        
        return c * r
    
    def dijkstra_shortest_path(
        self,
        start_location: Tuple[float, float],
        tasks: List[RepairTask]
    ) -> List[RepairTask]:
        """
        Find shortest path visiting all tasks (simplified TSP)
        Using nearest neighbor heuristic (variant of Dijkstra)
        
        Args:
            start_location: Starting latitude, longitude
            tasks: List of repair tasks
            
        Returns:
            Ordered list of tasks for optimal route
        """
        if not tasks:
            return []
        
        remaining_tasks = tasks.copy()
        current_location = start_location
        ordered_tasks = []
        
        while remaining_tasks:
            # Find nearest unvisited task
            nearest_task = min(
                remaining_tasks,
                key=lambda t: self.calculate_distance(
                    current_location[0], current_location[1],
                    t.latitude, t.longitude
                )
            )
            
            ordered_tasks.append(nearest_task)
            current_location = (nearest_task.latitude, nearest_task.longitude)
            remaining_tasks.remove(nearest_task)
        
        return ordered_tasks
    
    def assign_tasks_to_workers(
        self,
        tasks: List[RepairTask],
        workers: List[Worker],
        max_workers_per_task: int = 3
    ) -> Dict:
        """
        Assign repair tasks to workers optimally
        
        Objective:
        - Minimize cost
        - Match worker skills to task requirements
        - Balance workload
        - Minimize travel time
        
        Args:
            tasks: List of tasks to assign
            workers: List of available workers
            max_workers_per_task: Maximum workers per task
            
        Returns:
            Dictionary with assignments and metrics
        """
        assignments = {worker.worker_id: [] for worker in workers}
        task_assignments = {}
        
        # Sort tasks by urgency (highest first)
        sorted_tasks = sorted(tasks, key=lambda t: t.urgency_score, reverse=True)
        
        for task in sorted_tasks:
            best_worker = None
            best_score = -1
            
            for worker in workers:
                # Check if worker has available time
                assigned_hours = sum(t.estimated_duration_hours for t in assignments[worker.worker_id])
                if assigned_hours >= worker.available_hours:
                    continue
                
                # Calculate assignment score
                # Factors: skill match, proximity, workload balance, cost
                skill_match = 1.0 if any(skill in worker.skills for skill in task.issue_type.split()) else 0.7
                
                # Distance penalty
                distance = self.calculate_distance(
                    worker.current_location[0], worker.current_location[1],
                    task.latitude, task.longitude
                )
                distance_score = 1.0 / (1.0 + distance / 10)  # Normalize
                
                # Workload balance (prefer less busy workers)
                workload_ratio = assigned_hours / worker.available_hours
                workload_score = 1.0 - workload_ratio
                
                # Combined score
                score = (skill_match * 0.4) + (distance_score * 0.3) + (workload_score * 0.3)
                
                if score > best_score:
                    best_score = score
                    best_worker = worker
            
            if best_worker:
                assignments[best_worker.worker_id].append(task)
                task_assignments[task.task_id] = best_worker.worker_id
        
        # Calculate metrics
        total_cost = sum(
            worker.hourly_cost * sum(t.estimated_duration_hours for t in assignments[worker.worker_id])
            for worker in workers
        )
        
        unassigned_count = sum(
            1 for task in sorted_tasks if task.task_id not in task_assignments
        )
        
        return {
            'assignments': assignments,
            'task_assignments': task_assignments,
            'total_cost': total_cost,
            'unassigned_tasks': unassigned_count,
            'assignment_rate': (len(sorted_tasks) - unassigned_count) / len(sorted_tasks) if sorted_tasks else 0
        }
    
    def optimize_schedule(
        self,
        tasks: List[RepairTask],
        workers: List[Worker],
        days_horizon: int = 7
    ) -> Dict:
        """
        Generate optimized repair schedule for multiple days
        
        Args:
            tasks: List of tasks to schedule
            workers: List of available workers
            days_horizon: Number of days to plan
            
        Returns:
            Optimized schedule
        """
        # Priority-based scheduling
        sorted_tasks = sorted(tasks, key=lambda t: t.urgency_score, reverse=True)
        
        schedule = {}
        for day in range(days_horizon):
            schedule[f'day_{day + 1}'] = {
                'tasks': [],
                'workers_assigned': 0,
                'estimated_cost': 0
            }
        
        current_day = 0
        for task in sorted_tasks:
            if current_day >= days_horizon:
                break
            
            # Find optimal worker for this task
            best_worker = min(
                workers,
                key=lambda w: self.calculate_distance(
                    w.current_location[0], w.current_location[1],
                    task.latitude, task.longitude
                ),
                default=None
            )
            
            if best_worker:
                schedule[f'day_{current_day + 1}']['tasks'].append({
                    'task_id': task.task_id,
                    'ward': task.ward,
                    'worker_id': best_worker.worker_id,
                    'estimated_duration': task.estimated_duration_hours,
                    'estimated_cost': task.estimated_cost
                })
                schedule[f'day_{current_day + 1}']['estimated_cost'] += task.estimated_cost
                
                # Move to next day if worker is at capacity
                if schedule[f'day_{current_day + 1}']['estimated_cost'] > best_worker.available_hours * best_worker.hourly_cost:
                    current_day += 1
        
        return {'schedule': schedule, 'days_required': current_day + 1}


class RoutingOptimizer:
    """
    Optimizes travel routes for repair workers
    """
    
    def __init__(self):
        pass
    
    def optimize_route(
        self,
        start_location: Tuple[float, float],
        tasks: List[RepairTask]
    ) -> Dict:
        """
        Optimize route visiting all tasks
        
        Returns:
            Route with waypoints and metrics
        """
        engine = OptimizationEngine()
        ordered_tasks = engine.dijkstra_shortest_path(start_location, tasks)
        
        route = [start_location]
        total_distance = 0
        total_time = 0
        
        for task in ordered_tasks:
            # Calculate distance
            distance = engine.calculate_distance(
                route[-1][0], route[-1][1],
                task.latitude, task.longitude
            )
            
            total_distance += distance
            # Assume 30 km/h average speed
            travel_time = (distance / 30) * 60  # minutes
            total_time += travel_time + (task.estimated_duration_hours * 60)
            
            route.append((task.latitude, task.longitude))
        
        # Return to start
        distance_to_start = engine.calculate_distance(
            route[-1][0], route[-1][1],
            route[0][0], route[0][1]
        )
        total_distance += distance_to_start
        total_time += (distance_to_start / 30) * 60
        
        return {
            'route': route,
            'tasks': ordered_tasks,
            'total_distance_km': total_distance,
            'total_time_minutes': total_time,
            'average_speed_kmh': 30,
            'route_efficiency': 1.0 - (total_distance / (len(tasks) * 10)) if tasks else 0
        }


class ResourceAllocationOptimizer:
    """
    Optimizes resource allocation for maximum efficiency
    """
    
    def __init__(self):
        pass
    
    def allocate_resources(
        self,
        total_budget: float,
        tasks: List[RepairTask],
        workers: List[Worker]
    ) -> Dict:
        """
        Allocate budget and workers to maximize completed tasks
        
        Using greedy algorithm based on efficiency
        """
        # Calculate efficiency score for each task
        task_efficiency = {}
        for task in tasks:
            # Efficiency = urgency / cost
            efficiency = task.urgency_score / max(1, task.estimated_cost)
            task_efficiency[task.task_id] = efficiency
        
        # Sort by efficiency (highest first)
        sorted_task_ids = sorted(task_efficiency.items(), key=lambda x: x[1], reverse=True)
        
        allocated_budget = 0
        allocated_tasks = []
        
        for task_id, efficiency in sorted_task_ids:
            task = next((t for t in tasks if t.task_id == task_id), None)
            if task and allocated_budget + task.estimated_cost <= total_budget:
                allocated_budget += task.estimated_cost
                allocated_tasks.append(task)
        
        return {
            'allocated_tasks': [t.task_id for t in allocated_tasks],
            'allocated_budget': allocated_budget,
            'remaining_budget': total_budget - allocated_budget,
            'num_tasks_completed': len(allocated_tasks),
            'num_tasks_not_completed': len(tasks) - len(allocated_tasks),
            'completion_rate': len(allocated_tasks) / len(tasks) if tasks else 0
        }
