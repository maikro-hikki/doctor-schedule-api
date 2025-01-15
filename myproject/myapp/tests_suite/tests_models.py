from django.test import TestCase

from ..models import Hospital, Doctor, Availability
from django.utils import timezone


class HospitalModelTestCase(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="Test hospital",
            phone_number="12345678",
            address_line_1="Test address",
            district="Test district",
            region="Test region",
        )

    def test_hospital_creation(self):
        self.assertEqual(self.hospital.name, "Test hospital")
        self.assertEqual(self.hospital.phone_number, "12345678")
        self.assertEqual(self.hospital.address_line_1, "Test address")
        self.assertEqual(self.hospital.district, "Test district")
        self.assertEqual(self.hospital.region, "Test region")


class DoctorModelTestCase(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="Test hospital",
            phone_number="12345678",
            address_line_1="Test address",
            district="Test district",
            region="Test region",
        )
        self.doctor = Doctor.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="87654321",
            hospital=self.hospital,
            category="Test category",
            member_price=100.50,
            fee=200.75,
            fee_notes="Test fee notes",
            language1="en",
            language2="es",
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.first_name, "John")
        self.assertEqual(self.doctor.last_name, "Doe")
        self.assertEqual(self.doctor.phone_number, "87654321")
        self.assertEqual(self.doctor.hospital, self.hospital)
        self.assertEqual(self.doctor.category, "Test category")
        self.assertEqual(self.doctor.member_price, 100.50)
        self.assertEqual(self.doctor.fee, 200.75)
        self.assertEqual(self.doctor.fee_notes, "Test fee notes")
        self.assertEqual(self.doctor.language1, "en")
        self.assertEqual(self.doctor.language2, "es")


class AvailabilityModelTestCase(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="Test hospital",
            phone_number="12345678",
            address_line_1="Test address",
            district="Test district",
            region="Test region",
        )
        self.doctor = Doctor.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="87654321",
            hospital=self.hospital,
            category="Test category",
            member_price=100.50,
            fee=200.75,
            fee_notes="Test fee notes",
            language1="en",
            language2="es",
        )
        self.availability = Availability.objects.create(
            doctor=self.doctor,
            day_of_week="Monday",
            start_time=timezone.now().time(),
            end_time=timezone.now().time(),
            recurrence_pattern="weekly",
        )

    def test_availability_creation(self):
        self.assertEqual(self.availability.doctor, self.doctor)
        self.assertEqual(self.availability.day_of_week, "Monday")
        self.assertEqual(self.availability.recurrence_pattern, "weekly")
