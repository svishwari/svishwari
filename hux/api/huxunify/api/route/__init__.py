"""
Purpose of this sub-folder is to store all route logic.
"""
from huxunify.api.route.destination import dest_bp
from huxunify.api.route.metrics import metrics_bp
from huxunify.api.route.user import user_bp
from huxunify.api.route.decisioning import model_bp
from huxunify.api.route.orchestration import orchestration_bp
from huxunify.api.route.cdp_data_source import cdp_data_sources_bp
from huxunify.api.route.notifications import notifications_bp
from huxunify.api.route.customers import customers_bp
from huxunify.api.route.engagement import engagement_bp
from huxunify.api.route.delivery import delivery_bp

ROUTES = [
    dest_bp,
    user_bp,
    model_bp,
    orchestration_bp,
    cdp_data_sources_bp,
    notifications_bp,
    customers_bp,
    engagement_bp,
    delivery_bp,
    metrics_bp
]
