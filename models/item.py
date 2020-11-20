item_list = []

def get_last_id():
    if item_list:
        last_item = item_list[-1]
    else:
        return 1
    return last_item.id + 1

class Item:
    def __init__(self, name, description, tags, rating, ratings, price, amount):
        self.id = get_last_id()
        self.name = name
        self.description = description
        self.tags = tags
        self.rating = 0
        self.ratings = 0
        self.price = price
        self.amount = amount

    @property
    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "rating": self.rating,
            "ratings": self.ratings,
            "price": self.price,
            "amount": self.amount
        }