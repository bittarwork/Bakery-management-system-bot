#!/usr/bin/env python3
"""
Test Script for Bakery Management Website
This script tests the website functionality and API endpoints
"""

import requests
import time
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 30

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed:", data.get("status", "unknown"))
            return True
        else:
            print("❌ Health check failed:", response.status_code)
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_stats_endpoint():
    """Test the stats endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("stats", {})
                print("✅ Stats endpoint working:")
                print(f"   - Users: {stats.get('users', 0)}")
                print(f"   - Products: {stats.get('products', 0)}")
                print(f"   - Orders: {stats.get('orders', 0)}")
                print(f"   - Stores: {stats.get('stores', 0)}")
                return True
            else:
                print("❌ Stats endpoint failed:", data)
                return False
        else:
            print("❌ Stats endpoint error:", response.status_code)
            return False
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint"""
    try:
        test_message = "كم عدد المنتجات المتاحة؟"
        payload = {
            "message": test_message,
            "language": "ar"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Chat endpoint working")
                print(f"   - Response: {data.get('response', 'No response')[:100]}...")
                return True
            else:
                print("❌ Chat endpoint failed:", data.get("error", "Unknown error"))
                return False
        else:
            print("❌ Chat endpoint error:", response.status_code)
            return False
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return False

def test_main_page():
    """Test the main website page"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            content = response.text
            if "نظام إدارة المخبز" in content:
                print("✅ Main page loaded successfully")
                return True
            else:
                print("❌ Main page content incorrect")
                return False
        else:
            print("❌ Main page error:", response.status_code)
            return False
    except Exception as e:
        print(f"❌ Main page error: {e}")
        return False

def test_static_files():
    """Test static files loading"""
    try:
        # Test CSS file
        css_response = requests.get(f"{BASE_URL}/static/css/style.css", timeout=TEST_TIMEOUT)
        css_ok = css_response.status_code == 200
        
        # Test JS file
        js_response = requests.get(f"{BASE_URL}/static/js/app.js", timeout=TEST_TIMEOUT)
        js_ok = js_response.status_code == 200
        
        if css_ok and js_ok:
            print("✅ Static files loaded successfully")
            return True
        else:
            print(f"❌ Static files error - CSS: {css_response.status_code}, JS: {js_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Static files error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Bakery Management System Tests")
    print("=" * 50)
    
    tests = [
        ("Main Page", test_main_page),
        ("Health Endpoint", test_health_endpoint),
        ("Stats Endpoint", test_stats_endpoint),
        ("Static Files", test_static_files),
        ("Chat Endpoint", test_chat_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Website is working correctly.")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    print("🍰 Bakery Management System - Website Test")
    print(f"🌐 Testing URL: {BASE_URL}")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = run_all_tests()
    
    if success:
        print("\n✅ Website is ready for production!")
        print("🚀 You can now deploy to PythonAnywhere")
    else:
        print("\n❌ Please fix the issues before deployment")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 