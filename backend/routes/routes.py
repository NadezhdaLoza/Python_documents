from flask import Blueprint

from routes.positions import position_router
from routes.organizations import organization_router 
from routes.items import item_router 
from routes.damages import damage_router 
from routes.individuals import individual_router 
from routes.proxies import proxy_router 
from routes.requests import router as repair_request_router

router = Blueprint('/', __name__, url_prefix="/api/")
router.register_blueprint(position_router)
router.register_blueprint(organization_router)
router.register_blueprint(item_router)
router.register_blueprint(damage_router)
router.register_blueprint(individual_router)
router.register_blueprint(proxy_router)
router.register_blueprint(repair_request_router)