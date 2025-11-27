import requests

url = 'http://127.0.0.1:5000/validate'
files = {
    'protocol': open('bad_protocol.json', 'rb'),
    'log': open('experiment_log_template.csv', 'rb')
}

try:
    response = requests.post(url, files=files)
    if response.status_code == 200:
        if "Ethics approval is pending" in response.text:
            print("Verification Passed: Correctly identified missing ethics approval.")
        else:
            print("Verification Failed: Did not find expected error message.")
            print(response.text)
    else:
        print(f"Failed with status code: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
finally:
    files['protocol'].close()
    files['log'].close()
