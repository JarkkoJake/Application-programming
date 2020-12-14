from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from models.item import Item
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from resources.util import user_not_found,item_not_found
from resources.item_history import saveItemHistory
from webargs import fields
from webargs.flaskparser import use_kwargs
from schemas.item import ItemSchema
import os
from utils import save_image
from extensions import image_set

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)
item_picture_schema = ItemSchema(only=("picture", ))

class ItemListResource(Resource):

    def get(self):  #Hakee kaikki itemit

        items = Item.get_all()
        return item_list_schema.dump(items).data, HTTPStatus.OK

    @jwt_required
    def post(self): #Itemin luonti

        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = item_schema.load(data=json_data)

        if errors:

            return {"message": "Validation errors", "errors" : errors }, HTTPStatus.BAD_REQUEST

        item = Item(**data)

        if item.tag1 == item.tag2 or item.tag1 == item.tag3 or item.tag2 == item.tag3:  #Validoi ettei tagit ole samoja.
            return {"message": "Tags cant be the same"}, HTTPStatus.BAD_REQUEST

        item.user_id = current_user
        item.save()

        saveItemHistory(item.id)    #Tallettaa itemin myös historiaan

        return item_schema.dump(item).data, HTTPStatus.CREATED

class UserItemListResource(Resource):
    @jwt_optional
    def get(self, username):    #Palauttaa tietyn käyttäjän kaikki itemit
        user = User.get_by_username(username=username)
        if not user:
            user_not_found()
        items = Item.get_all_by_user(user_id=user.id)
        return item_list_schema.dump(items).data, HTTPStatus.OK

class ItemResource(Resource):


    @jwt_required
    def patch(self, item_id):   #Päivittää itemin

        json_data = request.get_json()

        data, errors = item_schema.load(data=json_data, partial=("name",))

        if errors:
            return {"message": "Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        item = Item.get_by_id(item_id=item_id)

        if item is None:
            return {"message": "item not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != item.user_id:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        item.name = data.get("name") or item.name
        item.description = data.get("description") or item.description
        item.tag1 = data.get("tag1") or item.tag1
        item.tag2 = data.get("tag2") or item.tag2
        item.tag3 = data.get("tag3") or item.tag3
        item.ratings = data.get("ratings") or item.ratings
        item.rating = data.get("rating") or item.rating
        item.price = data.get("price") or item.price
        item.amount = data.get("amount") or item.amount

        item.save()

        saveItemHistory(item.id)

        return item_schema.dump(item).data, HTTPStatus.OK

    def get(self, item_id): #Hakee itemin id.n mukaan

        item = Item.get_by_id(item_id=item_id)

        if item is None:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND

        return item_schema.dump(item), HTTPStatus.OK

    @jwt_required
    def put(self, item_id): #Korvaa olemassa olevan itemin

        json_data = request.get_json()

        item = Item.get_by_id(item_id=item_id)

        if item is None:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != item.user_id:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        item.name = json_data["name"]
        item.description = json_data["description"]
        item.tag1 = json_data["tag1"]
        item.tag2 = json_data["tag2"]
        item.tag3 = json_data["tag3"]
        item.ratings = json_data["ratings"]
        item.rating = json_data["rating"]
        item.price = json_data["price"]
        item.amount = json_data["amount"]

        item.save()
        saveItemHistory(item.id)

        return item.data, HTTPStatus.OK

    @jwt_required
    def delete(self, item_id): #Poistaa itemin, mutta jättää sen historia tauluun.

        item = Item.get_by_id(item_id=item_id)

        if item is None:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != item.user_id:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        item.delete()

        return {"message": "Item deleted"}, HTTPStatus.NO_CONTENT

class ItemTagResource(Resource):    #Hakee tagien mukaan

    def get(self, tags):

        items = Item.get_by_tag(tags=tags)

        if items is None:
            return {"message": "Items with this tag cannot be found"}, HTTPStatus.NOT_FOUND

        return item_list_schema.dump(items).data, HTTPStatus.OK

class ItemNameResource(Resource):   #Hakee itemin nimen mukaan.

    def get(self, name):

        items = Item.get_by_name(name=name)

        if items is None:

            return {"message": "Items with this name cannot be found"}, HTTPStatus.NOT_FOUND

        return item_list_schema.dump(items).data, HTTPStatus.OK

class ItemPictureUploadResource(Resource):
    @jwt_required
    def put(self, item_id):
        file = request.files.get("picture")
        current_user = get_jwt_identity()
        item = Item.get_by_id(item_id=item_id)
        if item.user_id != current_user:
            return {"message": "Access not allowed"}, HTTPStatus.FORBIDDEN
        if not file:
            return {"message": "Not a valid image"}, HTTPStatus.BAD_REQUEST
        if not image_set.file_allowed(file, file.filename):
            return {"message": "File type not allowed"}, HTTPStatus.BAD_REQUEST
        if item.picture:
            picture_path = image_set.path(folder="pictures", filename=item.picture)
            if os.path.exists(picture_path):
                os.remove(picture_path)
        filename = save_image(image=file, folder="pictures")
        item.picture = filename
        item.save()
        saveItemHistory(item.id)
        return item_picture_schema.dump(item).data, HTTPStatus.OK
