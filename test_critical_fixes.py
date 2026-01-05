#!/usr/bin/env python3
"""
Critical Fixes Test Script
Tests all document types end-to-end to verify fixes
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_document_type(doc_type, requirement):
    """Test a specific document type end-to-end"""
    print(f"\n🧪 Testing {doc_type.upper()} Document Type...")
    
    try:
        # Step 1: Analyze requirement
        analyze_endpoint = f"/analyze_{doc_type}" if doc_type != "user-story" else "/analyze"
        print(f"  📊 Analyzing requirement...")
        
        analyze_response = requests.post(f"{BASE_URL}{analyze_endpoint}", 
                                       json={"requirement": requirement})
        
        if analyze_response.status_code != 200:
            print(f"  ❌ Analysis failed: {analyze_response.text}")
            return False
        
        coverage_data = analyze_response.json()
        print(f"  ✅ Analysis successful")
        
        # Step 2: Generate document
        generate_endpoint = f"/generate_{doc_type}" if doc_type != "user-story" else "/generate"
        print(f"  📝 Generating document...")
        
        generate_response = requests.post(f"{BASE_URL}{generate_endpoint}", 
                                        json={
                                            "requirement": requirement,
                                            "answers": {},
                                            "coverage_analysis": coverage_data.get("coverage_analysis", {})
                                        })
        
        if generate_response.status_code != 200:
            print(f"  ❌ Generation failed: {generate_response.text}")
            return False
        
        document_data = generate_response.json()
        print(f"  ✅ Generation successful")
        
        # Step 3: Test export (Word format)
        export_endpoint = f"/export_{doc_type}/word" if doc_type != "user-story" else "/export/word"
        print(f"  📄 Testing Word export...")
        
        data_key = f"{doc_type}_data" if doc_type != "user-story" else "story_data"
        export_response = requests.post(f"{BASE_URL}{export_endpoint}", 
                                      json={
                                          data_key: document_data,
                                          "coverage_data": coverage_data,
                                          "section_images": {
                                              "test-section": [{
                                                  "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                                                  "caption": "Test image"
                                              }]
                                          }
                                      })
        
        if export_response.status_code != 200:
            print(f"  ❌ Export failed: {export_response.text}")
            return False
        
        print(f"  ✅ Export successful")
        print(f"  🎉 {doc_type.upper()} test PASSED")
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed with exception: {str(e)}")
        return False

def main():
    """Run all critical tests"""
    print("🔥 CRITICAL FIXES TEST SUITE")
    print("=" * 50)
    
    # Test data
    test_requirement = "Create a user login system with authentication and session management"
    
    # Document types to test
    document_types = [
        "user-story",
        "brd", 
        "frd",
        "srd"
    ]
    
    results = {}
    
    # Test each document type
    for doc_type in document_types:
        results[doc_type] = test_document_type(doc_type, test_requirement)
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for doc_type, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {doc_type.upper():<12} : {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Overall Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Critical fixes are working.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)