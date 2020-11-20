from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
# from config import (Config)
# from resources.item import (all resources)
# from resources.user import (all resources)
# from resources.token import (all resources, black_list)
# from extensions import jwt, db

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)
    register_extensions(app)
    # register_resources(app)
    return app
def register_extensions(app):
    # db.init_app(app)
    # migrate = Migrate(app, db)
    # jwt.init_app(app)
    # @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token["jti"]
        # return jti in black_list

def register_resources(app):
    api = Api(app)
    # api.add_resource(UserListResource, "/users")
    # api.add_resource(UserResource, "/users/<string:username>")
    # api.add_resource(UserItemListResource, "/users/<string:username>/items")
    # api.add_resource(MeResource, "/me")
    # api.add_resource(ItemListResource, "/items")
    # api.add_resource(ItemResource, "/items/<int:item_id>")
    # api.add_resource(ItemRatingsResource, "/items/<int:item_id>/ratings")

if __name__ == "__main__":
    app = create_app()
    app.run(port=5050, debug=True)