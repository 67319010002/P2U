from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

# Import models
from models import User, Product, CartItem, Order, Address

# Import Blueprints
from routes.auth import auth
from routes.seller import seller
from routes.product import product
from routes.seller_rank import seller_rank  # <-- AI Ranking

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup Extensions
    CORS(app, origins="*")
    JWTManager(app)

    # MongoDB Connection
    connect(
        db=app.config["MONGODB_SETTINGS"]["db"],
        host=app.config["MONGODB_SETTINGS"]["host"]
    )

    # Register Blueprints
    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(seller, url_prefix="/api")
    app.register_blueprint(product, url_prefix="/api")
    app.register_blueprint(seller_rank, url_prefix="/api")  # AI Ranking

    # Serve profile files
    @app.route('/static/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        return send_from_directory('static/uploads', filename)

    # Serve product images
    @app.route('/uploads/products/<path:filename>')
    def serve_product_image(filename):
        return send_from_directory('uploads/products', filename)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)
