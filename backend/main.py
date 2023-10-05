from connection import db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Confession

# Create an instance of FastAPI to handle routes
app = FastAPI()

# Configure CORS to allow requests from your React app's origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your React app's origin(s) here
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
