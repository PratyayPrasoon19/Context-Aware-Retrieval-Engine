from flask import Flask
from flask_cors import CORS

from api.endpoints import api_bp
from config.config import PORT

from pkg.services.rag_pipeline import rag_pipeline

app = Flask(__name__)
CORS(app)

# Initialize Vector Database at server startup
rag_pipeline.load_and_prepare_db()

# Register API blueprint
app.register_blueprint(api_bp, url_prefix='/api')


if __name__ == "__main__":
    app.run(debug=True, port=PORT)