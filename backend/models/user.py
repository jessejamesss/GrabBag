## This class serves as an object for Users.
from config import firestoreDB

class User:
    def __init__(self, uid, first_name, last_name, email, grab_bag):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.grab_bag = grab_bag
        
    def save_to_firestore(self,uid):
        user_data = {
            "firstName" : self.first_name,
            "lastName" : self.last_name,
            "email" : self.email,
            "grabBag" : self.grab_bag
        }
        
        firestoreDB.collection("users").document(uid).set(user_data)
        
        
    def update_in_firestore(self, field, new_value):
        if field == "firstName":
            self.first_name = new_value
        elif field == "lastName":
            self.last_name = new_value
        elif field == "email":
            self.email = new_value
        elif field == "grabBag":
            self.grab_bag = new_value
        else:
            raise ValueError("Invalid field name.")
        
        user_data = {
            field : new_value
        }
        firestoreDB.collection("users").document(self.uid).update(user_data)
        
        
    def to_json(self):
        return {
            "firstName" : self.first_name,
            "lastName" : self.last_name,
            "email" : self.email,
            "grabBag" : self.grab_bag
        }