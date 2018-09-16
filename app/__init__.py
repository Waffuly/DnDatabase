from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES
from pathlib import Path, PureWindowsPath

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config.from_object(Config)

photo_path = PureWindowsPath("app\\static\\img")
pure_path = Path(photo_path)

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOADED_PHOTOS_DEST'] = pure_path
configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)

if __name__ == '__main__':
	app.run(debug=True)

from app import routes, models