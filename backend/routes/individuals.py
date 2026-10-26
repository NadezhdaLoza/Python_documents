from flask import Blueprint
from controllers.individuals import IndividualController

individual_router = Blueprint('individuals', __name__, url_prefix="individuals/")
controller = IndividualController()

@individual_router.get('')
def get_all():
    return controller.get_all()

@individual_router.get('<id>')
def get_one(id: int):
    return controller.get_one(id)

@individual_router.post('')
def post():
    return controller.post()

@individual_router.put('')
def put():
    return controller.put()

@individual_router.delete('<id>')
def delete(id: int):
    return controller.delete(id)
