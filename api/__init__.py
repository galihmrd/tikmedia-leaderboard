from flask import Flask


def create_app():
    app = Flask(__name__)
    from api.index import home_, api_, uptime, downloader_web, dl_api, is_tikmedia_member, tikmedia_unblock, tikmedia_unblock_web, tikmedia_privacy_web, tikmedia_terms_web, uptime_web
    app.register_blueprint(home_)
    app.register_blueprint(api_)
    app.register_blueprint(uptime)
    app.register_blueprint(uptime_web)
    app.register_blueprint(downloader_web)
    app.register_blueprint(dl_api)
    app.register_blueprint(is_tikmedia_member)
    app.register_blueprint(tikmedia_unblock)
    app.register_blueprint(tikmedia_unblock_web)
    app.register_blueprint(tikmedia_privacy_web)
    app.register_blueprint(tikmedia_terms_web)

    return app
