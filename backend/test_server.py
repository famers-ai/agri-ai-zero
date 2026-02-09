"""
Simple test server to verify FastAPI is working
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Server</title>
    </head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>✅ Server is Working!</h1>
        <p>If you see this, FastAPI is running correctly.</p>
    </body>
    </html>
    """)

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Server is healthy"}

if __name__ == "__main__":
    print("🚀 Starting test server on http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
