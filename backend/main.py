from flask import Flask
from flask_cors import CORS
from api.endpoints import api_bp
from config.config import PORT

app = Flask(__name__)
CORS(app)

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True, port=PORT)

