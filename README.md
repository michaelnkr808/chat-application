# Chat App

A basic user-to-user chat application built with Python using socket programming.
This project demonstrates real-time communication between clients via a central server and modular Python design.

## Features

- Server-client architecture using Python sockets
- Real-time messaging between multiple clients
- Modular structure with reusable utility functions
- Username validation and message formatting

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
└── README.md
```

### Getting Started

Running the Server:
```
python server/server.py
```
Running the Client:

In a new terminal:
```
python client/client.py
```

### Prerequisites
- Python 3.8+ installed
- Basic knowledge of command line

### Usage

- Start the server
- Run one or more clients
- Enter a username and start sending messages

### Utilities

- Validates username to ensure uniformity on server