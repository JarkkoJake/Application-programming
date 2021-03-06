from extensions import db

#User constructor
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    items = db.relationship("Item", backref="user")
    rating = db.Column(db.Float())
    profile_picture = db.Column(db.String(300), default=None)
    is_admin = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False,
                           server_default=db.func.now(),
                           onupdate=db.func.now())

#Funktio joka hakee käyttäjänimen mukaan
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
#Funktio joka hakee sähköpostin mukaan
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

# Funktio joka hakee käyttäjän id.n mukaan
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

