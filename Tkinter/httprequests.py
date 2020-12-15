import requests
from app import port

address = "http://localhost:"
port = str(port)+"/"
header = {"content-type":"JSON"}

def post_user(data):
    url = address+port+"users"
    req = requests.post(url, json=data)
    return req.json()
def post_token(data):
    url = address+port+"token"
    req = requests.post(url, json=data)
    return req.json()
def post_refresh(jwt):
    url = address + port + "refresh"
    req = requests.post(url, headers={"Authorization":"Bearer "+jwt})
    return req.json()
def post_item(data, jwt):
    url = address+port+"items"
    req = requests.post(url, json=data, headers={"Authorization":"Bearer "+jwt})
    return req.json()
def post_rating(data, item_id, jwt):
    url = address + port + "items/" + str(item_id) + "/ratings"
    req = requests.post(url, json=data, headers={"Authorization":"Bearer "+jwt})
    return req.json()
def get_user_unregistered(username):
    url = address + port + "users/"+str(username)
    req = requests.get(url)
    return req.json()
def get_user(username, jwt):
    url = address + port + "users/"+str(username)
    req = requests.get(url, headers={"Authorization":"Bearer "+jwt})
    return req.json()
def get_item(item_id):
    url = address + port + "items/" + str(item_id)
    req = requests.get(url)
    return req.json()
def get_items():
    url = address + port + "items"
    req = requests.get(url)
    return req.json()
def search_items(tag):
    url = address + port + "tags/" + str(tag)
    req = requests.get(url).json()
    return req
def search_items_name(tag):
    url = address + port + "item/" + tag
    req = requests.get(url)
    return req.json()
def get_me(jwt):
    url = address + port + "me"
    req = requests.get(url, headers={"Authorization":"Bearer "+jwt})
    return req.json()
def get_all_by_user(username):
    url = address + port + "users/" + username + "/items"
    req = requests.get(url)
    return req.json()
def patch_item(data, jwt):
    url = address + port + "items/" + str(data["id"])
    req = requests.patch(url, json=data, headers={"Authorization":"Bearer "+jwt})
    return req
def delete_item(data, jwt):
    url = address + port + "items/" + str(data["id"])
    req = requests.delete(url, headers={"Authorization":"Bearer "+jwt})
    return req

