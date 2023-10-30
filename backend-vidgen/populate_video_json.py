import os
import json
import requests

def main():
    # Get the base URL from the environment variable
    # BASE_URL = os.environ.get('MY_VARIABLE_1')
    BASE_URL = 'https://api.myconfessions.co.za'
    
    if BASE_URL is None:
        print("Environment variable MY_VARIABLE_1 is not set.")
        return

    # Define the API endpoint URL
    endpoint_url = f"{BASE_URL}/process-images/"

    try:
        # Make a GET request to the API endpoint
        # response = requests.get(endpoint_url, verify=False) # For testing
        response = requests.get(endpoint_url) # For production
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Write the data to video.json, overwriting it if it exists
            with open('video.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print("Data written to video.json")
        else:
            print(f"Failed to retrieve data from {endpoint_url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
