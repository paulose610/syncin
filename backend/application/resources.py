from flask_restful import Resource, Api, reqparse, fields, marshal
from flask_security import auth_token_required, current_user
from flask import jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from .sec import datastore
from .models import db, User, Role, Playlist, Likedsongs, Album, Song
import os
from .config import Config


api=Api(prefix='/api')

class login(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)

    def post(self):
        args= self.parser.parse_args()
        email=args.get("email")    
        password=args.get("password")

        user=datastore.find_user(email=email)
        
        if not user:
            print('user does not exist')
            return make_response(jsonify({"message":"User doesn't exist!"}), 400)
        
        elif user and check_password_hash(user.password,password):
            token=user.get_auth_token()
            print("success!")
            return jsonify({
                            "token": token,
                             "email": user.email,
                             "username":user.username,
                             "role": user.roles[0].name,
                             "id":user.id,
                             "creator_name":user.creator_name  
                             })
        
        elif user.email=='admin@syncin.ac.in':
            return make_response(jsonify({"message":"Incorrect password"}), 400)
        else:
            return make_response(jsonify({"message":"Incorrect username or password"}), 400)

api.add_resource(login, '/login')

class register(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        self.parser.add_argument('creator', type=bool, required=True)
        self.parser.add_argument('crtrname', type=str, required=True)

    def post(self):
        args= self.parser.parse_args()
        password=args.get("password")
        uname=args.get("username")
        email=args.get("email")
        creator=args.get("creator")
        crtrname=args.get('crtrname')

        user=datastore.find_user(email=email)
        if (email=="admin@syncin.ac.in"):
             return make_response(jsonify({"message":"Enter a valid email!"}), 400)
        if user:
            return make_response(jsonify({"message":"Email already exists!"}), 400)
        
        if crtrname:
            user=datastore.find_user(creator_name=crtrname)
        if user:
            return make_response(jsonify({"message":"creator Name already exists!"}), 400)
        r="creator" if creator else "user"
        
        datastore.create_user(email=email,
                              password=generate_password_hash(password),
                              username=uname,
                              roles=[r],
                              active=1,
                              sub=False,
                              creator_name=crtrname
                              )
    
        db.session.commit()
        user=datastore.find_user(email=email)
        return jsonify({"userdata":{
                            "token": user.get_auth_token(),
                            "email": user.email,
                            "username":user.username,
                            "role": user.roles[0].name,
                            "id": user.id,
                            "last_played": user.last_played,
                            "creator_name":user.creator_name
                            },
                        "message":"account created"})

api.add_resource(register, '/register')    

class authenticate(Resource):

    @auth_token_required
    def get(self):
        return jsonify({'authenticated': current_user.roles[0].name})

        
api.add_resource(authenticate, '/authenticate') 


class retreive(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser() 
        self.parser.add_argument('cname', type=str, required=True)
        self.parser.add_argument('email', type=str, required=True)
    
    @auth_token_required
    def get(self):
        return jsonify({"email": current_user.email,
                        "username":current_user.username,
                        "role": current_user.roles[0].name,
                        "id": current_user.id,
                        "creator_name": current_user.creator_name,
                        "last_played": current_user.last_played
                        })
    def put(self):
        args= self.parser.parse_args()
        crtrname=args.get("cname")  
        email=args.get("email")
        print(crtrname)  
        print(email)    
        crtr=datastore.find_user(creator_name=crtrname)
        print(crtr)
        if crtr is None:
            user=datastore.find_user(email=email)
            current_role=Role.query.get(1)
            new_role=Role.query.get(2)
            user.roles.remove(current_role)
            user.roles.append(new_role)
            user.creator_name=crtrname
            db.session.commit()
            return jsonify({'changed':True})
        else:
            return make_response(jsonify({'changed': False}),404)
    
api.add_resource(retreive,'/retreive')  


#----------------------------------------Library------------------------------------

playlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

likedsongs_fields = {
    'id': fields.Integer,
    'song_id': fields.Integer
}

album_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'likes': fields.Integer,
    'creator_id': fields.Integer,
    'cover': fields.String,
}

song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'lyrics': fields.String,
    'cover': fields.String,
    'audio': fields.String,
    'likes': fields.Integer,
    'time_played': fields.Integer,
    'playlist_id': fields.Integer,
    'creator_id': fields.Integer,
    'album_id': fields.Integer,
    'genre': fields.String
}


