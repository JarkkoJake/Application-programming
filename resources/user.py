from flask import request
from flask_restful import Resource
from http import HTTPStatus
from utils import hash_password, save_image
from models.user import User
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from schemas.user import UserSchema
from resources.utils import user_not_found, item_not_found
from extensions import image_set
import os

user_schema = UserSchema()
user_public_schema = UserSchema(exclude = ("email", "created_at", "updated_at", ))
user_profile_picture_schema = UserSchema(only=("profile_picture", ))

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data = json_data)

        if errors:
            return {"message":"Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get("username")):
            return {"message":"username already used"}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get("email")):
            return {"message":"email already used"}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED

class UserResource(Resource):
    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)
        if not user:
            user_not_found()
        current_user = get_jwt_identity()
        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data
        return data, HTTPStatus.OK
class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id = get_jwt_identity())
        return user_schema.dump(user).data
class UserProfilePictureUploadResource(Resource):
    @jwt_required
    def put(self):
        file = request.files.get("profile_picture")
        if not file:
            return {"message":"Not a valid image"}, HTTPStatus.BAD_REQUEST
        """if not image_set.file_allowed(file, file.filename):
            return {"message":"File type not allowed"}, HTTPStatus.BAD_REQUEST"""
        user = User.get_by_id(id=get_jwt_identity())
        """if user.profile_picture:
            profile_picture_path = image_set.path(folder="profile-pictures", filename=user.profile_picture)
            if os.path.exists(profile_picture_path):
                os.remove(profile_picture_path)"""
        filename = save_image(image=file, folder="profile-pictures")
        user.profile_picture = filename
        user.save()
        return user_profile_picture_schema.dump(user).data, HTTPStatus.OK
