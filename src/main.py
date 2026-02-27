from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

from src.api.oauth_callback import router as oauth_router


# =====================================================
# LIFESPAN (Railway-safe)
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Google OAuth MCP Server started successfully")
    print("👉 Visit /google_oauth to begin authentication")
    yield
    print("🛑 Server shutting down")


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Google OAuth Server for MCP",
    description="Google OAuth Proxy Server for Remote MCP Access",
    version="0.1.0",
    lifespan=lifespan
)


# =====================================================
# CORS CONFIG
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can restrict later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# ROUTERS
# =====================================================

app.include_router(oauth_router)


# =====================================================
# ROOT ENDPOINT
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Google OAuth MCP Server</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: #333;
                }
                a {
                    margin-top: 20px;
                    padding: 10px 20px;
                    text-decoration: none;
                    background-color: #4285F4;
                    color: white;
                    border-radius: 5px;
                }
                a:hover {
                    background-color: #3367D6;
                }
            </style>
        </head>
        <body>
            <h1>Google OAuth MCP Server</h1>
            <a href="/google_oauth">Authenticate with Google</a>
        </body>
    </html>
    """


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
async def health_check():
    return {"status": "OK"}
