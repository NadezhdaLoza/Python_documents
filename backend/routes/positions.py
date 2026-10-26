from flask import Blueprint
from controllers.positions import PositionController

position_router = Blueprint('positions', __name__, url_prefix="positions/")
controller = PositionController()

@position_router.get('')
def get_all():
    return controller.get_all()

@position_router.get('<id>')
def get_one(id: int):
    return controller.get_one(id)

@position_router.post('')
def post():
    return controller.post()

@position_router.put('')
def put():
    return controller.put()

@position_router.delete('<id>')
def delete(id: int):
    return controller.delete(id)
