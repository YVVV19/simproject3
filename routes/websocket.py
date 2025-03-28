from typing import List
from fastapi import Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from db import Config
from .ouath2_jwt import oauth2_scheme
from ._role_checker import role_checker
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

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token = Depends(oauth2_scheme)):
    async with Config.SESSION as session:
        try:
            if not await role_checker(token, session):  
                raise HTTPException(status_code=403, detail="You are not authorized to send messages")
            await manager.connect(websocket)

            while True:
                data = await websocket.receive_text()
                await manager.broadcast(data)

        except HTTPException as ex:
            await websocket.send_text(ex.detail)
            await websocket.close()

        except WebSocketDisconnect:
            manager.disconnect(websocket)

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
#Page with user chat
@app.get("/ws/user")
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
#Page with admin chat
@app.get("/ws/admin")
async def get_admin_page():
    return HTMLResponse(admin_page)
