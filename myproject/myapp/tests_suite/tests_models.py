from django.test import TestCase
from ..models import Hospital, Doctor, Availability


class HospitalModelTestCase(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            phone_number="12345678",
            address_line_1="123 Test Street",
            district="Test District",
            region="Test Region",
        )

    def test_hospital_creation(self):
        self.assertEqual(self.hospital.name, "Test Hospital")
        self.assertEqual(self.hospital.phone_number, "12345678")
        self.assertEqual(self.hospital.address_line_1, "123 Test Street")
        self.assertEqual(self.hospital.district, "Test District")
        self.assertEqual(self.hospital.region, "Test Region")


class DoctorModelTestCase(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            phone_number="12345678",
            address_line_1="123 Test Street",
            district="Test District",
            region="Test Region",
        )
        self.doctor = Doctor.objects.create(
            first_name="Test",
            last_name="Doctor",
            phone_number="87654321",
            hospital=self.hospital,
            category="Test Category",
            fee=100.00,
            language1="en",
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.first_name, "Test")
        self.assertEqual(self.doctor.last_name, "Doctor")
        self.assertEqual(self.doctor.phone_number, "87654321")
        self.assertEqual(self.doctor.hospital, self.hospital)
        self.assertEqual(self.doctor.category, "Test Category")
        self.assertEqual(self.doctor.fee, 100.00)
        self.assertEqual(self.doctor.language1, "en")


class AvailabilityModelTestCase(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            phone_number="12345678",
            address_line_1="123 Test Street",
            district="Test District",
            region="Test Region",
        )
        self.doctor = Doctor.objects.create(
            first_name="Test",
            last_name="Doctor",
            phone_number="87654321",
            hospital=self.hospital,
            category="Test Category",
            fee=100.00,
            language1="en",
        )
        self.availability = Availability.objects.create(
            doctor=self.doctor,
            day_of_week="Monday",
            start_time="09:00:00",
            end_time="17:00:00",
        )

    def test_availability_creation(self):
        self.assertEqual(self.availability.doctor, self.doctor)
        self.assertEqual(self.availability.day_of_week, "Monday")
        self.assertEqual(self.availability.start_time, "09:00:00")
        self.assertEqual(self.availability.end_time, "17:00:00")
        self.assertEqual(self.availability.recurrence_pattern, "weekly")
