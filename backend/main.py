
from flask import request, jsonify
from config import app, firebase, firestoreDB, firebaseAuth
from firebase_admin import exceptions
from models.user import User

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
        "password" : password,
        "app" : firebase
    }
    
    try:
        new_user_record = firebaseAuth.create_user(**create_user_kwargs)
        print("User successfully added to Authentication.")
    except exceptions.FirebaseError as e:
        print(e)
        return jsonify({
            "message" : e
        })
        
    ## Add User to Firestore
    new_user_kwargs = {
        "uid" : new_user_record.uid,
        "first_name" : first_name,
        "last_name" : last_name,
        "email" : email,
        "grab_bag" : []
    }
    
    new_user = User(**new_user_kwargs)
    try:
        firestoreDB.collection("users").document(new_user.uid).set(new_user_kwargs)
        print("User successfully added to Firestore.")
    except exceptions.FirebaseError as e:
        print(e)
        return jsonify({
            "message" : e
        })
        
    return jsonify({
        "message" : "User successfully added to Authentication and Firestore!"
    })
    
    
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    