from flask import Flask


def create_app():
    app = Flask(__name__)
    from api.index import home_, api_, uptime, downloader_web, dl_api, uptime_web
    app.register_blueprint(home_)
    app.register_blueprint(api_)
    app.register_blueprint(uptime)
    app.register_blueprint(uptime_web)
    app.register_blueprint(downloader_web)
    app.register_blueprint(dl_api)

    return app
