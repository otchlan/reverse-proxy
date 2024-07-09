#api.py
from fastapi import FastAPI, Request
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware to allow all origins (for testing purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_bypass_header(request: Request, call_next):
    request.state.tunnel_password = "80.51.181.42"  # Replace with actual password if needed
    response = await call_next(request)
    response.headers['User-Agent'] = 'localtunnel-bypass'
    return response

@app.get("/")
async def read_root(request: Request):
    client_host = request.client.host
    request_path = request.url.path
    logger.info(f"Received request from: {client_host}, Path: {request_path}")
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
