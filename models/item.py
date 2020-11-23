from extensions import db
from sqlalchemy.dialects import postgresql

item_list = []


class Item(db.Model):

    __tablename__ = "item"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    tags = db.Column(postgresql.ARRAY(db.String(300)))
    ratings = db.Column(postgresql.ARRAY(db.String(300)))
    rating = db.Column(db.Integer)
    price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_id(cls, item_id):
        return cls.query.filter_by(id=item_id).first()

    @classmethod
    def get_by_tags(cls, tags):
        return cls.query.filter_by(tags=tags).all()

    @classmethod
    def get_all(cls):
        return cls.query.filer_by().all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()