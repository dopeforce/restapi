from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd
import time

app = FastAPI()

# Enable CORS for any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Middleware for timing
@app.middleware("http")
async def add_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start)
    return response

# Load CSV data on startup
df = pd.read_csv("students.csv")

@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    # Filter if class is specified
    if class_:
        filtered = df[df["class"].isin(class_)]
    else:
        filtered = df
    students = filtered.to_dict(orient="records")
    return {"students": students}

# Optional root route
@app.get("/")
async def root():
    return {"message": "Student API is running"}
