from flask import Flask
from flask.blueprints import Blueprint
from flask_cors import CORS
import routes
import config

server  = Flask(__name__)

if config.ENABLE_CORS:
    cors    = CORS(server, resources={r"/api/*": {"origins": "*"}})

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.API_URL_PREFIX)

if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
