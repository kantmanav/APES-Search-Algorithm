from flask import Flask
from apes_search.api.routes import v1

app = Flask(__name__)

app.register_blueprint(v1, url_prefix='/api/')