## This class represents the GrabBag object.
from config import firestoreDB

class GrabBag:
    def __init__(self, owner):
        self.items = []
        self.owner = owner
        
    def save_to_firestore(self):
        bag_data = {
            "items" : self.items,
            "owner" : self.owner
        }
        
        new_grab_bag = firestoreDB.collection("grabBag").add(bag_data)
        return new_grab_bag
        
    def update_in_firestore(self, field, new_value):
        if field == "items":
            self.items.append(new_value)
        elif field == "owner":
            self.owner = new_value
        else:
            raise ValueError("Invalid field name.")
        
        bag_data = {
            field : new_value
        }
        firestoreDB.collection("grabBag").document(self.uid).update(bag_data)
        