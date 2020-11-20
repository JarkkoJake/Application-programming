from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.item import Item

class ItemListResource(Resource):

    def get(self):

        data = Item.data

        return {"data": data}, HTTPStatus.OK

