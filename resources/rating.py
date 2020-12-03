from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from models.item import Item
from models.rating import Rating
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from schemas.rating import RatingSchema
from resources.utils import user_not_found,item_not_found

rating_schema = RatingSchema()


class RatingListResource(Resource):
    def get(self):
        ratings = Rating.get_all()
        return rating_schema.dump(ratings).data, HTTPStatus.OK

    @jwt_required
    def post(self, item_id):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = rating_schema.load(data=json_data)
        item = Item.get_by_id(item_id=item_id)

        if errors:
            return {"message": "Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        rating = Rating(**data)
        rating.user_id = current_user
        rating.item_id = item.id
        rating.save()

        return rating_schema.dump(rating).data, HTTPStatus.CREATED
