from flask_uploads import extension
from passlib.hash import pbkdf2_sha256
import uuid
from extensions import image_set

def hash_password(password):
    return pbkdf2_sha256.hash(password)
def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)
def save_image(image, folder):
    filename = "{}.{}".format(uuid.uuid4(), extension(image.filename))
    image_set.save(image, folder=folder, name=filename)
    return filename