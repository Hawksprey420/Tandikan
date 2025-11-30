from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    """Custom user model with role-based access"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('registrar', 'Registrar'),
        ('cashier', 'Cashier'),
        ('admin', 'Administrator'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


class Student(models.Model):
    """Student profile information"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    
    program = models.CharField(max_length=200)
    year_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"


class Subject(models.Model):
    """Course/Subject master data"""
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    units = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    year_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subjects'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.title}"


class Schedule(models.Model):
    """Class schedule for subjects"""
    DAYS_CHOICES = [
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('S', 'Saturday'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    section = models.CharField(max_length=20)
    instructor = models.CharField(max_length=200)
    academic_year = models.CharField(max_length=20)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    
    days = models.JSONField(help_text="Array of day codes: ['M', 'W', 'F']")
    time_start = models.TimeField()
    time_end = models.TimeField()
    room = models.CharField(max_length=50)
    
    max_slots = models.IntegerField(default=40)
    enrolled_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schedules'
        ordering = ['subject__code', 'section']

    def __str__(self):
        return f"{self.subject.code} - {self.section}"

    @property
    def available_slots(self):
        return self.max_slots - self.enrolled_count


class Enrollment(models.Model):
    """Student enrollment per semester"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.CharField(max_length=20)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    total_units = models.IntegerField(default=0)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_enrollments')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'enrollments'
        ordering = ['-created_at']
        unique_together = ['student', 'academic_year', 'semester']

    def __str__(self):
        return f"{self.student.student_id} - {self.academic_year} S{self.semester}"


class EnrolledSubject(models.Model):
    """Subjects enrolled in an enrollment"""
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
    ]
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='subjects')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='enrolled_students')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    grade = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    enrolled_at = models.DateTimeField(auto_now_add=True)
    dropped_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'enrolled_subjects'
        unique_together = ['enrollment', 'schedule']

    def __str__(self):
        return f"{self.enrollment.student.student_id} - {self.schedule.subject.code}"


class FeeItem(models.Model):
    """Fee items configuration"""
    CATEGORY_CHOICES = [
        ('tuition', 'Tuition Fee'),
        ('laboratory', 'Laboratory Fee'),
        ('miscellaneous', 'Miscellaneous Fee'),
        ('other', 'Other Fee'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    per_unit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fee_items'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - ₱{self.amount}"


class Assessment(models.Model):
    """Fee assessment for an enrollment"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ]
    
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='assessment')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_assessments')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_assessments')
    
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'assessments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Assessment for {self.enrollment.student.student_id}"


class AssessmentItem(models.Model):
    """Individual items in an assessment"""
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='items')
    fee_item = models.ForeignKey(FeeItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'assessment_items'

    def __str__(self):
        return f"{self.fee_item.name} - ₱{self.amount}"


class Payment(models.Model):
    """Payment records"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
    ]
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    reference_number = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_payments')
    
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment of ₱{self.amount} - {self.reference_number}"
