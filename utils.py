from flask_uploads import extension
from passlib.hash import pbkdf2_sha256
import uuid
from extensions import image_set
import os
from PIL import Image

def hash_password(password):
    return pbkdf2_sha256.hash(password)
def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)
def save_image(image, folder):
    filename = "{}.{}".format(uuid.uuid4(), extension(image.filename))
    image_set.save(image, folder=folder, name=filename)
    filename = compress_image(filename=filename, folder=folder)
    return filename
def compress_image(filename, folder):
    file_path = image_set.path(filename=filename, folder=folder)
    image = Image.open(file_path)
    if image.mode != "RGB":
        image = image.convert("RGB")
    if max(image.width, image.height) > 1600:
        maxsize = (1600, 1600)
        image.thumbnail(maxsize, Image.ANTIALIAS)
    compressed_filename = "{}.jpg".format(uuid.uuid4())
    compressed_file_path = image_set.path(filename=compressed_filename,
                                          folder=folder)
    image.save(compressed_file_path, optimize=True, quality=85)
    original_size = os.stat(file_path).st_size
    compressed_size = os.stat(compressed_file_path).st_size
    percentage = round((original_size-compressed_size)/original_size * 100)
    print("size reduced by {}%, from {} to {}".format(percentage, original_size,
                                                      compressed_size))
    os.remove(file_path)
    return compressed_filename