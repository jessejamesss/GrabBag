from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth

## Initialize Flask application
app = Flask(__name__)

## Specify allowed origins
CORS(app)

## Firebase Admin SDK configuration
cred = credentials.Certificate("")
firebase = firebase_admin.initialize_app(cred)

## Firestore configuration
firestoreDB = firestore.client(firebase)

## Authentication configuration
firebaseAuth = auth.Client(firebase)