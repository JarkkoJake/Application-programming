from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from models.item import Item
from models.rating import Rating
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from schemas.rating import RatingSchema
from resources.util import item_not_found

rating_schema = RatingSchema()
rating_list_schema = RatingSchema(many=True)


class RatingListResource(Resource):
    # GET-metodilla haetaan itemin kaikki ratingit
    def get(self, item_id):
        item = Item.get_by_id(item_id=item_id)
        if item is None:
            return item_not_found()
        ratings = Rating.get_by_item(item_id=item.id)
        return rating_list_schema.dump(ratings).data, HTTPStatus.OK

    # POST-metodi ratingin luomiseen
    @jwt_required
    def post(self, item_id):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = rating_schema.load(data=json_data)
        item = Item.get_by_id(item_id=item_id)

        if errors:
            return {"message": "Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        if Rating.get_by_user_item(user_id=current_user, item_id=item.id) is not None:
            return {"message": "You have already rated this item"}

        rating = Rating(**data)
        rating.user_id = current_user
        rating.item_id = item.id
        rating.save()

        update_ratings(item_id=item.id)

        return rating_schema.dump(rating).data, HTTPStatus.CREATED

    # Patch-metodi olemassa olevan ratingin muuttamiseen
    @jwt_required
    def patch(self, item_id):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = rating_schema.load(data=json_data, partial=("name", ))
        item = Item.get_by_id(item_id=item_id)

        if errors:
            return {"message": "Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        if item is None:
            return {"message": "item not found"}, HTTPStatus.NOT_FOUND

        if current_user != item.user_id:
            return {"message": "Access not allowed"}, HTTPStatus.FORBIDDEN

        rating = Rating.get_by_user_item(user_id=current_user, item_id=item.id)

        rating.rating = data.get("rating") or rating.rating
        rating.rating_text = data.get("rating_text") or rating.rating_text

        rating.save()

        update_ratings(item_id=item.id)

        return rating_schema.dump(rating).data, HTTPStatus.OK


# Funktio ratingien päivittämiseen
def update_ratings(item_id):
    # itemiin liittyvät muuttujat
    item = Item.get_by_id(item_id=item_id)
    ratings = Rating.get_by_item(item_id=item_id)
    i_rating = 0.0
    r = 0
    # useriin liittyvät muuttujat
    user = User.get_by_id(id=item.user_id)
    user_items = Item.get_all_by_user(user_id=item.user_id)
    u_rating = 0.0
    ru = 0

    # lasketaan itemin ratingien keskiarvo
    for rating in ratings:
        r = r + 1
        i_rating = i_rating + rating.__dict__["rating"]

    i_rating_dict = {"rating": i_rating / r}
    item.rating = i_rating_dict.get("rating")

    # lasketaan userin kaikkien itemien ratingien keskiarvo
    for rating in user_items:
        ru = ru + 1
        u_rating = u_rating + rating.__dict__["rating"]

    u_rating_dict = {"rating": u_rating / r}
    user.rating = u_rating_dict.get("rating")

    # tallennetaan muutokset
    item.save()
    user.save()
