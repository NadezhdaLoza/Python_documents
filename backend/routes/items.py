from flask import Blueprint
from controllers.items import ItemController

item_router = Blueprint('items', __name__, url_prefix="items/")
controller = ItemController()

@item_router.get('')
def get_all():
    return controller.get_all()

@item_router.get('<id>')
def get_one(id: int):
    return controller.get_one(id)

@item_router.post('')
def post():
    return controller.post()

@item_router.put('')
def put():
    return controller.put()

@item_router.delete('<id>')
def delete(id: int):
    return controller.delete(id)
