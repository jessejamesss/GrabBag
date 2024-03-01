
from flask import request, jsonify
from config import app, firebase, firebaseAuth
from firebase_admin import exceptions
from models.user import User
from models.grabbag import GrabBag
from utils.password_utils import generate_salt, hash_password, validate_password

@app.route("/register", methods=["POST"])
def register():
    ## Get user details from registration form.
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    password = request.json.get("password")
    
    ## Check if the fields are empty. If they are, run an error.
    if not first_name or not last_name or not email or not password:
        return jsonify({
            "message" : "Please enter first name, last name, email, and password."
            })
    
    ## Create user in Authentication.
    create_user_kwargs = {
        "display_name" : first_name + ' ' + last_name,
        "email" : email,
        "password" : password
    }
    
    try:
        new_user_record = firebaseAuth.create_user(**create_user_kwargs)
        print("User successfully added to Authentication.")
    except exceptions.FirebaseError as e:
        print(e)
        return jsonify({
            "message" : e
        })
        
    ## Create a new GrabBag for registering User and add to Firestore
    new_grabBag = GrabBag(new_user_record.uid)
    
    try:
        new_grabBag_record = new_grabBag.save_to_firestore()
        print("GrabBag created for newly registered User!")
    except exceptions.FirebaseError as e:
        print(e)
        return jsonify({
            "message" : e
        })
        
    ## Create a new User for registering user and add to Firestore
    salt = generate_salt()
    password_hashed = hash_password(password, salt)
    new_user_kwargs = {
        "uid" : new_user_record.uid,
        "first_name" : first_name,
        "last_name" : last_name,
        "email" : email,
        "password" : password_hashed.hex(),
        "salt" : salt.hex(),
        "grab_bag" : new_grabBag_record[1]
    }
    new_user = User(**new_user_kwargs)
    
    try:
        new_user.save_to_firestore(new_user.uid)
        print("User successfully added to Firestore.")
    except exceptions.FirebaseError as e:
        print(e)
        return jsonify({
            "message" : e
        })
        
    return jsonify({
        "message" : "User successfully added to Authentication and Firestore!"
    })

# @app.route("/login", methods=["GET"])
# def login():
#     print("Render login page.")

# @app.route("/<string:uid>", methods=["GET"])
# def getGrabBagPage():
#     print("where tf is my shit!?!?!?!??!?")
#     validate_password()
    
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
