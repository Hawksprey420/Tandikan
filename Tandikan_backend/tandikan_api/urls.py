from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    index, register_view, login_view, logout_view, current_user_view,
    StudentViewSet, SubjectViewSet, ScheduleViewSet, EnrollmentViewSet,
    AssessmentViewSet, PaymentViewSet, FeeItemViewSet,
    StudentInfoViewSet, FacultyViewSet, CollegeViewSet, ProgramsViewSet,
    ClassSubjectsViewSet, ClassOfferingsViewSet, ERDScheduleViewSet,
    StudentSubjectsViewSet, RoomsViewSet,
    tuition_assessment_view, payment_post_view
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
router.register(r'erd/student-info', StudentInfoViewSet, basename='student-info')
router.register(r'erd/faculty', FacultyViewSet, basename='faculty')
router.register(r'erd/college', CollegeViewSet, basename='college')
router.register(r'erd/programs', ProgramsViewSet, basename='programs')
router.register(r'erd/class-subjects', ClassSubjectsViewSet, basename='class-subjects')
router.register(r'erd/class-offerings', ClassOfferingsViewSet, basename='class-offerings')
router.register(r'erd/schedule', ERDScheduleViewSet, basename='erd-schedule')
router.register(r'erd/student-subjects', StudentSubjectsViewSet, basename='student-subjects')
router.register(r'erd/rooms', RoomsViewSet, basename='rooms')

urlpatterns = [
    # Root endpoint
    path('', index, name='index'),
    
    # Authentication endpoints
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/me/', current_user_view, name='current-user'),

    # Enrollment flow stubs
    path('enrollment/tuition-assessment/', tuition_assessment_view, name='tuition-assessment'),
    path('enrollment/payment-post/', payment_post_view, name='payment-post'),
    
    # Include router URLs
    path('', include(router.urls)),
]