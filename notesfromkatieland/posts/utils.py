import os
import secrets
from PIL import Image, ImageOps
from flask import current_app

def savePicture(formPicture):
    randomHex = secrets.token_hex(8)
    _, fext = os.path.splitext(formPicture.filename)
    fname = randomHex + fext
    fpath = os.path.join(current_app.root_path, 'static', 'post_pics', fname)

    outputSize = (500, 500)
    img = Image.open(formPicture)
    img = ImageOps.exif_transpose(img)
    img.thumbnail(outputSize)
    img.save(fpath)

    return fname