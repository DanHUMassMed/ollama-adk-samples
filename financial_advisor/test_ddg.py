# test_ddg.py
import sys
import logging
from pprint import pprint

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError as e:
        print(f"Failed to import DDGS: {e}")
        sys.exit(1)

def main():
    print("Testing DDGS...")
    try:
        ddg = DDGS()
        results = list(ddg.text("Apple stock news April 2026", max_results=3))
        pprint(results)
        print("Success!")
    except Exception as e:
        print(f"Error during search: {e}")

if __name__ == "__main__":
    main()
