import spacy
from flask import Blueprint, jsonify, request

from apes_search.src.paragraph_search import execute


v1 = Blueprint('api_', __name__)


def load_spacy_model():
	nlp = spacy.load('en_core_web_sm')
	return nlp


nlp_libs = load_spacy_model()


@v1.route('/apes', methods=['POST'])  # HTTP POST request payload
def apes():
	request_obj = request.get_json()
	resp = execute(request_obj, nlp_libs=nlp_libs)
	return jsonify(resp)
