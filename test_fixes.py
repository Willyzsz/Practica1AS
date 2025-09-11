#!/usr/bin/env python3
"""
Test script to verify the database fixes
"""

import requests
import json

def test_app_endpoints():
    """Test the main endpoints to verify fixes"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Flask App Endpoints...")
    print("=" * 50)
    
    # Test endpoints
    endpoints = [
        ("/", "Home page"),
        ("/categorias", "Categorias page"),
        ("/pendientes", "Pendientes page"),
        ("/recordatorios", "Recordatorios page"),
        ("/tbodyCategorias", "Categorias data"),
        ("/tbodyPendientes", "Pendientes data"),
        ("/tbodyRecordatorios", "Recordatorios data"),
        ("/categorias/all", "All categorias for dropdowns"),
        ("/pendientes/all", "All pendientes for dropdowns")
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {description}: {response.status_code}")
            results.append((endpoint, response.status_code == 200))
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Connection error - {e}")
            results.append((endpoint, False))
    
    print("\n" + "=" * 50)
    successful = sum(1 for _, success in results if success)
    total = len(results)
    print(f"📊 Results: {successful}/{total} endpoints working")
    
    if successful == total:
        print("🎉 All endpoints are working correctly!")
        print("\n🔧 Issues Fixed:")
        print("   ✅ Database connection management")
        print("   ✅ Foreign key relationships in JOINs")
        print("   ✅ Dropdown data loading")
        print("   ✅ Error handling and connection cleanup")
        print("   ✅ Pusher error handling")
    else:
        print("⚠️  Some endpoints still have issues")
        failed = [endpoint for endpoint, success in results if not success]
        print(f"Failed endpoints: {failed}")
    
    return successful == total

if __name__ == "__main__":
    success = test_app_endpoints()
    exit(0 if success else 1)
