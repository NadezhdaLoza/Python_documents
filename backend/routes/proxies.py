from flask import Blueprint
from controllers.proxies import ProxyController

proxy_router = Blueprint('proxies', __name__, url_prefix="proxies/")
controller = ProxyController()

@proxy_router.get('')
def get_all():
    return controller.get_all()

@proxy_router.get('<id>')
def get_one(id: int):
    return controller.get_one(id)

@proxy_router.post('')
def post():
    return controller.post()

@proxy_router.put('')
def put():
    return controller.put()

@proxy_router.delete('<id>')
def delete(id: int):
    return controller.delete(id)
