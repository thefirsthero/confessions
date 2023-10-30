import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# We create the 'Credential' variable (cred) and load the Firebase credential file into it
cred = credentials.Certificate("serviceAccountKey.json")
# We initialize Firebase with the provided credentials
firebase_admin.initialize_app(cred, {
    'storageBucket': 'confessions-e4a11.appspot.com'
})
# We create an instance of Firestore, which will be our database (db)
db = firestore.client()
# We will import this variable, which is an instance of the database, in the 'main.py' file!!!
