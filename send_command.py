import asyncio
import websockets
import base64
import json
import ssl

# Load TV IP from config file
with open("tv_ip.json", "r") as f:
    config = json.load(f)
TV_IP = config["tv_ip"]

async def send_key():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    client_name = base64.b64encode(b"KaliTest").decode("utf-8")
    token = "15440995" # Your generated token from the pairing response

    uri = f"wss://{TV_IP}:8002/api/v2/channels/samsung.remote.control?name={client_name}&token={token}"

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        print("[+] Connected using token! Sending command...")

        # Payload to simulate clicking the Mute key
        payload = json.dumps({
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": "KEY_MUTE",
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey"
            }
        })

        await websocket.send(payload)
        await asyncio.sleep(1)
        print("[+] Command sent successfully without prompting the TV screen!")

asyncio.run(send_key())
