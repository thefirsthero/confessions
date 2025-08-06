from os import environ as env
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

firebase_json_b64 = env.get('FIREBASE_SERVICE_ACCOUNT_JSON')

if not firebase_json_b64:
    raise RuntimeError("Missing FIREBASE_SERVICE_ACCOUNT_JSON environment variable")

# Decode the base64 string
firebase_json = base64.b64decode(firebase_json_b64).decode('utf-8')

# Parse JSON string into a dictionary
cred_dict = json.loads(firebase_json)

# Use credentials from dictionary instead of file
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred, {
    'storageBucket': 'confessions-e4a11.appspot.com'
})

db = firestore.client()
