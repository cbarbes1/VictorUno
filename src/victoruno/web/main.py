"""Web interface for VictorUno using FastAPI."""

import asyncio
import logging
from pathlib import Path
from typing import List, Optional
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ..core.agent import VictorUnoAgent
from ..core.config import Config

logger = logging.getLogger(__name__)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    thread_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    thread_id: str

class FileUploadResponse(BaseModel):
    filename: str
    message: str
    success: bool


class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


# Initialize FastAPI app
app = FastAPI(
    title="VictorUno Web Interface",
    description="Web interface for VictorUno personal AI assistant",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
config = Config.from_env()
agent = VictorUnoAgent(config)
manager = ConnectionManager()

# Create static files directory
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VictorUno - Personal AI Assistant</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #1a1a1a;
                color: #ffffff;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .chat-container {
                display: flex;
                height: 600px;
                border: 1px solid #333;
                border-radius: 8px;
                overflow: hidden;
            }
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background-color: #2a2a2a;
            }
            .message {
                margin-bottom: 15px;
                padding: 10px;
                border-radius: 8px;
            }
            .user-message {
                background-color: #0066cc;
                text-align: right;
            }
            .ai-message {
                background-color: #444;
            }
            .input-area {
                padding: 20px;
                background-color: #333;
                border-top: 1px solid #555;
            }
            .input-group {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex: 1;
                padding: 10px;
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #2a2a2a;
                color: #ffffff;
            }
            button {
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                background-color: #0066cc;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #0052a3;
            }
            .file-upload {
                margin-top: 10px;
            }
            input[type="file"] {
                color: #ffffff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 VictorUno</h1>
                <p>Personal AI Assistant for Research, Development, and Optimization</p>
            </div>
            
            <div class="chat-container">
                <div class="chat-messages" id="messages">
                    <div class="message ai-message">
                        <strong>VictorUno:</strong> Hello! I'm your personal AI assistant. How can I help you today?
                    </div>
                </div>
            </div>
            
            <div class="input-area">
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()">Send</button>
                </div>
                <div class="file-upload">
                    <input type="file" id="fileInput" accept=".pdf,.txt,.docx,.md" onchange="uploadFile()">
                    <label for="fileInput">📎 Upload Document</label>
                </div>
            </div>
        </div>

        <script>
            const ws = new WebSocket(`ws://localhost:${window.location.port}/ws`);
            const messages = document.getElementById('messages');
            const messageInput = document.getElementById('messageInput');

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                addMessage(data.message, 'ai-message', 'VictorUno');
            };

            function addMessage(text, className, sender) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${className}`;
                messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
                messages.appendChild(messageDiv);
                messages.scrollTop = messages.scrollHeight;
            }

            function sendMessage() {
                const message = messageInput.value.trim();
                if (message) {
                    addMessage(message, 'user-message', 'You');
                    ws.send(JSON.stringify({
                        type: 'chat',
                        message: message,
                        thread_id: 'web_session'
                    }));
                    messageInput.value = '';
                }
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            async function uploadFile() {
                const fileInput = document.getElementById('fileInput');
                const file = fileInput.files[0];
                if (file) {
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    try {
                        const response = await fetch('/upload', {
                            method: 'POST',
                            body: formData
                        });
                        const result = await response.json();
                        addMessage(result.message, 'ai-message', 'System');
                    } catch (error) {
                        addMessage('Error uploading file: ' + error.message, 'ai-message', 'System');
                    }
                    
                    fileInput.value = '';
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "chat":
                message = data.get("message", "")
                thread_id = data.get("thread_id", "web_session")
                
                if message:
                    try:
                        response = await agent.chat(message, thread_id)
                        await manager.send_personal_message(
                            f'{{"message": "{response}"}}',
                            websocket
                        )
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        await manager.send_personal_message(
                            f'{{"message": "Sorry, I encountered an error: {str(e)}"}}',
                            websocket
                        )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """REST endpoint for chat messages."""
    try:
        response = await agent.chat(chat_message.message, chat_message.thread_id)
        return ChatResponse(response=response, thread_id=chat_message.thread_id)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a document."""
    try:
        # Check file size
        if file.size > config.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {config.max_file_size} bytes."
            )
        
        # Check file format
        file_extension = Path(file.filename).suffix.lower().lstrip('.')
        if file_extension not in config.supported_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported formats: {config.supported_formats}"
            )
        
        # Save file
        file_path = config.documents_dir / f"{uuid.uuid4()}_{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document
        result = await agent.process_document(file_path)
        
        return FileUploadResponse(
            filename=file.filename,
            message=result,
            success=True
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "VictorUno", "version": "0.1.0"}


async def run_web_server():
    """Run the web server."""
    import uvicorn
    
    logger.info(f"Starting VictorUno web server on {config.web_host}:{config.web_port}")
    
    uvicorn_config = uvicorn.Config(
        app,
        host=config.web_host,
        port=config.web_port,
        log_level="info"
    )
    
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_web_server())