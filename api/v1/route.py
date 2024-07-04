""" Register all blueprints here """
from auth import auth_api
from user import user_api
from vendor import vendor_api
from food_item import food_item_api
from order import order_api
from order_item import order_item_api
from review import review_api

def register_blueprints(app, prefix):
    app.register_blueprint(auth_api, url_prefix=prefix)
    app.register_blueprint(user_api, url_prefix=prefix)
    app.register_blueprint(vendor_api, url_prefix=prefix)
    app.register_blueprint(food_item_api, url_prefix=prefix)
    app.register_blueprint(order_api, url_prefix=prefix)
    app.register_blueprint(order_item_api, url_prefix=prefix)
    app.register_blueprint(review_api, url_prefix=prefix)



