import asyncio
import websockets
import base64
import json
import ssl
import os
import argparse

# Load TV IP from config file
with open("tv_ip.json", "r") as f:
    config = json.load(f)
TV_IP = config["tv_ip"]

TOKEN_FILE = "tv_token.json"
CLIENT_NAME = base64.b64encode(b"KaliStreamlinedController").decode("utf-8")

# Comprehensive Samsung Tizen Remote Keys Reference
COMMON_KEYS = {
    # Power & Source
    "power": "KEY_POWER",
    "source": "KEY_SOURCE",
    "menu": "KEY_MENU",
    "guide": "KEY_GUIDE",
    "info": "KEY_INFO",
    "tools": "KEY_TOOLS",
    
    # Navigation & Selection
    "home": "KEY_HOME",
    "up": "KEY_UP",
    "down": "KEY_DOWN",
    "left": "KEY_LEFT",
    "right": "KEY_RIGHT",
    "enter": "KEY_ENTER",
    "return": "KEY_RETURN",
    "exit": "KEY_EXIT",
    
    # Audio & Channels
    "volup": "KEY_VOLUP",
    "voldown": "KEY_VOLDOWN",
    "mute": "KEY_MUTE",
    "chup": "KEY_CHUP",
    "chdown": "KEY_CHDOWN",
    
    # Playback & Media
    "play": "KEY_PLAY",
    "pause": "KEY_PAUSE",
    "stop": "KEY_STOP",
    "ff": "KEY_FF",
    "rewind": "KEY_REWIND",
    
    # App Shortcuts (varies by model firmware)
    "netflix": "KEY_NETFLIX",
    "youtube": "KEY_YOUTUBE",
    "prime": "KEY_AMAZON"
}

def load_token():
    """Load cached token from local file if it exists."""
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
                return data.get("token")
        except Exception:
            pass
    return None

def save_token(token):
    """Save the token to disk for future passwordless sessions."""
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f)
    print(f"[+] Token successfully cached to {TOKEN_FILE}")

async def get_connection_uri():
    """Build URI with cached token if available, otherwise initiate pairing."""
    token = load_token()
    if token:
        return f"wss://{TV_IP}:8002/api/v2/channels/samsung.remote.control?name={CLIENT_NAME}&token={token}"
    else:
        print("[*] No saved token found. A confirmation prompt will appear on your TV screen.")
        return f"wss://{TV_IP}:8002/api/v2/channels/samsung.remote.control?name={CLIENT_NAME}"

async def send_command(key_code):
    """Connect to the TV securely and send the specified key command."""
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    uri = await get_connection_uri()
    
    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            print(f"[+] Connected to Samsung TV at {TV_IP}")
            
            # Receive initial connection payload from TV
            response = await websocket.recv()
            data = json.loads(response)
            
            # Extract and cache new token if provided
            if "data" in data and "token" in data["data"]:
                new_token = data["data"]["token"]
                if not load_token() or load_token() != new_token:
                    save_token(new_token)
            
            # Construct command payload
            payload = json.dumps({
                "method": "ms.remote.control",
                "params": {
                    "Cmd": "Click",
                    "DataOfCmd": key_code,
                    "Option": "false",
                    "TypeOfRemote": "SendRemoteKey"
                }
            })
            
            # Send command
            await websocket.send(payload)
            print(f"[+] Command sent successfully: {key_code}")
            await asyncio.sleep(0.5)
            
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"[-] Connection closed (Code {e.code}). If this is a first run, ensure you accept the pairing prompt on your TV screen.")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Streamlined Samsung Tizen TV Remote Controller")
    parser.add_argument("command", nargs="?", default="info", help="Shortcut name (e.g. mute, home, netflix) or raw key (e.g. KEY_MUTE)")
    args = parser.parse_args()

    # Map shortcut to exact key or fallback to raw uppercase input
    cmd_lower = args.command.lower()
    if cmd_lower in COMMON_KEYS:
        key_code = COMMON_KEYS[cmd_lower]
    else:
        key_code = args.command.upper()
        if not key_code.startswith("KEY_"):
            key_code = f"KEY_{key_code}"

    print(f"[*] Executing command -> {key_code}")
    asyncio.run(send_command(key_code))

if __name__ == "__main__":
    main()
