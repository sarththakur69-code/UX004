import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_health():
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"Health: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Health Check Failed: {e}")

def test_scan_no_auth():
    try:
        r = requests.post(f"{BASE_URL}/scan", json={"url": "https://example.com"})
        print(f"Scan (No Auth): {r.status_code}") # Expect 401
    except Exception as e:
        print(f"Scan (No Auth) Failed: {e}")

def test_scan_with_auth():
    try:
        headers = {"x-api-key": "ux_test_12345"}
        r = requests.post(f"{BASE_URL}/scan", json={"url": "https://example.com"}, headers=headers)
        print(f"Scan (Auth): {r.status_code}") # Expect 200
        if r.status_code == 200:
            print("Scan Result Keys:", r.json().keys())
    except Exception as e:
        print(f"Scan (Auth) Failed: {e}")

if __name__ == "__main__":
    test_health()
    test_scan_no_auth()
    test_scan_with_auth()
