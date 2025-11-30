from django.db import models

"""Skeleton models mapped to existing ERD tables.
Fields must be replaced with exact database column definitions.
managed = False prevents Django from altering existing tables.
"""


class StudentInfo(models.Model):
    student_id = models.CharField(max_length=32, unique=True)
    class Meta:
        db_table = 'student_info'
        managed = False


class Faculty(models.Model):
    class Meta:
        db_table = 'faculty'
        managed = False


class College(models.Model):
    class Meta:
        db_table = 'college'
        managed = False


class Programs(models.Model):
    class Meta:
        db_table = 'programs'
        managed = False


class ClassSubjects(models.Model):
    class Meta:
        db_table = 'class_subjects'
        managed = False


class ClassOfferings(models.Model):
    class Meta:
        db_table = 'class_offerings'
        managed = False


class Schedule(models.Model):  # ERD schedule (distinct from existing Schedule model)
    class Meta:
        db_table = 'schedule'
        managed = False


class StudentSubjects(models.Model):
    class Meta:
        db_table = 'student_subjects'
        managed = False


class Rooms(models.Model):
    class Meta:
        db_table = 'rooms'
        managed = False
