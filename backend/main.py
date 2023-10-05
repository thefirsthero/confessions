from connection import db
from fastapi import FastAPI, HTTPException
from models import User

# We access the 'users' collection in the database (Firestore instance)
users = db.collection(u'users')

# Create an instance of FastAPI to handle routes
app = FastAPI()

# Define the behavior for the http://127.0.0.1:8000/ route with the GET method
@app.get("/")
async def root():
    # Using users.get(), which belongs to Firebase, we retrieve all users from the list
    usersRef = users.get()
    # Create a dictionary to return as JSON
    usersJson = {}
    # Iterate through the list of users
    for user in usersRef:
        # Add each retrieved user to the dictionary
        usersJson[user.id] = user.to_dict()
    # Return the dictionary
    return usersJson

# Define the behavior for the http://127.0.0.1:8000/addUser route with the POST method
@app.post("/addUser")
async def addUser(user: User): # We pass the user model {name, lastName, born} as a parameter
    # Create an instance of the user list and add the id as the dictionary key
    userAdd = users.document(f'{user.id}') 
    # Add the internal parameters of the dictionary and send the changes
    userAdd.set({
        # On the left, we see the field name in the database
        u'name': user.name, # On the right, we see the data passed as a parameter in the POST request
        u'surname': user.lastName,
        u'birthYear': user.birthYear
    })
    return {'status' : 200} # Return a success message

# Define the behavior for the http://127.0.0.1:8000/delUser route with the DELETE method
@app.delete("/delUser")
async def delUser(id): # We pass the user's id as a parameter
    # Delete the user in the collection with the provided id
    userRef = db.collection(u'users').document(id)
    user = userRef.get()
    if user.exists:        
        users.document(f'{id}').delete()      
    else:
        raise HTTPException(status_code=404, detail="User not found") # Raise an exception in case the user with the provided id doesn't exist
        
    return {'status' : 200} # Return a success message

@app.put("/modName")
async def modUser(id, name): 
    userMod = users.document(id)
    userMod.set({
        u'name': name
    })
    return {'status' : 200}
