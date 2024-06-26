""" Register all blueprints here """
from auth import auth_api
from user import user_api
from vendor import vendor_api

def register_blueprints(app, prefix):
    app.register_blueprint(auth_api, url_prefix=prefix)
    app.register_blueprint(user_api, url_prefix=prefix)
    app.register_blueprint(vendor_api, url_prefix=prefix)




