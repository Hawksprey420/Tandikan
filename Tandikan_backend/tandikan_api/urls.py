from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    index, register_view, login_view, logout_view, current_user_view,
    StudentViewSet, SubjectViewSet, ScheduleViewSet, EnrollmentViewSet,
    AssessmentViewSet, PaymentViewSet, FeeItemViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'fee-items', FeeItemViewSet, basename='feeitem')

urlpatterns = [
    # Root endpoint
    path('', index, name='index'),
    
    # Authentication endpoints
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/me/', current_user_view, name='current-user'),
    
    # Include router URLs
    path('', include(router.urls)),
]