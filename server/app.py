from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.task_routes import task_bp
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)
app.config["JWT_SECRET_KEY"] = "your-secret-key"
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp) 

@app.route('/')
def home():
    return{"message": "Backend is running"}

if __name__ == '__main__':
    app.run(debug=True)