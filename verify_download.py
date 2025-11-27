import requests

url = 'http://127.0.0.1:5000/download/protocol_template.json'

try:
    response = requests.get(url)
    if response.status_code == 200:
        print("Success! Downloaded protocol template.")
        if "experiment_id" in response.text:
            print("Verification Passed: Content looks correct.")
        else:
            print("Verification Failed: Content does not match expected JSON.")
    else:
        print(f"Failed with status code: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
