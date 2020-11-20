item_list = []

def get_last_id():
    if item_list:
        last_item = item_list[-1]
    else:
        return 1
    return last_item.id + 1

class Item:
    def __init__(self, name, description, img, rating, ratings, price, amount):
        self.id = get_last_id()
        self.name = name
        self.description = description
        self.rating = 0
        self.ratings = 0
        self.price = price
        self.amount = amount