class playlists(Resource):

    @auth_token_required
    def get(self):
        user=current_user
        playlists=user.playlists
        return jsonify(marshal(playlists,playlist_fields))

api.add_resource(playlists,'/playlists')  

class likedsongs(Resource):
    @auth_token_required
    def get(self):
        user=current_user
        likedsongs=Likedsongs.query.filter(Likedsongs.user_id==user.id).all()
        return jsonify(marshal(likedsongs,likedsongs_fields))

api.add_resource(likedsongs, '/likedsongs')

class albums(Resource):
    
    def get(self):
        uid=request.args.get('uid')
        ur=request.args.get('ur')
        allalbums=Album.query.all()
        allalbums=marshal(allalbums,album_fields)
        response={'allalbums':allalbums}
        
        if ur=='creator':
            print(ur)
            albums=Album.query.filter(Album.creator_id==uid).all()
            albums=marshal(albums,album_fields)
            response['albums']=albums
            print(response['albums'])

        return jsonify(response) 
    
    @auth_token_required
    def post(self):
        user=current_user
        name = request.form['album']

        imgext ={'jpg','png'}

        def allowed_img(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower() in imgext
        
        def imgtype(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower()
        
        new_album=Album.query.filter(Album.name==name, Album.creator_id==user.id).first()
        if new_album:
            print(new_album)
            return make_response(jsonify({"error":"You've already used this album name!"}),400)
        
        new_album=Album(name=name, creator_id=user.id,likes=0)

        db.session.add(new_album)
        db.session.commit()

        if 'cover' in request.files:
            new_album=Album.query.filter(Album.name==name, Album.creator_id==user.id).first()
            id=new_album.id
            cover_image = request.files['cover']
            imgid='alb'+str(id)+'.'+imgtype(cover_image.filename)
            if cover_image and allowed_img(cover_image.filename):
                new_album.cover=imgid
                cover_image.save(os.path.join(Config.UPLOAD_FOLDER,imgid))
            else:
                return make_response(jsonify({'error':'Only jpg/png images allowed!'}),400)
            db.session.commit()


        return jsonify({
            'id': new_album.id,
            'name': new_album.name,
            'cover': new_album.cover,
            'likes': new_album.likes,
            'time_played': new_album.time_played,
            'creator_id': new_album.creator_id,
        })
    
    @auth_token_required
    def put(self):
        aid=request.form['aid']
        name = request.form['album']
        removecover=request.form['removecover']
        
        cover_image=None
        imgext={'jpg','png'}

        def allowed_img(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower() in imgext
        def imgtype(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower()
        
        if int(aid)>-1:
            album=Album.query.filter(Album.id==aid, Album.creator_id==current_user.id).first()
            if not album:
                return make_response(jsonify({"error":"No such Album exists!"}))
            album.name=name
            if 'cover' in request.files and (removecover=='false'):
                cover_image=request.files['cover']
                if cover_image and allowed_img(cover_image.filename):
                    if not album.cover:
                        imgid='alb'+str(aid)+'.'+str(imgtype(cover_image.filename))
                        print(imgid)
                        album.cover=imgid
                        print(album.cover)
                        cover_image.save(os.path.join(Config.UPLOAD_FOLDER,imgid))
                    else:
                        cover_image.save(os.path.join(Config.UPLOAD_FOLDER,album.cover))
                else:
                    return make_response(jsonify({'error':'Only jpeg/png images allowed!'}),400)
            
            elif removecover and album.cover:
                path=os.path.join(Config.UPLOAD_FOLDER,album.cover)
                if os.path.exists(path):
                    os.remove(path)
                    album.cover=None

            db.session.commit()

            return jsonify({
                'id': album.id,
                'name': album.name,
                'cover': album.cover,
                'likes': album.likes,
                'time_played': album.time_played,
                'creator_id': album.creator_id,
            })

        else: return make_response(jsonify({'error':"couldn't identify album!"}),400)


    @auth_token_required
    def delete(self):
        user=current_user
        cond=request.args.get('cond')
        aid=request.args.get('aid')

        album=Album.query.filter(Album.id==aid , Album.creator_id==user.id).first()
        if not album:
            return make_response(jsonify({'error':"album doesn't exist!"}),400)        
        else:
            if album.cover:
                imgtodel=album.cover
                path=os.path.join(Config.UPLOAD_FOLDER,imgtodel)
                if os.path.exists(path):
                    os.remove(path)
            
            uas=Song.query.filter(Song.creator_id==user.id,Song.album_id==aid)
            if cond==1:
                for song in uas:
                    if song.cover:
                        imgtodel=song.cover
                        path=os.path.join(Config.UPLOAD_FOLDER,imgtodel)
                        if os.path.exists(path):
                            os.remove(path)

                    if song.audio:
                        audtodel=song.audio
                        path=os.path.join(Config.UPLOAD_FOLDER,audtodel)
                        if os.path.exists(path):
                            os.remove(path)
                            
                    db.session.delete(song)

            if cond==2:
                for song in uas:
                    song.album_id=None

            db.session.delete(album)
            db.session.commit()

            return make_response(jsonify({
                                          'msg':"album deleted successfully!",
                                          'delinfo':{
                                              'id': aid,
                                              'cond': cond
                                              }
                                          }),200)        



api.add_resource(albums,'/albums')      



class songs(Resource):

    def get(self):
        uid=request.args.get('uid')
        ur=request.args.get('ur')
        allsongs=Song.query.all()
        allsongs=marshal(allsongs,song_fields)
        response = {'allsongs': allsongs}
        
        if ur=='creator':
            songs=Song.query.filter(Song.creator_id==uid).all()
            songs=marshal(songs,song_fields)
            response['songs'] = songs
        
        return jsonify(response)   

    @auth_token_required
    def post(self): 
        user=current_user
        title = request.form['title']
        album = request.form['album']
        genre = request.form['genre']
        lyrics = request.form['lyrics']
        
        audio_file=None
        cover_image = None
        al=None

        audext = {'mp3'}
        imgext ={'jpg','png'}

        if album!='':
            al=Album.query.filter(Album.name==album, Album.creator_id==user.id).first()
            if not al:
                return make_response(jsonify({'error':"album doesn't exist!"}),400)
            alid=al.id

        if 'audio' in request.files:
            audio_file = request.files['audio']
            print('yes')
        
        def allowed_audio(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower() in audext
        def allowed_img(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower() in imgext
        def imgtype(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower()
            
        
        if not audio_file:
            return make_response(jsonify({'error':'no audio file present'}),400)
           
        song=Song.query.filter(Song.creator_id==user.id, Song.title==title).first()
        if song:
            return make_response(jsonify({'error':'title already used by you!'}),400)
        if not allowed_audio(audio_file.filename):
            return make_response(jsonify({'error':'Only mp3 audio files allowed!'}),400)
        else:
            new_song = Song(title=title, genre=genre, lyrics=lyrics, creator_id=user.id, audio='dummy', likes=0, time_played=0)

        db.session.add(new_song)
        db.session.commit()

        new_song=Song.query.filter(Song.creator_id==user.id, Song.title==title).first()
        id=new_song.id
        audid='aud'+str(id)+'.mp3'
        new_song.audio=audid
        audio_file.save(os.path.join(Config.UPLOAD_FOLDER,audid))

        if 'cover' in request.files:
            cover_image = request.files['cover']
            imgid='img'+str(id)+'.'+imgtype(cover_image.filename)
            if cover_image and allowed_img(cover_image.filename):
                new_song.cover=imgid
                cover_image.save(os.path.join(Config.UPLOAD_FOLDER,imgid))
            else:
                return make_response(jsonify({'error':'Only jpeg/png images allowed!'}),400)

        if album!='':
            new_song.album_id=alid 

        db.session.commit()

        print(new_song)

        return jsonify({
            'id': new_song.id,
            'title': new_song.title,
            'lyrics': new_song.lyrics,
            'cover': new_song.cover,
            'audio': new_song.audio,
            'likes': new_song.likes,
            'time_played': new_song.time_played,
            'playlist_id': new_song.playlist_id,
            'creator_id': new_song.creator_id,
            'album_id': new_song.album_id,
            'genre': new_song.genre    
        })   
    

    @auth_token_required
    def put(self):
        user=current_user
        sid=request.form['sid']
        title = request.form['title']
        album = request.form['album']
        genre = request.form['genre']
        lyrics = request.form['lyrics']
        removecover=request.form['removecover']

        audio_file=None
        cover_image = None
        al=None
        song=None

        audext = {'mp3'}
        imgext ={'jpg','png'}

        print('392')

        def allowed_audio(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower() in audext
        def allowed_img(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower() in imgext
        def imgtype(filename):
            return '.' in filename and \
                    filename.rsplit('.', 1)[1].lower()

        if int(sid)>-1:
            song=Song.query.filter(Song.id==sid, Song.creator_id==user.id).first()
            print(song.title)
            if not song:
                return make_response(jsonify({'error':"Song doesn't exist!"}),400)

            if song.title!=title:
                song.title=title
            if song.lyrics!=lyrics:
                song.lyrics=lyrics
            if album!='':
                al=Album.query.filter(Album.name==album, Album.creator_id==user.id).first()
                if not al:
                    return make_response(jsonify({'error':"album doesn't exist!"}),400)
                alid=al.id
                if song.album_id!=alid:
                    song.album_id=alid
            else:
                song.album_id=None

            if song.genre!=genre:
                song.genre=genre

            if 'audio' in request.files:
                print('hi')
                audio_file = request.files['audio']
                if audio_file and allowed_audio(audio_file.filename):
                        audio_file.save(os.path.join(Config.UPLOAD_FOLDER,song.audio))
                else: return make_response(jsonify({'error':'Only mp3 audio files allowed!'}),400)        

            if 'cover' in request.files and (removecover=='false'):
                cover_image=request.files['cover']
                if cover_image and allowed_img(cover_image.filename):
                    if not song.cover:
                        imgid='img'+str(sid)+'.'+str(imgtype(cover_image.filename))
                        print(imgid)
                        song.cover=imgid
                        print(song.cover)
                        cover_image.save(os.path.join(Config.UPLOAD_FOLDER,imgid))
                    else:
                        cover_image.save(os.path.join(Config.UPLOAD_FOLDER,song.cover)) 

                else:  return make_response(jsonify({'error':'Only jpeg/png images allowed!'}),400)  
            
            elif removecover and song.cover:
                path=os.path.join(Config.UPLOAD_FOLDER,song.cover)
                if os.path.exists(path):
                    os.remove(path)
                    song.cover=None


            db.session.commit()

            return jsonify({
                'id': song.id,
                'title': song.title,
                'lyrics': song.lyrics,
                'cover': song.cover,
                'audio': song.audio,
                'likes': song.likes,
                'time_played': song.time_played,
                'playlist_id': song.playlist_id,
                'creator_id': song.creator_id,
                'album_id': song.album_id,
                'genre': song.genre    
            })


        else: return make_response(jsonify({'error':"couldn't identify song!"}),400)


    @auth_token_required
    def delete(self):
        sid=request.args.get('sid')

        print(sid)
        song=Song.query.filter(Song.id==sid , Song.creator_id==current_user.id).first()
        if not song:
            return make_response(jsonify({'error':"Song doesn't exist!"}),400)        
        else:
            if song.cover:
                imgtodel=song.cover
                path=os.path.join(Config.UPLOAD_FOLDER,imgtodel)
                if os.path.exists(path):
                    os.remove(path)

            if song.audio:
                audtodel=song.audio
                path=os.path.join(Config.UPLOAD_FOLDER,audtodel)
                if os.path.exists(path):
                    os.remove(path)

            db.session.delete(song)
            db.session.commit()

            return make_response(jsonify({
                                          'msg':"Song deleted successfully!",
                                          'id': sid
                                          }),200)                                  


api.add_resource(songs,'/songs')







