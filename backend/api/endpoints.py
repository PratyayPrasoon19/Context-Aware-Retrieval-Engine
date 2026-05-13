from flask import Blueprint, request, jsonify
from pkg.handler.handler import handle_search_request

api_bp = Blueprint('api', __name__)

@api_bp.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    response, status_code = handle_search_request(data)
    return jsonify(response), status_code