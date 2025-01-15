from enum import Enum
from django.db import models
import uuid


# class Category(Enum):
#     CARDIOLOGIST = "cardiologist"
#     DERMATOLOGIST = "dermatologist"
#     NEUROLOGIST = "neurologist"
#     GENERAL_PRACTITIONER = "general_practitioner"


# class Languages(Enum):
#     ENGLISH = "en"
#     FRENCH = "fr"
#     SPANISH = "es"
#     GERMAN = "de"
#     CHINESE = "zh"


class Hospital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=8, null=True)
    address_line_1 = models.TextField()
    district = models.CharField(max_length=50)
    region = models.CharField(max_length=50)


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=8)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=100)
    member_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    fee_notes = models.TextField(null=True)
    # utilize ISO 639-1 two-letter language codes to represent language
    language1 = models.CharField(max_length=2)
    language2 = models.CharField(max_length=2, null=True)


class Availability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    recurrence_pattern = models.CharField(max_length=20, default="weekly")
