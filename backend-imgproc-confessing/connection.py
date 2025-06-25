from os import environ as env
import json
import firebase_admin
from firebase_admin import credentials, firestore

firebase_json = env['FIREBASE_SERVICE_ACCOUNT_JSON']

if not firebase_json:
    raise RuntimeError("Missing FIREBASE_SERVICE_ACCOUNT_JSON environment variable")

# Parse JSON string into a dictionary
cred_dict = json.loads(firebase_json)

# Use credentials from dictionary instead of file
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred, {
    'storageBucket': 'confessions-e4a11.appspot.com'
})

db = firestore.client()
