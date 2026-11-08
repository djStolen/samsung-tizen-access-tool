import requests
import json

# Load TV IP from config file
with open("tv_ip.json", "r") as f:
    config = json.load(f)
TV_IP = config["tv_ip"]

url = f"http://{TV_IP}:7678/nservice/"
response = requests.get(url)
print(response.status_code, response.text)
