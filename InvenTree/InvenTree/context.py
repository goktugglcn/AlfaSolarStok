# -*- coding: utf-8 -*-

"""Provides extra global data to all templates."""

<<<<<<< HEAD
import InvenTree.email
=======
>>>>>>> 331c0c7ac41e8dd6ad8241f441a49bf3aa607e5c
import InvenTree.status
from InvenTree.status_codes import (BuildStatus, PurchaseOrderStatus,
                                    ReturnOrderLineStatus, ReturnOrderStatus,
                                    SalesOrderStatus, StockHistoryCode,
                                    StockStatus)
from users.models import RuleSet, check_user_role


def health_status(request):
    """Provide system health status information to the global context.

    - Not required for AJAX requests
    - Do not provide if it is already provided to the context
    """
    if request.path.endswith('.js'):
        # Do not provide to script requests
        return {}  # pragma: no cover

    if hasattr(request, '_inventree_health_status'):
        # Do not duplicate efforts
        return {}

    request._inventree_health_status = True

    status = {
        'django_q_running': InvenTree.status.is_worker_running(),
<<<<<<< HEAD
        'email_configured': InvenTree.email.is_email_configured(),
=======
        'email_configured': InvenTree.status.is_email_configured(),
>>>>>>> 331c0c7ac41e8dd6ad8241f441a49bf3aa607e5c
    }

    # The following keys are required to denote system health
    health_keys = [
        'django_q_running',
    ]

    all_healthy = True

    for k in health_keys:
        if status[k] is not True:
            all_healthy = False

    status['system_healthy'] = all_healthy

    status['up_to_date'] = InvenTree.version.isInvenTreeUpToDate()

    return status


def status_codes(request):
    """Provide status code enumerations."""
    if hasattr(request, '_inventree_status_codes'):
        # Do not duplicate efforts
        return {}

    request._inventree_status_codes = True

    return {
        # Expose the StatusCode classes to the templates
        'ReturnOrderStatus': ReturnOrderStatus,
        'ReturnOrderLineStatus': ReturnOrderLineStatus,
        'SalesOrderStatus': SalesOrderStatus,
        'PurchaseOrderStatus': PurchaseOrderStatus,
        'BuildStatus': BuildStatus,
        'StockStatus': StockStatus,
        'StockHistoryCode': StockHistoryCode,
    }


def user_roles(request):
    """Return a map of the current roles assigned to the user.

    Roles are denoted by their simple names, and then the permission type.

    Permissions can be access as follows:

    - roles.part.view
    - roles.build.delete

    Each value will return a boolean True / False
    """
    user = request.user

    roles = {
    }

    for role in RuleSet.RULESET_MODELS.keys():

        permissions = {}

        for perm in ['view', 'add', 'change', 'delete']:
            permissions[perm] = user.is_superuser or check_user_role(user, role, perm)

        roles[role] = permissions

    return {'roles': roles}
