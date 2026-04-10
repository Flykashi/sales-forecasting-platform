"""
Testing script for the Sales Forecasting API
Run this after starting the Flask server
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:5000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")

def test_health():
    """Test health endpoint"""
    print_header("Testing Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed - Status: {data.get('status')}")
            return True
        else:
            print_error(f"Health check failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_root():
    """Test root endpoint"""
    print_header("Testing Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"API is running - Version: {data.get('version')}")
            print_info(f"Available endpoints: {len(data.get('endpoints', {}))}")
            return True
        return False
    except Exception as e:
        print_error(f"Root endpoint error: {str(e)}")
        return False

def test_single_prediction():
    """Test single prediction endpoint"""
    print_header("Testing Single Prediction")
    
    test_data = {
        "store": 1,
        "day_of_week": 2,
        "date": "2024-07-15",
        "promo": 1,
        "school_holiday": 0,
        "state_holiday": "0",
        "store_type": "b",
        "assortment": "b",
        "competition_distance": 500.0,
        "promo2": 0,
        "competition_open_years": 5,
        "promo2_running_years": 0
    }
    
    try:
        print_info(f"Sending prediction request for Store {test_data['store']}")
        response = requests.post(
            f"{BASE_URL}/api/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Prediction successful")
                print_info(f"Predicted Sales: {data.get('prediction')}")
                print_info(f"Store: {data.get('store')}, Date: {data.get('date')}")
                return True
            else:
                print_error(f"Prediction failed: {data.get('error')}")
                return False
        else:
            print_error(f"Request failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Prediction error: {str(e)}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print_header("Testing Batch Prediction")
    
    batch_data = {
        "predictions": [
            {
                "store": 1,
                "day_of_week": 2,
                "date": "2024-07-15",
                "promo": 1,
                "competition_distance": 500.0
            },
            {
                "store": 2,
                "day_of_week": 3,
                "date": "2024-07-16",
                "promo": 0,
                "competition_distance": 1000.0
            },
            {
                "store": 3,
                "day_of_week": 4,
                "date": "2024-07-17",
                "promo": 1,
                "competition_distance": 250.0
            }
        ]
    }
    
    try:
        print_info(f"Sending batch request for {len(batch_data['predictions'])} stores")
        response = requests.post(
            f"{BASE_URL}/api/predict/batch",
            json=batch_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Batch prediction successful")
                print_info(f"Total predictions: {data.get('total_predictions')}")
                print_info(f"Average prediction: {data.get('average_prediction')}")
                print_info(f"Min: {data.get('min_prediction')}, Max: {data.get('max_prediction')}")
                return True
            else:
                print_error(f"Batch prediction failed: {data.get('error')}")
                return False
        else:
            print_error(f"Request failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Batch prediction error: {str(e)}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print_header("Testing Model Info")
    try:
        response = requests.get(f"{BASE_URL}/api/insights/model-info")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Model info retrieved")
                print_info(f"Model Type: {data.get('model_type')}")
                print_info(f"Features: {data.get('n_features')}")
                print_info(f"Estimators: {data.get('n_estimators')}")
                print_info(f"Max Depth: {data.get('max_depth')}")
                return True
            return False
        return False
    except Exception as e:
        print_error(f"Model info error: {str(e)}")
        return False

def test_required_fields():
    """Test required fields endpoint"""
    print_header("Testing Required Fields")
    try:
        response = requests.get(f"{BASE_URL}/api/insights/required-fields")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                fields = data.get('required_fields', {})
                print_success(f"Required fields retrieved")
                print_info(f"Total fields: {len(fields)}")
                for i, (field, info) in enumerate(list(fields.items())[:3]):
                    print_info(f"  - {field}: {info.get('description')}")
                print_info(f"  ... and {len(fields) - 3} more fields")
                return True
            return False
        return False
    except Exception as e:
        print_error(f"Required fields error: {str(e)}")
        return False

def test_example():
    """Test example endpoint"""
    print_header("Testing Example")
    try:
        response = requests.get(f"{BASE_URL}/api/insights/example")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success(f"Example retrieved")
                print_info(f"Example input keys: {len(data.get('example_input', {}))}")
                print_info(f"Example output prediction: {data.get('example_output', {}).get('prediction')}")
                return True
            return False
        return False
    except Exception as e:
        print_error(f"Example error: {str(e)}")
        return False

def test_features():
    """Test features endpoint"""
    print_header("Testing Model Features")
    try:
        response = requests.get(f"{BASE_URL}/api/insights/features")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                features = data.get('features', [])
                print_success(f"Features retrieved")
                print_info(f"Total features: {len(features)}")
                print_info(f"Sample features: {features[:5]}")
                return True
            return False
        return False
    except Exception as e:
        print_error(f"Features error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print_header("SALES FORECASTING API - TEST SUITE")
    print_info(f"Base URL: {BASE_URL}")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to {BASE_URL}")
        print_info("Make sure the Flask server is running: python app.py")
        return
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Model Info", test_model_info),
        ("Required Fields", test_required_fields),
        ("Example", test_example),
        ("Model Features", test_features),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        time.sleep(0.5)  # Small delay between tests
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{symbol} {test_name}: {status}{Colors.END}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    if passed == total:
        print(f"{Colors.GREEN}All {total} tests passed!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}{passed}/{total} tests passed{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

if __name__ == "__main__":
    run_all_tests()
