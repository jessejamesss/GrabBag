
from flask import request, jsonify
from config import app, firestoreDB, firebaseAuth
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
        
    ## Add salt and hash password
    salt = generate_salt()
    password_hashed = hash_password(password, salt)
    
    ## Create a new User for registering user and add to Firestore
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

@app.route("/login", methods=["GET"])
def getGrabBagPage():
    ## Get login information from login form.
    email = request.json.get("email")
    password = request.json.get("password")
    
    if not email or not password:
        return jsonify({
            "message": "Both email and password required."
        })
        
    ## Validate user email.
    try:
        user_record = firebaseAuth.get_user_by_email(email)
        print("User email exists. Record returned.")
    except exceptions.FirebaseError as e:
        print(e)
        return jsonify({
            "message": e
        })
        
    user_uid = user_record.uid
    
    ## Get user from Firestore.
    try:
        user_ref = firestoreDB.collection("users").document(user_uid).get()
        print("Successfully returned user reference.")
    except exceptions.FirebaseError as e:
        print(e)
        return jsonify({
            "message": e
        })
        
    ## Validate user password.
    user_doc = user_ref.to_dict()

    validated = validate_password(password, bytes.fromhex(user_doc["password"]), bytes.fromhex(user_doc["salt"]))
    print(validated)
    if validated:
        try:
            custom_user_token = firebaseAuth.create_custom_token(user_uid)
            print("Custom Token successfully generated.")
        except exceptions.FirebaseError as e:
            print(e)
            return jsonify({
                "message": e
            })
    else:
        return jsonify({
            "message": "Password is not valid."
        })
    
    response = jsonify({
        "message": "User successfully validated. Custom Token sent for authentication."
    })
    response.headers["Authorization"] = 'Bearer ' + custom_user_token.decode("utf-8")
    
    return response
    
    
    
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
