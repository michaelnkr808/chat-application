# Chat App

A basic user-to-user chat application built with Python using socket programming.
This project demonstrates real-time communication between clients via a central server and modular Python design.

## Features

- Server-client architecture using Python sockets
- Real-time messaging between multiple clients
- Modular structure with reusable utility functions
- Username validation and message formatting
- Transport encryption with TLS (server-authenticated; not end-to-end)

## Project Structure

```
chat-app/
├── server/ # Server-side code
│ └── server.py
├── client/ # Client-side code
│ └── client.py
├── utils/ # Helper functions
│ ├── __init__.py
│ └── common.py
├── certs/ # TLS materials (dev)
│ ├── server.crt   # public certificate (shareable)
│ └── server.key   # private key (DO NOT COMMIT)
└── README.md
```

### Getting Started

Running the Server:

In a new terminal from the project dir
```
python3 -m server.server
```
Running the Client:

In a new terminal from the project dir:
```
python3 -m client.client
```

### Prerequisites
- Python 3.8+ installed
- Basic knowledge of command line

### TLS Encryption (Transport Security)

This app encrypts traffic between the client and server using TLS. The server still sees plaintext after decryption (this is transport encryption, not end‑to‑end).

1) Generate a development certificate (for localhost)

Run in Terminal (adjust only if your path differs):

```
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout "./certs/server.key" \
  -out    "./certs/server.crt" \
  -days 365 -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost"
```

Quick checks:

```
head -2 "./certs/server.key"   # -----BEGIN PRIVATE KEY-----
head -2 "./certs/server.crt"   # -----BEGIN CERTIFICATE-----
```

2) Configure constants

In `utils/common.py` set certificate paths and hostnames (either absolute or project‑relative):

- `CERT_PATH = "./certs/server.crt"`
- `KEY_PATH  = "./certs/server.key"`
- `HOST = "localhost"` and `SERVER_HOSTNAME = "localhost"`

3) How it works (summary)

- Server loads the cert/key and wraps accepted sockets with TLS.
- Client trusts the server cert and wraps its socket with `server_hostname=localhost` for hostname verification.
- All `send`/`recv` calls are over the encrypted channel.

4) Troubleshooting

- FileNotFoundError: check `CERT_PATH` / `KEY_PATH` point to real files.
- CERTIFICATE_VERIFY_FAILED: ensure cert CN/SAN is `localhost` and client connects to `HOST = "localhost"`.
- Port in use: stop old server or change `PORT`.

Security notes:

- Do NOT commit `server.key`. Add to `.gitignore`:

```
certs/*.key
```

### Usage

- Start the server
- Run one or more clients
- Enter a username and start sending messages

### Utilities

- Validates username to ensure uniformity on server
- Contains common variables used in both the server and client