from flask import Flask


def create_app():
    app = Flask(__name__)
    from api.index import home_, api_
    app.register_blueprint(home_)
    app.register_blueprint(api_)

    return app
