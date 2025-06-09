from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configurations for your app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proxima.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5b3VyX3VzZXJfaWRfaGVyZSIsImV4cCI6MTc0OTI0OTk3MX0.rkGR96haAK-PxPoziMfjFc_4ZZhvmmoTSqaDSfeg1ic'  # Use a strong secret key here
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)  # access token valid for 7 days
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # refresh token valid for 30 days
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Enable CORS for your frontend (http://localhost:3000)
    # Allow all necessary HTTP methods and headers
    CORS(app, resources={r"/api/*": {
        "origins": "http://localhost:3000",  # Ensure this matches the frontend origin
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

    # Register Blueprints for routing
    from .routes.auth import auth_bp
    from .routes.groups import groups_bp
    from .routes.transactions import transactions_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(groups_bp, url_prefix='/api/groups')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    
    @app.route('/')
    def home():
        return {"message": "Welcome to Proxima Centauri API"}

    @app.before_request
    def handle_options():
        # Handling the OPTIONS method explicitly
        if request.method == "OPTIONS":
            response = app.make_response('')
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

    return app
