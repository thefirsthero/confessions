from connection import db
from fastapi import FastAPI, HTTPException
from models import Confession

# We access the 'users' collection in the database (Firestore instance)
confessions = db.collection(u'confessions')

# Create an instance of FastAPI to handle routes
app = FastAPI()

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

# Define the behavior for the http://127.0.0.1:8000/addUser route with the POST method
@app.post("/addConfession")
async def addUser(confession_obj: Confession): # We pass the confession model {confession, location} as a parameter
    # Create an instance of the confessions list and add the id as the dictionary key
    confessionAdd = confessions.document(f'{confession_obj.id}') 
    # Add the internal parameters of the dictionary and send the changes
    confessionAdd.set({
        # On the left, we see the field name in the database
        u'confession': confession_obj.confession, # On the right, we see the data passed as a parameter in the POST request
        u'location': confession_obj.location
    })
    return {'status' : 200} # Return a success message