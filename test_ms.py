import asyncio
import websockets
import base64
import json

# Load TV IP from config file
with open("tv_ip.json", "r") as f:
    config = json.load(f)
TV_IP = config["tv_ip"]

async def check_multiscreen():
    # Encode a friendly name like "KaliTest" into Base64
    client_name = base64.b64encode(b"KaliTest").decode("utf-8")
    uri = f"ws://{TV_IP}:8001/api/v2/channels/samsung.remote.control?name={client_name}"

    try:
        async with websockets.connect(uri) as websocket:
            print("[+] Connected successfully to port 8001!")
            response = await websocket.recv()
            print(f"[<] Received: {response}")
    except Exception as e:
        print(f"[-] Connection failed: {e}")

asyncio.run(check_multiscreen())
