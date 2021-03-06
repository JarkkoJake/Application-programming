from marshmallow import Schema, fields, post_dump,\
    ValidationError, validates, validate
from schemas.user import UserSchema
from flask_uploads import url_for


class ItemHistorySchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    original_item_id = fields.Integer()
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    tag1 = fields.String(required=False, validate=[validate.Length(max=15)])
    tag2 = fields.String(required=False, validate=[validate.Length(max=15)])
    tag3 = fields.String(required=False, validate=[validate.Length(max=15)])
    price = fields.Float()
    amount = fields.Integer()
    rating = fields.Float()
    author = fields.Nested(UserSchema, attribute="user",
                           dump_only=True,
                           only=["id", "username"])
    created_at = fields.DateTime(dump_only=True)
    picture = fields.Method(serialize="dump_picture")

    def dump_picture(self, item):
        if item.picture:
            return url_for("static", filename="images/pictures/{}".format(item.picture),
                           _external=True)
        else:
            return url_for("static", filename="images/assets/default-item.jpg")

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data":data}
        return data