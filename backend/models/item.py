## This class serves as an object for Items in the User's grabBag.

class Item():
    def __init__(self, img, itemName, price, itemURL):
        self.img = img
        self.itemName = itemName
        self.price = price
        self.itemURL = itemURL
        
    def to_json(self):
        return {
            "img" : self.img,
            "itemName" : self.itemName,
            "price" : self.price,
            "itemURL" : self.itemURL,
        }