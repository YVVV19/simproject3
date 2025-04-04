from typing import List
from fastapi import Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse

from .ouath2_jwt import oauth2_scheme
from ._role_checker import role_checker
from main import app

connections: List[WebSocket] = []

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple WebSocket Chat</title>
</head>
<body>
    <h1>WebSocket Chat</h1>
    <div id='messages'></div>
    <input type='text' id='messageInput'>
    <button onclick='sendMessage()'>Send</button>

    <script>
        const websocket = new WebSocket("ws://localhost:8000/ws");
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');

        websocket.onopen = function(event) {
            console.log("WebSocket connection opened");
        };

        websocket.onmessage = function(event) {
            const message = document.createElement('div');
            message.textContent = event.data;
            messagesDiv.appendChild(message);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        };

        websocket.onclose = function(event) {
            console.log("WebSocket connection closed");
        };

        websocket.onerror = function(event) {
            console.error("WebSocket error:", event);
        };

        function sendMessage() {
            if (websocket.readyState === WebSocket.OPEN) {
                const message = messageInput.value;
                websocket.send(message);
                messageInput.value = '';
            } else {
                console.error("WebSocket is not open.");
            }
        }
    </script>
</body>
</html>
"""

@app.get("/websocket")
async def get():
    return HTMLResponse(html)

async def broadcast(message: str):
    for connection in connections:
        try:
            await connection.send_text(message)
        except RuntimeError as e:
            print(f"Error sending message to connection {connection}: {e}")
            connections.remove(connection)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(f"Organisation: {data}")
    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket}")
        connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error for connection {websocket}: {e}")
        if websocket in connections:
            connections.remove(websocket)