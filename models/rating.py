from extensions import db
from models.item import Item
from models.user import User


class Rating(db.Model):

    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer(), db.ForeignKey("item.id"))
    rating = db.Column(db.Integer())
    rating_text = db.Column(db.String(2000))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_item(cls, item_id):
        return cls.query.filter_by(item_id=item_id).all()

    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_all(cls):
        return cls.query.filter_by().all()

    @classmethod
    def get_by_user_item(cls, user_id, item_id):
        return cls.query.filter_by(user_id=user_id, item_id=item_id).first()



    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
