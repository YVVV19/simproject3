from typing import List
from fastapi import Depends, HTTPException, status, WebSocket, Request
from fastapi.responses import HTMLResponse

from main import app



class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()



user_page = """
<!DOCTYPE html>
<html>
<head><title>Chat</title></head>
<body>
    <h2>Chat Messages</h2>
    <ul id="messages"></ul>
    <script>
        let ws = new WebSocket("ws://localhost:8000/ws/user_token");
        ws.onmessage = event => {
            let messages = document.getElementById("messages");
            let li = document.createElement("li");
            li.appendChild(document.createTextNode(event.data));
            messages.appendChild(li);
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get_user_page():
    return HTMLResponse(user_page)

admin_page = """
<!DOCTYPE html>
<html>
<head><title>Admin Chat</title></head>
<body>
    <h2>Admin Chat</h2>
    <input id="message" type="text" />
    <button onclick="sendMessage()">Send</button>
    <ul id="messages"></ul>
    <script>
        let ws = new WebSocket("ws://localhost:8000/ws/admin_token");
        ws.onmessage = event => {
            let messages = document.getElementById("messages");
            let li = document.createElement("li");
            li.appendChild(document.createTextNode(event.data));
            messages.appendChild(li);
        };
        function sendMessage() {
            let input = document.getElementById("message");
            ws.send(input.value);
            input.value = "";
        }
    </script>
</body>
</html>
"""

@app.get("/admin")
async def get_admin_page():
    return HTMLResponse(admin_page)