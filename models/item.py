from extensions import db
from sqlalchemy.dialects import postgresql
from sqlalchemy import asc, desc, or_

#item_list = []


class Item(db.Model):

    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    picture = db.Column(db.String(300), default=None)
    tags = db.Column(postgresql.ARRAY(db.String(300)))
    rating = db.Column(db.Float)
    price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    ratings = db.relationship("Rating", backref="item")

    @classmethod
    def get_by_id(cls, item_id):
        return cls.query.filter_by(id=item_id).first()

    @classmethod
    def get_by_tags(cls, q, page, per_page):
        keyword = "%{keyword}%".format(keyword=q)
        return cls.query.filter_by(cls.tags.ilike(keyword).order_by(desc(cls.created_at)).paginate(page=page, per_page=per_page))

    @classmethod
    def get_all(cls, q, page, per_page):
        keyword = "%{keyword}%".format(keyword=q)
        return cls.query.filter_by(cls.tags.ilike(keyword).order_by(desc(cls.created_at)).paginate(page=page, per_page=per_page))

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()