from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from config import Config
from resources.item import ItemListResource, UserItemListResource, ItemResource, ItemTagResource, ItemPictureUploadResource
from resources.user import UserListResource, UserResource, MeResource, UserProfilePictureUploadResource
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list
from resources.rating import RatingListResource
from extensions import jwt, db, image_set
from flask_uploads import configure_uploads, patch_request_class

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    configure_uploads(app, image_set)
    patch_request_class(app, 10*1024*1024)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token["jti"]
        return jti in black_list

def register_resources(app):
    api = Api(app)
    api.add_resource(UserListResource, "/users")
    api.add_resource(UserResource, "/users/<string:username>")
    api.add_resource(UserItemListResource, "/users/<string:username>/items")
    api.add_resource(UserProfilePictureUploadResource, "/users/profile_picture")
    api.add_resource(MeResource, "/me")
    api.add_resource(ItemListResource, "/items")
    api.add_resource(ItemResource, "/items/<int:item_id>")
    api.add_resource(ItemTagResource, "/tags")
    api.add_resource(ItemPictureUploadResource, "/items/<int:item_id>/picture")
    # api.add_resource(ItemRatingsResource, "/items/<int:item_id>/ratings")
    api.add_resource(TokenResource, "/token")
    api.add_resource(RefreshResource, "/refresh")
    api.add_resource(RevokeResource, "/revoke")
    api.add_resource(RatingListResource, "/items/<int:item_id>/ratings")

if __name__ == "__main__":
    app = create_app()
    app.run(port=5050)
