import datetime
import time
import uuid
from src.connection import get_pool, query, fetchrow, execute, close_pool
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import requests
import uvicorn
import os
import json
from typing import List
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

# Create an instance of FastAPI to handle routes
app = FastAPI()

'''The below section allows specific ip addresses to make requests'''
# Get allowed servers from env file
frontend_url = env['FRONTEND_URL']
frontend_url_2 = env['FRONTEND_URL_2']

# Configure CORS to allow requests from your React app's origins
origins = [
    frontend_url,
    frontend_url_2
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Add your React app's origin(s) here
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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

# Define the behavior for the http://127.0.0.1:8000/ route with the GET method
@app.get("/")
async def root():
    """Get all confessions from the database"""
    try:
        # Query all confessions from PostgreSQL
        rows = await query("""
            SELECT id, confession, location, created_at, updated_at
            FROM confessions
            ORDER BY id ASC
        """)
        
        # Convert to dictionary format
        confessions_dict = {
            str(row['id']): {
                'id': row['id'],
                'confession': row['confession'],
                'location': row['location'],
                'created_at': row['created_at'].isoformat() if row['created_at'] else None,
                'updated_at': row['updated_at'].isoformat() if row['updated_at'] else None
            }
            for row in rows
        }
        
        return confessions_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define the behavior for the http://127.0.0.1:8000/addConfession route with the POST method
@app.post("/addConfession")
async def addConfession(confession_obj: ConfessionCreate): 
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
                'confession': row['confession'],
                'location': row['location'],
                'created_at': row['created_at'].isoformat(),
                'updated_at': row['updated_at'].isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image processing endpoints removed - will be handled locally in admin site

# API endpoint to generate a MyConfessions.json for www.myconfessions.co.za confessions
@app.get("/myconfessions-json/")
async def myconfessions_json():
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
            confession_text = row['confession'].strip()
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

# Healthcheck Endpoint
@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
