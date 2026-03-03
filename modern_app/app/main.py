# filename: modern_app/app/main.py
from fastapi import FastAPI
from .api import router

app = FastAPI(title="Modern Issue Tracker (Refactored)")
app.include_router(router)
