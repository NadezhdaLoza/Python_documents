from flask import Blueprint
from controllers.requests import RepairRequestController

router = Blueprint('repair_requests', __name__, url_prefix="repair_requests/")
controller = RepairRequestController()

@router.get('')
def get_all():
    return controller.get_all()

@router.get('<id>')
def get_one(id):
    return controller.get_one(id)

@router.post('')
def post():
    return controller.post()

@router.put('')
def put():
    return controller.put()

@router.delete('<id>')
def delete(id):
    return controller.delete(id)