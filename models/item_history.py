from extensions import db
from sqlalchemy.dialects import postgresql


# HistoryItem constructor
class HistoryItem(db.Model):

    __tablename__ = "item_history"

    id = db.Column(db.Integer, primary_key=True)
    original_item_id = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    picture = db.Column(db.String(300), default=None)
    tag1 = db.Column(db.String(15))
    tag2 = db.Column(db.String(15))
    tag3 = db.Column(db.String(15))
    rating = db.Column(db.Float)
    price = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())

# Funktio joka hakee original_item_id:n mukaan kaikki esineet
    @classmethod
    def get_by_original_item_id(cls, item_id):
        return cls.query.filter_by(original_item_id=item_id).all()

# Funktio joka hakee kaikki esineet item_history tablesta
    @classmethod
    def get_all(cls):
        return cls.query.all()

# Funktio joka hakee user_id:n mukaan kaikki esineet
    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
