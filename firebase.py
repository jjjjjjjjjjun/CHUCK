import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def save_story(name: str, concept: str, story: str):
    db.collection("stories").add({
        "name": name,
        "concept": concept,
        "story": story,
        "created_at": datetime.utcnow()
    })
