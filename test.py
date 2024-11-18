import requests

data = {"ic": "041121070023"}
response = requests.post('http://localhost:6000/register_fingerprint', json=data)
print(response.json())