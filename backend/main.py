from flask import Flask, jsonify
from flask_cors import CORS
from application.config import DevelopmentConfig
from application.sec import datastore
from flask_security import SQLAlchemyUserDatastore, Security
from application.models import db
from application.resources import api
from flask_migrate import Migrate

def create_app():
    app=Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate=Migrate(app,db)
    api.init_app(app)
    app.security=Security(app,datastore)
    with app.app_context():
        import application.views
    
    return app

app=create_app()

CORS(app,resources={r"/*":{'origins':"*"}})

if __name__=="__main__":
    app.run(debug=True)