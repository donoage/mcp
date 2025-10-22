import os
import asyncio
from datetime import date
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStdio
import json
import markdown
import time
from collections import deque

load_dotenv()

# Rate limiting
class RateLimiter:
    def __init__(self, max_requests=5, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
    
    async def acquire(self):
        now = time.time()
        # Remove old requests outside the time window
        while self.requests and self.requests[0] < now - self.time_window:
            self.requests.popleft()
        
        if len(self.requests) >= self.max_requests:
            wait_time = self.requests[0] + self.time_window - now
            if wait_time > 0:
                return False, wait_time
        
        self.requests.append(now)
        return True, 0

rate_limiter = RateLimiter(max_requests=3, time_window=60)  # 3 requests per minute

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ------------- MCP Server Factory -------------
def create_polygon_mcp_server():
    """Create Polygon.io MCP server"""
    print("[MCP] Creating Polygon.io MCP server...")
    polygon_api_key = os.getenv("POLYGON_API_KEY")
    if not polygon_api_key:
        print("[MCP] ERROR: POLYGON_API_KEY not found")
        raise Exception("POLYGON_API_KEY is not set in the environment or .env file.")
    
    print(f"[MCP] POLYGON_API_KEY found: {polygon_api_key[:10]}...")
    env = os.environ.copy()
    env["POLYGON_API_KEY"] = polygon_api_key
    
    # Use official Polygon.io MCP server
    print("[MCP] Initializing MCPServerStdio with uvx...")
    return MCPServerStdio(
        command="uvx",
        args=[
            "--from",
            "git+https://github.com/polygon-io/mcp_polygon@v0.4.0",
            "mcp_polygon"
        ],
        env=env
    )

# ------------- Agent Setup -------------
def create_agent():
    server = create_polygon_mcp_server()
    agent = Agent(
        model="anthropic:claude-sonnet-4-5-20250929",
        mcp_servers=[server],
        system_prompt=(
            "You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. "
            "Use the latest data available. Always double check your math. "
            "For any questions about the current date, use the 'get_today_date' tool. "
            "For long or complex queries, break the query into logical subtasks and process each subtask in order."
        )
    )
    
    # Add custom tool for today's date
    @agent.tool
    def get_today_date(ctx: RunContext) -> str:
        """Returns today's date in YYYY-MM-DD format."""
        return str(date.today())
    
    return agent, server

# Store active sessions
sessions = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = id(websocket)
    message_history = []
    
    try:
        print(f"[WebSocket] New connection accepted, session_id: {session_id}")
        
        try:
            agent, server = create_agent()
            print(f"[WebSocket] Agent created successfully")
        except Exception as e:
            print(f"[WebSocket] Failed to create agent: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "message": f"Failed to initialize AI agent: {str(e)}"
            })
            await websocket.close()
            return
        
        try:
            async with asyncio.timeout(30):  # 30 second timeout for MCP server startup
                async with agent.run_mcp_servers():
                    print(f"[WebSocket] MCP servers started successfully")
                    await websocket.send_json({
                        "type": "connected",
                        "message": "Connected to Market Query AI"
                    })
                    
                    while True:
                        try:
                            data = await websocket.receive_text()
                            user_query = json.loads(data)
                            query_text = user_query.get("query", "").strip()
                            
                            if not query_text:
                                continue
                            
                            # Check rate limit
                            can_proceed, wait_time = await rate_limiter.acquire()
                            if not can_proceed:
                                await websocket.send_json({
                                    "type": "error",
                                    "message": f"Rate limit exceeded. Please wait {int(wait_time)} seconds before trying again. This helps prevent API rate limit errors."
                                })
                                continue
                            
                            # Send processing status
                            await websocket.send_json({
                                "type": "processing",
                                "message": "Processing your query..."
                            })
                            
                            try:
                                # Run the agent with timeout
                                response = await asyncio.wait_for(
                                    agent.run(
                                        query_text,
                                        message_history=message_history
                                    ),
                                    timeout=60.0  # 60 second timeout
                                )
                                
                                # Extract tools used
                                tools_used = []
                                for msg in response.all_messages():
                                    if hasattr(msg, "parts"):
                                        for part in msg.parts:
                                            if hasattr(part, "tool_name"):
                                                tools_used.append(part.tool_name)
                                
                                # Get response output
                                output = getattr(response, "output", str(response))
                                
                                # Convert markdown to HTML if needed
                                html_output = markdown.markdown(output, extensions=['tables', 'fenced_code'])
                                
                                # Send response
                                await websocket.send_json({
                                    "type": "response",
                                    "data": {
                                        "output": html_output,
                                        "raw_output": output,
                                        "tools_used": list(set(tools_used))
                                    }
                                })
                                
                                # Update message history
                                # Don't limit history to avoid breaking tool_use/tool_result pairs
                                message_history = response.all_messages()
                                
                            except asyncio.TimeoutError:
                                await websocket.send_json({
                                    "type": "error",
                                    "message": "Query timed out after 60 seconds. Please try a simpler query or try again later."
                                })
                            except Exception as e:
                                error_msg = str(e)
                                # Handle rate limit errors specifically
                                if "rate_limit_error" in error_msg or "429" in error_msg:
                                    await websocket.send_json({
                                        "type": "error",
                                        "message": "API rate limit exceeded. Please wait a minute before trying again. Consider using simpler queries or reducing query frequency."
                                    })
                                else:
                                    await websocket.send_json({
                                        "type": "error",
                                        "message": f"Error: {error_msg}"
                                    })
                        
                        except json.JSONDecodeError:
                            await websocket.send_json({
                                "type": "error",
                                "message": "Invalid JSON format"
                            })
        except asyncio.TimeoutError:
            print(f"[WebSocket] MCP server startup timed out")
            await websocket.send_json({
                "type": "error",
                "message": "Failed to start MCP server: timeout. The server is taking too long to initialize. Please try again."
            })
            await websocket.close()
        except Exception as e:
            print(f"[WebSocket] MCP server startup failed: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "message": f"Failed to start MCP server: {str(e)}"
            })
            await websocket.close()
                    
    except WebSocketDisconnect:
        print(f"[WebSocket] Client disconnected, session_id: {session_id}")
        if session_id in sessions:
            del sessions[session_id]
    except Exception as e:
        print(f"[WebSocket] Unexpected error: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"Server error: {str(e)}"
            })
            await websocket.close()
        except:
            pass  # Connection might already be closed

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

