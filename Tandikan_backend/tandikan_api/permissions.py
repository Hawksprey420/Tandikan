from rest_framework.permissions import BasePermission

ROLE_MAP = {
    'admin': {'ALL'},
    'registrar': {'ENROLLMENT', 'ERD'},
    'cashier': {'PAYMENT'},
    'faculty': {'ERD', 'CLASS'},
    'student': {'SELF', 'ENROLLMENT'},
}

class RolePermission(BasePermission):
    def has_permission(self, request, view):
        category = getattr(view, 'permission_category', None)
        role = getattr(request.user, 'role', None)
        if role is None:
            return False
        allowed = ROLE_MAP.get(role, set())
        if 'ALL' in allowed:
            return True
        if category is None:
            return False
        return category in allowed