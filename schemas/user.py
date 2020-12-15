from marshmallow import Schema, fields
from utils import hash_password
from flask_uploads import url_for

class UserSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    rating = fields.Float(dump_only=True)
    password = fields.Method(required=True, deserialize="load_password")
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    profile_picture = fields.Method(serialize="dump_profile_picture")
    def dump_profile_picture(self, user):
        if user.profile_picture:
            return url_for("static", filename="images/profile-pictures/{}".format(user.profile_picture),
                           _external=True)
        else:
            return url_for("static", filename="images/assets/default-profile.jpg")
    def load_password(self, value):
        return hash_password(value)

