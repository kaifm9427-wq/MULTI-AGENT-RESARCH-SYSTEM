#!/usr/bin/env python3
"""
Test script to verify the backend is working correctly
"""

import requests
import json
import time
import sys

def test_health_check():
    """Test the health check endpoint"""
    print("🧪 Testing health check...")
    try:
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200, f"Health check failed: {response.status_code}"
        data = response.json()
        assert data.get("status") == "ok", f"Health check returned: {data}"
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_api_query():
    """Test the main API query endpoint"""
    print("\n🧪 Testing API query endpoint...")
    try:
        payload = {
            "query": "What is cloud computing?",
            "use_gemini": False
        }
        
        response = requests.post(
            "http://localhost:8000/api/run",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        
        assert response.status_code == 200, f"API query failed: {response.status_code} - {response.text[:200]}"
        
        result = response.json()
        
        # Check required fields
        required_fields = ['query', 'steps', 'report', 'sources', 'feedback', 'usage']
        missing_fields = [field for field in required_fields if field not in result]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        # Check field content
        assert isinstance(result['query'], str) and result['query'], "Query field is empty"
        assert isinstance(result['steps'], list) and result['steps'], "Steps list is empty"
        assert isinstance(result['report'], str) and result['report'], "Report field is empty"
        assert isinstance(result['sources'], list), "Sources is not a list"
        assert isinstance(result['feedback'], str) and result['feedback'], "Feedback field is empty"
        assert isinstance(result['usage'], dict), "Usage is not a dict"
        
        print(f"✅ API query passed")
        print(f"   - Query: {result['query'][:50]}...")
        print(f"   - Steps completed: {len(result['steps'])}")
        print(f"   - Sources found: {len(result['sources'])}")
        print(f"   - Report length: {len(result['report'])} chars")
        print(f"   - Feedback score: {result['feedback'].split('Score:')[1].split('/')[0].strip() if 'Score:' in result['feedback'] else 'N/A'}")
        
        return True
        
    except Exception as e:
        print(f"❌ API query failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frontend_served():
    """Test that the frontend HTML is served"""
    print("\n🧪 Testing frontend HTML serving...")
    try:
        response = requests.get("http://localhost:8000/")
        assert response.status_code == 200, f"Frontend fetch failed: {response.status_code}"
        
        html = response.text
        required_elements = [
            'query-input',
            'run-btn',
            'results-section',
            'report-container',
            'sources-container',
            'feedback-text'
        ]
        
        missing_elements = [elem for elem in required_elements if f'id="{elem}"' not in html]
        
        if missing_elements:
            print(f"❌ Missing HTML elements: {missing_elements}")
            return False
        
        print(f"✅ Frontend HTML served correctly")
        print(f"   - HTML length: {len(html)} chars")
        print(f"   - All required elements present")
        
        return True
        
    except Exception as e:
        print(f"❌ Frontend serving failed: {e}")
        return False

def main():
    """Run all tests"""
    print("""
╔════════════════════════════════════════════════════════════╗
║            ResearchMind Backend Test Suite                 ║
╚════════════════════════════════════════════════════════════╝
""")
    
    tests = [
        test_health_check,
        test_frontend_served,
        test_api_query,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Unexpected error in test: {e}")
            results.append(False)
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║                    Test Summary                            ║
╚════════════════════════════════════════════════════════════╝

Total Tests: {len(results)}
Passed: {sum(results)}
Failed: {len(results) - sum(results)}

{'✅ All tests passed!' if all(results) else '❌ Some tests failed'}
""")
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
