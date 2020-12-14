from marshmallow import Schema, fields, post_dump,\
    ValidationError, validates, validate
from schemas.user import UserSchema
from schemas.item import ItemSchema

class RatingSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    item_id = fields.Nested(ItemSchema, attribute="item",
                            dump_only=True,
                            only=["id"])
    rating = fields.Integer(required=True)
    rating_text = fields.String(validate=[validate.Length(max=2000)])
    author = fields.Nested(UserSchema, attribute="user",
                           dump_only=True,
                           only=["id", "username"])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data": data}
        return data

    @validates("rating")
    def validate_rating(self, value):
        if value < 0:
            raise ValidationError("Rating must be 0-5.")
        elif value > 5:
            raise ValidationError("Rating must be 0-5.")
