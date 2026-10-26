from flask import Blueprint
from controllers.damages import DamageController

damage_router = Blueprint('damages', __name__, url_prefix="damages/")
controller = DamageController()

@damage_router.get('')
def get_all():
    return controller.get_all()

@damage_router.get('<id>')
def get_one(id: int):
    return controller.get_one(id)

@damage_router.post('')
def post():
    return controller.post()

@damage_router.put('')
def put():
    return controller.put()

@damage_router.delete('<id>')
def delete(id: int):
    return controller.delete(id)
