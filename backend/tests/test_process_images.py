"""
Test script for /images/process endpoint
This script tests the image processing endpoint with a sample image.
"""
import requests
import sys
import os

# API endpoint
API_URL = "http://127.0.0.1:8000/images/process"

def test_process_images():
    """Test the images/process endpoint with sample images"""
    
    # Check if image paths are provided
    if len(sys.argv) < 2:
        print("Usage: python test_process_images.py <image_path1> [image_path2] ...")
        print("Example: python test_process_images.py confession1.png confession2.png")
        return
    
    image_paths = sys.argv[1:]
    
    # Prepare files for upload
    files = []
    for path in image_paths:
        try:
            with open(path, 'rb') as f:
                files.append(('images', (path, f.read(), 'image/png')))
        except FileNotFoundError:
            print(f"Error: Image file '{path}' not found")
            return
        except Exception as e:
            print(f"Error reading '{path}': {e}")
            return
    
    # Get API key from environment
    api_key = os.getenv('API_KEY')
    headers = {'X-API-Key': api_key} if api_key else {}
    
    try:
        # Send POST request
        print(f"Sending {len(files)} image(s) to {API_URL}...")
        response = requests.post(API_URL, files=files, headers=headers)
        
        # Check response
        if response.status_code == 200:
            print("\n✓ Success! Response:")
            print("-" * 60)
            import json
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running at http://127.0.0.1:8000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_process_images()
