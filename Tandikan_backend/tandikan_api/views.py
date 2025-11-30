from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    User, Student, Subject, Schedule, Enrollment, 
    EnrolledSubject, FeeItem, Assessment, AssessmentItem, Payment
)
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    StudentSerializer, SubjectSerializer, ScheduleSerializer,
    EnrollmentSerializer, EnrolledSubjectSerializer,
    FeeItemSerializer, AssessmentSerializer, AssessmentItemSerializer, PaymentSerializer
)


def index(request):
    return JsonResponse({"status": "Tandikan API is running"})


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login user"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': str(refresh.access_token),
            'refresh': str(refresh)
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user"""
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Get current user info"""
    return Response(UserSerializer(request.user).data)


# Student ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student CRUD operations"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.all()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current student profile"""
        try:
            student = Student.objects.get(user=request.user)
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# Subject ViewSet
class SubjectViewSet(viewsets.ModelViewSet):
    """ViewSet for Subject CRUD operations"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Subject.objects.all()
        year_level = self.request.query_params.get('year_level')
        semester = self.request.query_params.get('semester')
        
        if year_level:
            queryset = queryset.filter(year_level=year_level)
        if semester:
            queryset = queryset.filter(semester=semester)
        
        return queryset


# Schedule ViewSet
class ScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for Schedule CRUD operations"""
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Schedule.objects.select_related('subject').all()
        year_level = self.request.query_params.get('year_level')
        semester = self.request.query_params.get('semester')
        academic_year = self.request.query_params.get('academic_year')
        
        if year_level:
            queryset = queryset.filter(subject__year_level=year_level)
        if semester:
            queryset = queryset.filter(semester=semester)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get schedules with available slots"""
        queryset = self.get_queryset().filter(enrolled_count__lt=models.F('max_slots'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Enrollment ViewSet
class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment CRUD operations"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            try:
                student = Student.objects.get(user=user)
                return Enrollment.objects.filter(student=student)
            except Student.DoesNotExist:
                return Enrollment.objects.none()
        return Enrollment.objects.select_related('student').all()

    def perform_create(self, serializer):
        if self.request.user.role == 'student':
            student = Student.objects.get(user=self.request.user)
            serializer.save(student=student)
        else:
            serializer.save()

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current enrollment"""
        try:
            student = Student.objects.get(user=request.user)
            enrollment = Enrollment.objects.filter(
                student=student,
                status__in=['pending', 'approved']
            ).first()
            
            if enrollment:
                serializer = self.get_serializer(enrollment)
                return Response(serializer.data)
            
            return Response(
                {'error': 'No active enrollment found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve an enrollment"""
        if request.user.role != 'registrar':
            return Response(
                {'error': 'Only registrars can approve enrollments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        enrollment = self.get_object()
        enrollment.status = 'approved'
        enrollment.approved_by = request.user
        enrollment.approved_at = timezone.now()
        enrollment.save()
        
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject an enrollment"""
        if request.user.role != 'registrar':
            return Response(
                {'error': 'Only registrars can reject enrollments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        enrollment = self.get_object()
        enrollment.status = 'rejected'
        enrollment.rejection_reason = request.data.get('reason', '')
        enrollment.save()
        
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='subjects/(?P<subject_id>[^/.]+)')
    def drop_subject(self, request, pk=None, subject_id=None):
        """Drop a subject from enrollment"""
        enrollment = self.get_object()
        
        try:
            enrolled_subject = EnrolledSubject.objects.get(
                enrollment=enrollment,
                id=subject_id
            )
            enrolled_subject.status = 'dropped'
            enrolled_subject.dropped_at = timezone.now()
            enrolled_subject.save()
            
            # Update schedule count
            schedule = enrolled_subject.schedule
            schedule.enrolled_count = max(0, schedule.enrolled_count - 1)
            schedule.save()
            
            # Update total units
            enrollment.total_units -= schedule.subject.units
            enrollment.save()
            
            return Response({'message': 'Subject dropped successfully'})
        except EnrolledSubject.DoesNotExist:
            return Response(
                {'error': 'Enrolled subject not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# Assessment ViewSet
class AssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Assessment CRUD operations"""
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            try:
                student = Student.objects.get(user=user)
                return Assessment.objects.filter(enrollment__student=student)
            except Student.DoesNotExist:
                return Assessment.objects.none()
        return Assessment.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve an assessment"""
        if request.user.role not in ['registrar', 'cashier']:
            return Response(
                {'error': 'Only registrars or cashiers can approve assessments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        assessment = self.get_object()
        assessment.status = 'approved'
        assessment.approved_by = request.user
        assessment.approved_at = timezone.now()
        assessment.save()
        
        serializer = self.get_serializer(assessment)
        return Response(serializer.data)


# Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment CRUD operations"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Payment.objects.select_related('assessment__enrollment__student').all()
        assessment_id = self.request.query_params.get('assessment')
        
        if assessment_id:
            queryset = queryset.filter(assessment_id=assessment_id)
        
        user = self.request.user
        if user.role == 'student':
            try:
                student = Student.objects.get(user=user)
                queryset = queryset.filter(assessment__enrollment__student=student)
            except Student.DoesNotExist:
                return Payment.objects.none()
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(received_by=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a payment"""
        if request.user.role != 'cashier':
            return Response(
                {'error': 'Only cashiers can confirm payments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        payment = self.get_object()
        payment.status = 'confirmed'
        payment.confirmed_at = timezone.now()
        payment.save()
        
        # Check if assessment is fully paid
        assessment = payment.assessment
        total_paid = sum(p.amount for p in assessment.payments.filter(status='confirmed'))
        if total_paid >= assessment.net_amount:
            assessment.status = 'paid'
            assessment.save()
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)


# Fee Item ViewSet
class FeeItemViewSet(viewsets.ModelViewSet):
    """ViewSet for FeeItem CRUD operations"""
    queryset = FeeItem.objects.filter(is_active=True)
    serializer_class = FeeItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FeeItem.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset

