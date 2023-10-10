import datetime
import time
import uuid
from connection import db
from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import List
import shutil
from fastapi.middleware.cors import CORSMiddleware
from models import Confession
from os import environ as env
from os import remove
from firebase_admin import firestore

# Create an instance of FastAPI to handle routes
app = FastAPI()

'''The below section allows specific ip addresses to make requests'''
# Get allowed servers from env file
react_app_origin_1 = env['MY_VARIABLE_1']
react_app_origin_2 = env['MY_VARIABLE_2']

# Configure CORS to allow requests from your React app's origin
origins = [
    react_app_origin_1,
    react_app_origin_2
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Add your React app's origin(s) here
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# We access the 'users' collection in the database (Firestore instance)
confessions = db.collection(u'confessions')

# Define the behavior for the http://127.0.0.1:8000/ route with the GET method
@app.get("/")
async def root():
    # Using confessions.get(), which belongs to Firebase, we retrieve all users from the list
    confessionsRef = confessions.get()
    # Create a dictionary to return in JSON format
    confessionsJson = {}
    # Iterate through the list of confessions
    for confession in confessionsRef:
        # Add each retrieved confession to the dictionary
        confessionsJson[confession.id] = confession.to_dict()
    # Return the dictionary
    return confessionsJson

# Define the behavior for the http://127.0.0.1:8000/addConfession route with the POST method
@app.post("/addConfession")
async def addConfession(confession_obj: Confession): 
    try:
        # Get the count of existing documents in the 'confessions' collection
        confessions_count = len(list(confessions.stream()))
        
        # Set the 'id' field of the new document to the count + 1
        confession_obj.id = str(confessions_count + 1)
        
        # Create a new Confession document in Firestore
        new_confession = confessions.add(confession_obj.dict())
        return {'status': 200, 'message': 'Confession added successfully'}
    except Exception as e:
        return {'status': 500, 'error': str(e)}

from firebase_admin import storage

@app.post("/uploadImages")
async def upload_images(images: List[UploadFile]):
    try:
        # Initialize an empty list to store image URLs
        image_urls = []

        # Get the current timestamp as a string (for uniqueness)
        current_time = str(int(time.time()))

        # Iterate through the uploaded image files
        for index, image in enumerate(images):
            # Generate a unique filename with an incremental number and timestamp
            filename = f"{current_time}_{index}_{str(uuid.uuid4())}"

            # Upload the image to Firebase Storage
            bucket = storage.bucket()
            blob = bucket.blob(filename)
            blob.upload_from_file(image.file, content_type=image.content_type)

            # Get the download URL for the uploaded image
            image_url = blob.generate_signed_url(
                expiration=datetime.timedelta(days=1),
                method="GET"
            )

            # Save the image URL to Firestore
            image_doc = {
                'url': image_url,
                'filename': filename  # Optional: You can also save the filename
            }

            # Add the image document to the 'images' collection in Firestore
            db.collection('images').add(image_doc)

            # Append the image URL to the list
            image_urls.append(image_url)

        return {'status': 200, 'message': 'Images uploaded successfully', 'image_urls': image_urls}
    except Exception as e:
        return {'status': 500, 'error': str(e)}
