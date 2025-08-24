import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.upload_routes import upload_bp, report_bp
from routes.history_routes import history_bp
from routes.user_routes import user_bp

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-very-secret-key")

jwt = JWTManager(app)

app.register_blueprint(upload_bp, url_prefix="/upload")
app.register_blueprint(report_bp, url_prefix="/report")
app.register_blueprint(history_bp, url_prefix="/history")
app.register_blueprint(user_bp, url_prefix="/user")

@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Consider removing debug=True for production
