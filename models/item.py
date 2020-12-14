from extensions import db
from sqlalchemy.dialects import postgresql
from http import HTTPStatus

#Item constructer
class Item(db.Model):

    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    picture = db.Column(db.String(300), default=None)
    tag1 = db.Column(db.String(15))
    tag2 = db.Column(db.String(15))
    tag3 = db.Column(db.String(15))
    rating = db.Column(db.Float)
    price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    ratings = db.relationship("Rating", backref="item")

#Funktio joka hakee id.n mukaan esineitä
    @classmethod
    def get_by_id(cls, item_id):
        return cls.query.filter_by(id=item_id).first()

#Funktio joka hakee tagien mukaan esineitä
    @classmethod
    def get_by_tag(cls, tags):
        return cls.query.filter_by(tag1=tags).all() + cls.query.filter_by(tag2=tags).all() + cls.query.filter_by(tag3=tags).all()

#Funktio joka hakee nimen mukaan esineitä
    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).all()

#Funktio joka hakee kaikki esineet
    @classmethod
    def get_all(cls):
        return cls.query.all()

#Funktio joka hakee tietyn käyttäjän kaikki itemit
    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()