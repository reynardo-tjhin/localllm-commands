"""Keep alive script"""

import time

ID="0e6a19cc157941e0b56b6a272c6eec71"
NAME="Test Script 1"
DESCRIPTION="Script for Testing No 1"

def execute():
    
    try:
        while True:
            print("test_script_1: started")
            time.sleep(5)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise