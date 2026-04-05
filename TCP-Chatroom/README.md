# TCP Chat Room
A multithreaded TCP chat server and client built in Python using the `socket` and `threading` modules. Multiple users can connect simultaneously, exchange messages in real time, and use commands to manage their session. I built this project to strengthen my understanding of TCP socket programming, client-server architecture, and multithreading.

---

## Features
- Multi-client support using Python threads — one thread per connected client
- Nickname assignment on connection
- Broadcasts messages to all connected clients in real time
- `/list` command to display all currently connected users
- `/quit` command for clean client disconnection with server notification
- Graceful server shutdown with `Ctrl+C`

---

## Project Structure

```
tcp-chat/
├── README.md
├── server.py
└── client.py
```

---

## Requirements
- Windows, macOS, or Linux
- Python 3.10 or higher
- No external dependencies — standard library only (`socket`, `threading`, `sys`)

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Git installed on your system

### Step 1 — Clone the repository

```
git clone https://github.com/andruakadrew/network-programming.git
cd network-programming/tcp-chat
```

---

## Usage

### Step 1 — Start the server

```
python server.py
```

### Step 2 — Connect clients

Open a separate terminal for each client:

```
python client.py
```

Each client will be prompted to enter a nickname on connection.

### Step 3 — Available commands

| Command | Description |
|---|---|
| `/list` | Display all currently connected users |
| `/quit` | Disconnect from the chat room |

### Step 4 — Stop the server

Press `Ctrl+C` in the server terminal to shut down.

---

## Example Output

**Server**

```
Server is listening...
Connected with ('127.0.0.1', 56466)
Nickname of client: amorales180
Connected with ('127.0.0.1', 56472)
Nickname of client: jcosta99
Connected with ('127.0.0.1', 56485)
Nickname of client: tbouffard1
Server shutting down.
```

**Client**

```
Choose your nickname: amorales180
amorales180 joined the chat!
Connected to the server!
amorales180: hey, anyone here?
jcosta99: yeah im here
tbouffard1: same
Online users: amorales180, jcosta99, tbouffard1
amorales180: later guys
You left the chat.
```

---

Developed on Python 3.13 / PowerShell / Windows
