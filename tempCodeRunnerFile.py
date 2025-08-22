from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.upload_routes import upload_bp, report_bp  # import report_bp
from routes.history_routes import history_bp
from routes.user_routes import user_bp  

app = Flask(__name__)

# Enable CORS so Android app can access backend
CORS(app)

# JWT setup
app.config["JWT_SECRET_KEY"] = "your-very-secret-key"  # Replace with strong secret
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(upload_bp, url_prefix="/upload")
app.register_blueprint(report_bp, url_prefix="/report")  # new blueprint
app.register_blueprint(history_bp, url_prefix="/history")
app.register_blueprint(user_bp, url_prefix="/user")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
