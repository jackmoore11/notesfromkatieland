import os
import secrets
import subprocess
from flask import current_app

def saveVideo(formVideo):
    randomHex = secrets.token_hex(8)
    _, fext = os.path.splitext(formVideo.filename)
    fname = randomHex + '.mp4'
    fpath = os.path.join(current_app.root_path, 'static', 'videos', fname)
    if fext.lower() != '.mov':
        formVideo.save(fpath)
    else:
        fnameTmp = randomHex + fext
        fpathTmp = os.path.join(current_app.root_path, 'static', 'videos', 'tmp', fnameTmp)
        formVideo.save(fpathTmp)
        subprocess.call(['ffmpeg', '-i', fpathTmp, fpath, '-hide_banner', '-loglevel', 'error'])
        subprocess.call(['rm', fpathTmp])
    return fname