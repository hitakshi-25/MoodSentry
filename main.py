# main.py

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.routes import auth, dashboard, role_routes, audit, tasks, mood
import os

load_dotenv()

app = FastAPI()

# Middleware for sessions
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers (NOTE: mood removed due to heavy ML)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(role_routes.router)
app.include_router(audit.router)
app.include_router(tasks.router)
app.include_router(mood.router)

# Startup for Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
