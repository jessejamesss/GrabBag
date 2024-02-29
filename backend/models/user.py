## This class serves as an object for Users.
from config import firestoreDB

class User(firestoreDB):
    def __init__(self, uid, first_name, last_name, email, grab_bag):
        super().__init__()
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.grab_bag = grab_bag
        
    def save_to_firestore(self):
        user_data = {
            "firstName" : self.first_name,
            "lastName" : self.last_name,
            "email" : self.email,
            "grabBag" : self.grab_bag
        }
        
        
        
    def to_json(self):
        return {
            "uid" : self.uid,
            "firstName" : self.first_name,
            "lastName" : self.last_name,
            "email" : self.email,
            "grabBag" : self.grab_bag
        }