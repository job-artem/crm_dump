from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class HeightRank(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if not request.user and not request.user.is_authenticated:
            return False
        group = request.user.user_type
        return group in ['admin', 'coach', 'head_coach', 'operator']


class AdminOperator(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if not request.user and not request.user.is_authenticated:
            return False
        group = request.user.user_type
        return group in ['admin', 'operator']
