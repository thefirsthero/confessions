import datetime
import time
import uuid
from src.connection import get_pool, query, fetchrow, execute, close_pool
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Header
from fastapi.responses import FileResponse, JSONResponse
import requests
import uvicorn
import os
import json
from typing import List, Optional
import imghdr 
from src.image_processing import extract_and_reformat_text
from src.text_processing import filter_text, clean_and_format_text, extract_series_and_part, split_and_clean_text
from src.ocr_functions import extract_text_with_tesseract
from fastapi.middleware.cors import CORSMiddleware
from src.models import Confession, ConfessionCreate
from os import environ as env
import tempfile
import asyncio
import anyio
import cv2
import numpy as np
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Create an instance of FastAPI to handle routes
app = FastAPI()

# Parse CORS origins from environment variable
allowed_origins = env.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
allowed_origins = [origin.strip() for origin in allowed_origins]  # Remove whitespace

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# API Key Authentication Middleware
class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for health check endpoint
        if request.url.path == "/health":
            return await call_next(request)
        
        # Skip authentication for CORS preflight requests
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Get API key from environment
        valid_api_key = env.get('API_KEY')
        
        # If no API key is configured, allow all requests (development mode)
        if not valid_api_key:
            return await call_next(request)
        
        # Get API key from request header
        api_key = request.headers.get('X-API-Key')
        
        # Verify API key
        if not api_key or api_key != valid_api_key:
            return Response(
                content=json.dumps({"detail": "Invalid or missing API key"}),
                status_code=401,
                media_type="application/json"
            )
        
        return await call_next(request)

# Add API key middleware
app.add_middleware(APIKeyMiddleware)

# Self-ping functionality to keep the server alive
def ping_server():
    try:
        url = env.get('HEALTHCHECK_URL')
        if url:
            print(f"Pinging {url}...")
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            print(f"Ping successful at {datetime.datetime.now()}")
        else:
            print("HEALTHCHECK_URL not set, skipping ping.")
    except requests.exceptions.RequestException as e:
        print(f"Ping failed: {e}")

async def run_scheduler():
    while True:
        await anyio.to_thread.run_sync(ping_server)
        await asyncio.sleep(240) # 4 minutes

@app.on_event("startup")
async def startup_event():
    # Initialize database connection pool
    await get_pool()
    print("✅ Database connection pool initialized")
    
    if env.get('SELF_PING_ENABLED', 'false').lower() == 'true':
        print("Self-ping enabled. Starting scheduler.")
        asyncio.create_task(run_scheduler())
    else:
        print("Self-ping disabled.")

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connection pool
    await close_pool()
    print("✅ Database connection pool closed")

def clean_confession_text(text: str) -> str:
    """Clean confession text by replacing newlines with spaces and removing extra whitespace"""
    if not text:
        return text
    # Replace newline characters with spaces
    cleaned = text.replace('\n', ' ')
    # Replace multiple spaces with single space
    cleaned = ' '.join(cleaned.split())
    return cleaned

# Get all confessions
@app.get("/confessions")
async def get_confessions():
    """Get all confessions from the database"""
    try:
        # Query all confessions from PostgreSQL
        rows = await query("""
            SELECT id, confession, location, created_at, updated_at
            FROM confessions
            ORDER BY id ASC
        """)
        
        # Convert to dictionary format with cleaned text
        confessions_dict = {
            str(row['id']): {
                'id': row['id'],
                'confession': clean_confession_text(row['confession']),
                'location': row['location'],
                'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                'updated_at': row['updated_at'].isoformat() if row['updated_at'] else None
            }
            for row in rows
        }
        
        return confessions_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new confession
