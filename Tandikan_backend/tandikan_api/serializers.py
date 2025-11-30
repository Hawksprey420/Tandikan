from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    User, Student, Subject, Schedule, Enrollment, 
    EnrolledSubject, FeeItem, Assessment, AssessmentItem, Payment
)
from .erd_models import (
    StudentInfo, Faculty, College, Programs, ClassSubjects,
    ClassOfferings, Schedule as ERDSchedule, StudentSubjects, Rooms
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name', 'role']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'student')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_email', 'student_id', 'first_name', 'last_name', 
            'middle_name', 'date_of_birth', 'address', 'phone', 'email', 
            'program', 'year_level', 'status', 'enrolled_at', 'updated_at'
        ]
        read_only_fields = ['id', 'enrolled_at', 'updated_at']


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model"""
    prerequisites_list = serializers.StringRelatedField(source='prerequisites', many=True, read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id', 'code', 'title', 'description', 'units', 
            'year_level', 'semester', 'prerequisites', 'prerequisites_list',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScheduleSerializer(serializers.ModelSerializer):
    """Serializer for Schedule model"""
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_title = serializers.CharField(source='subject.title', read_only=True)
    subject_units = serializers.IntegerField(source='subject.units', read_only=True)
    available_slots = serializers.ReadOnlyField()

    class Meta:
        model = Schedule
        fields = [
            'id', 'subject', 'subject_code', 'subject_title', 'subject_units',
            'section', 'instructor', 'academic_year', 'semester',
            'days', 'time_start', 'time_end', 'room',
            'max_slots', 'enrolled_count', 'available_slots',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'enrolled_count', 'created_at', 'updated_at']


class EnrolledSubjectSerializer(serializers.ModelSerializer):
    """Serializer for EnrolledSubject model"""
    schedule = ScheduleSerializer(read_only=True)
    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(), 
        source='schedule', 
        write_only=True
    )

    class Meta:
        model = EnrolledSubject
        fields = [
            'id', 'enrollment', 'schedule', 'schedule_id', 
            'status', 'grade', 'enrolled_at', 'dropped_at'
        ]
        read_only_fields = ['id', 'enrolled_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model"""
    subjects = EnrolledSubjectSerializer(many=True, read_only=True)
    schedule_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    student_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'academic_year', 'semester',
            'status', 'total_units', 'approved_by', 'approved_by_name',
            'approved_at', 'rejection_reason', 'subjects', 'schedule_ids',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_units', 'approved_at', 'created_at', 'updated_at']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def get_approved_by_name(self, obj):
        if obj.approved_by:
            return f"{obj.approved_by.first_name} {obj.approved_by.last_name}"
        return None

    def create(self, validated_data):
        schedule_ids = validated_data.pop('schedule_ids', [])
        enrollment = Enrollment.objects.create(**validated_data)
        
        total_units = 0
        for schedule_id in schedule_ids:
            try:
                schedule = Schedule.objects.get(id=schedule_id)
                EnrolledSubject.objects.create(
                    enrollment=enrollment,
                    schedule=schedule
                )
                total_units += schedule.subject.units
                schedule.enrolled_count += 1
                schedule.save()
            except Schedule.DoesNotExist:
                pass
        
        enrollment.total_units = total_units
        enrollment.save()
        return enrollment


class FeeItemSerializer(serializers.ModelSerializer):
    """Serializer for FeeItem model"""
    class Meta:
        model = FeeItem
        fields = [
            'id', 'name', 'description', 'category', 'amount', 
            'per_unit', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssessmentItemSerializer(serializers.ModelSerializer):
    """Serializer for AssessmentItem model"""
    fee_name = serializers.CharField(source='fee_item.name', read_only=True)
    fee_category = serializers.CharField(source='fee_item.category', read_only=True)

    class Meta:
        model = AssessmentItem
        fields = ['id', 'assessment', 'fee_item', 'fee_name', 'fee_category', 'quantity', 'amount']
        read_only_fields = ['id']


class AssessmentSerializer(serializers.ModelSerializer):
    """Serializer for Assessment model"""
    items = AssessmentItemSerializer(many=True, read_only=True)
    student_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = [
            'id', 'enrollment', 'student_name', 'total_amount', 
            'discount_amount', 'net_amount', 'status', 
            'created_by', 'created_by_name', 'approved_by', 
            'items', 'created_at', 'approved_at'
        ]
        read_only_fields = ['id', 'created_at', 'approved_at']

    def get_student_name(self, obj):
        return f"{obj.enrollment.student.first_name} {obj.enrollment.student.last_name}"

    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}"
        return None


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    student_name = serializers.SerializerMethodField()
    received_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'assessment', 'student_name', 'amount', 
            'payment_method', 'reference_number', 'status',
            'received_by', 'received_by_name', 'created_at', 'confirmed_at'
        ]
        read_only_fields = ['id', 'created_at', 'confirmed_at']

    def get_student_name(self, obj):
        return f"{obj.assessment.enrollment.student.first_name} {obj.assessment.enrollment.student.last_name}"

    def get_received_by_name(self, obj):
        if obj.received_by:
            return f"{obj.received_by.first_name} {obj.received_by.last_name}"
        return None


# --- ERD SERIALIZERS (Skeleton placeholders) ---

class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = ['id', 'student_id']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id']


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id']


class ProgramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = ['id']


class ClassSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSubjects
        fields = ['id']


class ClassOfferingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassOfferings
        fields = ['id']


class ERDScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ERDSchedule
        fields = ['id']


class StudentSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjects
        fields = ['id']


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['id']
