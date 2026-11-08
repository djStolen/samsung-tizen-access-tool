import asyncio
import websockets
import base64
import ssl
import json

# Load TV IP from config file
with open("tv_ip.json", "r") as f:
    config = json.load(f)
TV_IP = config["tv_ip"]

async def check_secure():
    # Create an SSL context that ignores self-signed certificate errors common on IoT devices
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    client_name = base64.b64encode(b"KaliTest").decode("utf-8")
    uri = f"wss://{TV_IP}:8002/api/v2/channels/samsung.remote.control?name={client_name}"

    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            print("[+] Connected securely to port 8002!")
            response = await websocket.recv()
            print(f"[<] Received: {response}")
    except Exception as e:
        print(f"[-] Secure connection failed: {e}")

asyncio.run(check_secure())
