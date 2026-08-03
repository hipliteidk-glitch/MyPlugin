#!/usr/bin/env python3
import requests
import sys
import json
import urllib.parse

BASE_URL = "http://192.168.50.50:18081"

def send_lua(code):
    """Send Lua code to the HTTP server and get the result"""
    try:
        # Send command
        response = requests.post(
            f"{BASE_URL}/cmd",
            data=code,
            timeout=5,
            headers={"Content-Type": "text/plain"}
        )
        
        if response.status_code == 200:
            result = response.text.strip()
            if result:
                print(result)
            else:
                print("(no output)")
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server at " + BASE_URL)
    except Exception as e:
        print(f"Error: {e}")

def test_server():
    """Test if the HTTP server is running"""
    try:
        response = requests.get(f"{BASE_URL}/cmd", timeout=3)
        print(f"Server status: {response.status_code}")
        if response.text:
            print(f"Response preview: {response.text[:100]}")
        return True
    except Exception as e:
        print(f"Server not reachable: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python http_cmd.py test              - Test connection")
        print("  python http_cmd.py 'print(1+1)'     - Send Lua code")
        print("  python http_cmd.py 'return 42'      - Get return value")
        sys.exit(1)
    
    if sys.argv[1] == "test":
        test_server()
    else:
        code = " ".join(sys.argv[1:])
        send_lua(code)
