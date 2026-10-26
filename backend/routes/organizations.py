from flask import Blueprint
from controllers.organizations import OrganizationController

organization_router = Blueprint('organizations', __name__, url_prefix="organizations/")
controller = OrganizationController()

@organization_router.get('')
def get_all():
    return controller.get_all()

@organization_router.get('<id>')
def get_one(id: int):
    return controller.get_one(id)

@organization_router.post('')
def post():
    return controller.post()

@organization_router.put('')
def put():
    return controller.put()

@organization_router.delete('<id>')
def delete(id: int):
    return controller.delete(id)
