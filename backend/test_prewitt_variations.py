#!/usr/bin/env python3
"""
Test des variations du filtre Prewitt avec la methode existante
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_prewitt_variations():
    """Test Prewitt: vertical, horizontal, combine"""
    print("TEST PREWITT VARIATIONS")
    print("=" * 40)
    
    filename = "16-Flair_brain0003.png"
    
    # 1. Test Prewitt VERTICAL (Gx)
    print("\n1. PREWITT VERTICAL")
    payload = {
        "filename": filename,
        "operation": "edge_prewitt",
        "params": {"direction": "vertical"}
    }
    
    response = requests.post(f"{BASE_URL}/process", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Succes: {result['output_file']}")
    else:
        print(f"Erreur: {response.text}")
    
    # 2. Test Prewitt HORIZONTAL (Gy)
    print("\n2. PREWITT HORIZONTAL")
    payload = {
        "filename": filename,
        "operation": "edge_prewitt", 
        "params": {"direction": "horizontal"}
    }
    
    response = requests.post(f"{BASE_URL}/process", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Succes: {result['output_file']}")
    else:
        print(f"Erreur: {response.text}")
    
    # 3. Test Prewitt COMBINE (magnitude)
    print("\n3. PREWITT COMBINE")
    payload = {
        "filename": filename,
        "operation": "edge_prewitt",
        "params": {"direction": "combined"}  # ou pas de params pour defaut
    }
    
    response = requests.post(f"{BASE_URL}/process", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Succes: {result['output_file']}")
    else:
        print(f"Erreur: {response.text}")

if __name__ == "__main__":
    test_prewitt_variations()