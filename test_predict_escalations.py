#!/usr/bin/env python
"""Test script to debug predict_escalations."""

import sys
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("1. Importing AIService...")
    from backend.services.ai_service import AIService
    print("   ✓ AIService imported")
    
    print("\n2. Creating AIService instance...")
    ai_service = AIService()
    print("   ✓ AIService instance created")
    
    print("\n3. Calling predict_escalations()...")
    result = ai_service.predict_escalations()
    print("   ✓ predict_escalations() completed")
    
    print("\n4. Result preview:")
    if 'error' in result:
        print(f"   ERROR: {result['error']}")
    else:
        print(f"   Risks count: {len(result.get('risks', []))}")
        print(f"   Stats: {result.get('stats', {})}")
        if result.get('risks'):
            print(f"   First risk: {result['risks'][0]}")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    traceback.print_exc()
