""" Register all blueprints here """
from views.auth_view import auth_view
from views.vendor_view import vendor_view

def register_blueprints(app, prefix=None):
    app.register_blueprint(auth_view, url_prefix=prefix)
    app.register_blueprint(vendor_view, url_prefix=prefix)