@app.post("/confessions")
async def create_confession(confession_obj: ConfessionCreate): 
    """Add a new confession to the database"""
    try:
        # Insert confession into PostgreSQL
        row = await fetchrow("""
            INSERT INTO confessions (confession, location)
            VALUES ($1, $2)
            RETURNING id, confession, location, created_at, updated_at
        """, confession_obj.confession, confession_obj.location)
        
        return {
            'status': 200,
            'message': 'Confession added successfully',
            'data': {
                'id': row['id'],
                'confession': clean_confession_text(row['confession']),
                'location': row['location'],
                'created_at': row['created_at'].isoformat(),
                'updated_at': row['updated_at'].isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image processing endpoints removed - will be handled locally in admin site

# Export confessions as JSON file
@app.get("/confessions/export")
async def export_confessions():
    """Generate MyConfessions.json from PostgreSQL database"""
    try:
        # Query all confessions from PostgreSQL ordered by id
        rows = await query("""
            SELECT id, confession, location
            FROM confessions
            ORDER BY id ASC
        """)

        # Initialize a list to store the generated JSON data
        generated_json = []

        # Define common values for series, outro, and path
        series = "Your Confessions"
        outro = "Visit www.myconfessions.co.za to anonymously confess"
        path = "/content/drive/MyDrive/Colab Notebooks/AI_Bots/ContentGen/Whisper-Tiktok/code/Trash"

        # Function to append location with proper punctuation
        def append_location(text, location):
            if not location:
                return text
            if text and text[-1] in ('.', '!', '?'):
                return f"{text} {location}"
            else:
                return f"{text}. {location}"

        for row in rows:
            confession_id = row['id']
            # Clean the confession text
            confession_text = clean_confession_text(row['confession'])
            location = row['location']

            # Append 'location' to the text with proper punctuation
            full_text = append_location(confession_text, location)

            # Create a dictionary for the confession data
            confession_dict = {
                "series": series,
                "part": str(confession_id),
                "outro": outro,
                "path": path,
                "text": full_text.strip()
            }

            # Add the confession data to the generated JSON list
            generated_json.append(confession_dict)

        # Create a temporary directory to store the JSON file
        temp_dir = tempfile.mkdtemp(prefix='json_generation_')
        json_file_path = os.path.join(temp_dir, 'generated_confessions.json')

        # Write the generated JSON data to the JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(generated_json, json_file, ensure_ascii=False, indent=4)

        # Return the generated JSON file as a downloadable response
        response = FileResponse(json_file_path, headers={"Content-Disposition": "attachment; filename=MyConfessions.json"})

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Process images with OCR
@app.post("/images/process")
async def process_images(images: List[UploadFile] = File(...)):
    """
    Process uploaded images with OCR and generate video.json structure.
    Images are processed in-memory without saving to disk.
    
    Returns JSON array with format:
    [
        {
            "series": "Confessions",
            "part": "1",
            "outro": "Visit www.myconfessions.co.za to anonymously confess",
            "text": "extracted and cleaned confession text"
        },
        ...
    ]
    """
    try:
        video_data = []
        
        # Standard values for video generation
        series = "Confessions"
        outro = "Visit www.myconfessions.co.za to anonymously confess"
        
        for idx, image in enumerate(images, start=1):
            # Validate image type
            if not image.content_type or not image.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400, 
                    detail=f"File '{image.filename}' is not a valid image"
                )
            
            # Read image bytes
            image_bytes = await image.read()
            
            # Convert bytes to numpy array for OpenCV
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Could not decode image '{image.filename}'"
                )
            
            # Create temporary file for OCR processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                temp_path = temp_file.name
                cv2.imwrite(temp_path, img)
            
            try:
                # Extract text with OCR
                extracted_text = extract_and_reformat_text(temp_path, extract_text_with_tesseract)
                
                # Process text
                series_name, part_number = extract_series_and_part(extracted_text)
                cleaned_text = filter_text(extracted_text)
                cleaned_text = clean_and_format_text(cleaned_text)
                cleaned_text = split_and_clean_text(cleaned_text)
                
                # Use extracted part number if available, otherwise use index
                part = part_number if part_number else str(idx)
                
                # Build video data entry
                video_entry = {
                    "series": series_name if series_name else series,
                    "part": part,
                    "outro": outro,
                    "text": cleaned_text.strip()
                }
                
                video_data.append(video_entry)
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        
        # Sort by part number (numeric sort)
        try:
            video_data = sorted(video_data, key=lambda x: int(x["part"]))
        except (ValueError, KeyError):
            # If sorting fails, keep original order
            pass
        
        return JSONResponse(content=video_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")

# Healthcheck Endpoint
@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
