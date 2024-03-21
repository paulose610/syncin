from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
db = SQLAlchemy()

#--------------------------------------User------------------------

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False)
    creator_name = db.Column(db.String,unique=True,name='creator_name')
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active=db.Column(db.Boolean())
    sub=db.Column(db.Boolean(), default=False)
    subdate=db.Column(db.DateTime())
    last_played=db.Column(db.String(40), default="")
    albums=db.relationship('Album', backref='creator', lazy=True)
    playlists = db.relationship('Playlist', backref='user', lazy=True)
    likes = db.relationship('Likedsongs', backref='user', lazy=True)
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


#----------------------------------Song------------------------------

class Playlist(db.Model):
    __tablename__='playlist'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', name='usid'), nullable=False)
    songs=db.relationship('Song', backref='playlist', lazy=True)
  
class Likedsongs(db.Model):
    __tablename__='likedsongs'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', name='usid'), nullable=False)
    song_id = db.Column(db.Integer(), db.ForeignKey('song.id', name='soid'), nullable=False)    

class Album(db.Model):
    __tablename__='album'
    id = db.Column(db.Integer(), primary_key=True)
    creator_id=db.Column(db.Integer(), db.ForeignKey('user.id', name='usid'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(255))
    likes = db.Column(db.Integer(), default=0, nullable=False)
    time_played = db.Column(db.Integer(), default=0, nullable=False)
    songs=db.relationship('Song', backref='album', lazy=True)
     

class Song(db.Model):
    __tablename__='song'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    lyrics = db.Column(db.String(20))
    cover = db.Column(db.String(255))
    audio = db.Column(db.String(255),default='defaultsong.mp3', nullable=False)
    likes = db.Column(db.Integer(),default=0,nullable=False)
    time_played = db.Column(db.Integer(), default=0, nullable=False)
    playlist_id=db.Column(db.Integer(), db.ForeignKey('playlist.id', name='plid'))
    creator_id=db.Column(db.Integer(), db.ForeignKey('user.id', name='usid'), nullable=False)
    album_id = db.Column(db.Integer(), db.ForeignKey('album.id', name='alid'))
    genre=db.Column(db.String(), nullable=False)
    



    




