from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from models.item_history import HistoryItem
from models.item import Item
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from resources.util import user_not_found, item_not_found
from webargs import fields
from webargs.flaskparser import use_kwargs
from schemas.item_history import ItemHistorySchema
import os
from utils import save_image
from extensions import image_set


item_schema = ItemHistorySchema()
item_list_schema = ItemHistorySchema(many=True)


class ItemHistoryListResource(Resource):

    # Haetaan kaikki item_history-tableen tallennetut tiedot
    @jwt_required
    def get(self):

        items = HistoryItem.get_all()
        current_user = get_jwt_identity()
        user = User.get_by_id(current_user)

        if not user.is_admin:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        return item_list_schema.dump(items).data, HTTPStatus.OK


class UserItemHistoryListResource(Resource):

    # Haetaan usernamin kaikkien itemien historia
    @jwt_required
    def get(self, username):

        itemuser = User.get_by_username(username=username)
        current_user = get_jwt_identity()
        user = User.get_by_id(current_user)

        if not user.is_admin:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        if itemuser is None:
            return user_not_found()
        items = HistoryItem.get_all_by_user(user_id=itemuser.id)
        return item_list_schema.dump(items).data, HTTPStatus.OK


class ItemHistoryResource(Resource):

    # Haetaan tietyn itemin muutokset
    @jwt_required
    def get(self, original_item_id):

        items = HistoryItem.get_by_original_item_id(item_id=original_item_id)
        current_user = get_jwt_identity()
        user = User.get_by_id(current_user)
        originalitem = Item.get_by_id(item_id=original_item_id)

        if not user.is_admin:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        if originalitem is None:
            return item_not_found()
        return item_list_schema.dump(items).data, HTTPStatus.OK


# Funktio jolla tallennetaan itemi historiaan
def saveItemHistory(item_id):
    item = Item.get_by_id(item_id=item_id)
    historyitem = HistoryItem()

    historyitem.original_item_id = item.id
    historyitem.name = item.name
    historyitem.description = item.description
    historyitem.picture = item.picture
    historyitem.tag1 = item.tag1
    historyitem.tag2 = item.tag2
    historyitem.tag3 = item.tag3
    historyitem.rating = item.rating
    historyitem.price = item.price
    historyitem.amount = item.amount
    historyitem.user_id = item.user_id

    historyitem.save()


