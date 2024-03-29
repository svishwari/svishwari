"""Purpose of this sub-folder is to store all route logic."""

from huxunify.api.route.destination import dest_bp
from huxunify.api.route.email_deliverability import email_deliverability_bp
from huxunify.api.route.trust_id import trust_id_bp
from huxunify.api.route.user import user_bp
from huxunify.api.route.decisioning import model_bp
from huxunify.api.route.orchestration import orchestration_bp
from huxunify.api.route.cdp_data_source import cdp_data_sources_bp
from huxunify.api.route.notifications import notifications_bp
from huxunify.api.route.customers import customers_bp
from huxunify.api.route.engagement import engagement_bp
from huxunify.api.route.delivery import delivery_bp
from huxunify.api.route.audiences import audience_bp
from huxunify.api.route.configurations import configurations_bp
from huxunify.api.route.applications import applications_bp
from huxunify.api.route.client_projects import client_projects_bp
from huxunify.api.route.triggers import triggers_bp


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
    audience_bp,
    configurations_bp,
    applications_bp,
    client_projects_bp,
    email_deliverability_bp,
    trust_id_bp,
    triggers_bp,
]
