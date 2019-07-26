from flask import Flask 
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:nathanoj35@localhost/User'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='171bac65406834ce5d04ed52'
db=SQLAlchemy(app)

login_manager=LoginManager(app)


from mega import views
login_manager.login_view='Login'
