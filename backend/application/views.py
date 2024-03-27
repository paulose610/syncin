from flask import current_app as app, send_from_directory, jsonify, send_file
from .config import Config
import os
from .models import User
from flask_restful import marshal, fields
from .instances import cache
import redis
import io
from flask_security import auth_token_required, current_user
from .tasks import *

@app.route('/',methods=['GET'])
def home():
    return('welcome')

@app.route('/cover/<filename>')
@cache.cached(timeout=1800)
def get_cover(filename):
    redis_conn = redis.Redis()
    cover_image= redis_conn.get(filename)
    if cover_image: return send_file(io.BytesIO(cover_image),mimetype='image/jpeg') 
    else:
        cover_path=os.path.join(Config.UPLOAD_FOLDER,filename)   
        if not os.path.exists(cover_path):
            cover_image=redis_conn.get('defaultcover') 
            if cover_image:
                return send_file(io.BytesIO(cover_image),mimetype='image/jpeg')    
            else:
                cover_path=os.path.join(Config.UPLOAD_FOLDER,'defaultcover.jpg')
                filename='defaultcover'
        with open(cover_path, 'rb') as f:
            cover_image = f.read()
            redis_conn.set(filename, cover_image)   

    return send_file(io.BytesIO(cover_image),mimetype='image/jpeg')


@app.route('/audio/<filename>')
@cache.cached(timeout=1800)
def get_audio(filename):
    redis_conn = redis.Redis()
    audio_file= redis_conn.get(filename)
    if audio_file is None:
        audio_path=os.path.join(Config.UPLOAD_FOLDER,filename)
        if not os.path.exists(audio_path):
            audio_file=redis_conn.get('defaultaudio')    
            if audio_file is None:
                audio_path=os.path.join(Config.UPLOAD_FOLDER,'defaultaudio.mp3')
                filename='defaultaudio'
        with open(audio_path, 'rb') as f:
            audio_file = f.read()
            redis_conn.set(filename, audio_file)   

    return send_file(io.BytesIO(audio_file),mimetype='audio/mp3')

@app.route('/getcreators',methods=['GET'])
def get_creators():
    creators=User.query.filter(User.creator_name!='').all()
    creator_fields={
        'id': fields.Integer,
        'creator_name': fields.String,
        'clikes': fields.Integer 
    }
    data = marshal(creators, creator_fields)
    response = jsonify(data)
    return response



