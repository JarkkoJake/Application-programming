from marshmallow import Schema, fields, post_dump,\
    ValidationError, validates, validate
from schemas.user import UserSchema

class ItemSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    tags = fields.Raw()
    price = fields.Float()
    amount = fields.Integer()
    rating = fields.Float()
    author = fields.Nested(UserSchema, attribute="user",
                           dump_only=True,
                           only=["id","username"])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data":data}
        return data
