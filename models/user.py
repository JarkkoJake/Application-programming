from models.item import Item

user_list = []
def next_id():
    if len(user_list == 0):
        return 1
    return len(user_list)+1
def calc_rating(items):
    sum = 0
    n = 0
    for i in items:
        sum = i.rating
        n += 1
    return sum/n
class User:
    def __init__(self, data):
        self.id = next_id()
        self.username = data["name"]
        self.email = data["email"]
        self.password = data["password"]
        self.items = []
        self.rating = calc_rating(self.items)
        self.profile_picture = None
        self.is_admin = False
        user_list.append(self)

