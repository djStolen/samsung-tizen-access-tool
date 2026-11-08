# Samsung Tizen TV Controller

A Python-based controller for Samsung Tizen Smart TVs that enables remote control via WebSocket connections. Supports both secure (port 8002) and non-secure (port 8001) connections with automatic token caching for seamless subsequent connections.

## Features

- **Secure WebSocket Control** (Port 8002) with TLS encryption
- **Token Caching** - First connection prompts TV for approval, subsequent connections are automatic
- **Comprehensive Key Mapping** - 30+ predefined remote keys (navigation, media, apps, etc.)
- **CLI Interface** - Simple command-line usage with shortcut names
- **Multiple Connection Methods** - Secure, non-secure, and HTTP API testing
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Virtual Environment Setup** - Automated dependency management

## Requirements

- Python 3.7+
- Samsung Tizen TV (2016+ models) on same network
- TV Developer Mode enabled (for some models)

## Installation

### Quick Setup (Recommended)

source venv/bin/activate

pip install -r requirements.txt                                                                                                                                          

python tv_controller.py KEY_CHUP

python test_secure.py

python test_ms.py                                                                                                                                       

python test_tv.py                                                                                                                                          

python send_command.py
