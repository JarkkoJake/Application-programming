from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from models.item import Item
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from resources.utils import user_not_found,item_not_found
from webargs import fields
from webargs.flaskparser import use_kwargs
from schemas.item import ItemSchema, ItemPaginationSchema

item_pagination_schema = ItemPaginationSchema()
item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

class ItemListResource(Resource):

    @use_kwargs({"q":fields.Str(missing=""), "page":fields.Int(missing=1), "per_page": fields.Int(missing=20)})

    def get(self, q, page, per_page):

        paginated_items = Item.get_all(q, page, per_page)

        return item_pagination_schema.dump(paginated_items).data, HTTPStatus.OK


    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = item_schema.load(data=json_data)

        if errors:

            return {"message": "Validation errors", "errors" : errors }, HTTPStatus.BAD_REQUEST

        item = Item(**data)
        item.user_id = current_user
        item.save()

        return item_schema.dump(item).data, HTTPStatus.CREATED

class UserItemListResource(Resource):
    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)
        if not user:
            user_not_found()
        items = Item.get_all_by_user(user_id=user.id)
        return item_list_schema.dump(items).data, HTTPStatus.OK

class ItemResource(Resource):

    @jwt_required
    def patch(self, item_id):

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
        item.tags = data.get("tags") or item.tags
        item.ratings = data.get("ratings") or item.ratings
        item.rating = data.get("rating") or item.rating
        item.price = data.get("price") or item.price
        item.amount = data.get("amount") or item.amount

        item.save()

        return item_schema.dump(item).data, HTTPStatus.OK

    @jwt_optional
    def get(self, item_id):

        item = Item.get_by_id(item_id=item_id)

        if item is None:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND

#        current_user = get_jwt_identity()

        return item_schema.dump(item), HTTPStatus.OK

#    @jwt_optional
#    def get(self, tags):
#
#        tags = Item.get_by_tags(tags=tags)
#
#        if tags is None:
#            return {"message": "Items not found with this tag"}, HTTPStatus.NOT_FOUND
#
#        return tags.data(), HTTPStatus.OK

    @jwt_required
    def put(self, item_id):

        json_data = request.get_json()

        item = Item.get_by_id(item_id=item_id)

        if item is None:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != item.user_id:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        item.name = json_data["name"]
        item.description = json_data["description"]
        item.tags = json_data["tags"]
        item.ratings = json_data["ratings"]
        item.rating = json_data["rating"]
        item.price = json_data["price"]
        item.amount = json_data["amount"]

        item.save()

        return item.data, HTTPStatus.OK

    @jwt_required
    def delete(self, item_id):

        item = Item.get_by_id(item_id=item_id)

        if item is None:
            return {"message": "Item not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != item.user_id:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        item.delete()

        return {"message": "Item deleted"}, HTTPStatus.NO_CONTENT

class ItemTagResource(Resource):

    @use_kwargs({"q": fields.Str(missing=""), "page": fields.Int(missing=1), "per_page": fields.Int(missing=20)})
    def get(self, q, page, per_page):
        paginated_items = Item.get_all(q, page, per_page)

        return item_pagination_schema.dump(paginated_items).data, HTTPStatus.OK
