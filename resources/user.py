from flask import request
from flask_restful import Resource
from http import HTTPStatus
from utils import hash_password, save_image
from models.user import User
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required, fresh_jwt_required
from schemas.user import UserSchema
from resources.util import user_not_found, item_not_found
from extensions import image_set
import os

user_schema = UserSchema()
user_public_schema = UserSchema(exclude = ("email", "created_at", "updated_at", ))
user_profile_picture_schema = UserSchema(only=("profile_picture", ))

class UserListResource(Resource):   #Käyttäjän teko
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data = json_data)

        if errors:
            return {"message":"Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get("username")): #Tarkistaa onko tällä käyttäjänimellä jo käyttäjä
            return {"message":"username already used"}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get("email")):    #Tarkistaa onko tällä sähköpostilla jo käyttäjä
            return {"message":"email already used"}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user).data, HTTPStatus.CREATED

class UserResource(Resource):   #Hakee käyttäjän joko JWT.n kanssa tai ilman
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

    @fresh_jwt_required
    def patch(self, username):  #Päivittää käyttäjän tiedot ja vaatii freshin tokenin.
        json_data = request.get_json()
        data, errors = user_schema.load(data = json_data, partial=("name",))
        current_user = get_jwt_identity()
        user = User.get_by_username(username=username)

        if errors:
            return {"message":"Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        if user.id != current_user:
            return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

        user.username = data.get("username") or user.username
        user.email = data.get("email") or user.email
        user.password = data.get("password") or user.password

        user.save()
        return user_schema.dump(user).data, HTTPStatus.OK

class MeResource(Resource):     #Hakee käyttäjän JWT.n mukaan
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
        if not image_set.file_allowed(file, file.filename):
            return {"message":"File type not allowed"}, HTTPStatus.BAD_REQUEST
        user = User.get_by_id(id=get_jwt_identity())
        if user.profile_picture:
            profile_picture_path = image_set.path(folder="profile-pictures", filename=user.profile_picture)
            if os.path.exists(profile_picture_path):
                os.remove(profile_picture_path)
        filename = save_image(image=file, folder="profile-pictures")
        user.profile_picture = filename
        user.save()
        return user_profile_picture_schema.dump(user).data, HTTPStatus.OK
