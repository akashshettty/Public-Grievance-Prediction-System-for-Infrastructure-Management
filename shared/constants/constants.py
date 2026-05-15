"""Shared constants and enumerations."""

# Issue Types
ISSUE_TYPES = [
    'Road Infrastructure',
    'Drainage System',
    'Water Supply',
    'Streetlight & Utilities',
    'Traffic & Transport',
    'Sanitation',
    'Parks & Recreation',
    'Other'
]

# Complaint Status
COMPLAINT_STATUS = [
    'open',
    'in_progress',
    'on_hold',
    'closed',
    'rejected'
]

# Risk Levels
RISK_LEVELS = [
    'Low',
    'Medium',
    'High',
    'Critical'
]

# Response Status
RESPONSE_STATUS = {
    'SUCCESS': 200,
    'CREATED': 201,
    'BAD_REQUEST': 400,
    'UNAUTHORIZED': 401,
    'FORBIDDEN': 403,
    'NOT_FOUND': 404,
    'SERVER_ERROR': 500
}
