from django.test import TestCase
from myapp.models import Hospital, Doctor, Availability
from api.serializers import (
    DoctorSerializer,
    AvailabilitySerializer,
    CreateDoctorSerializer,
)


class SerializerTestCase(TestCase):
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

    def test_create_doctor_serializer(self):
        # Correct data
        data1 = {
            "first_name": "New",
            "last_name": "Doctor",
            "phone_number": "12345678",
            "hospital": self.hospital.id,
            "category": "General Practitioner",
            "member_price": "100.00",
            "fee": "150.00",
            "fee_notes": "in clusive 3 Days of Western medicine",
            "language1": "en",
            "language2": None,
            "availability": [["Monday", "08:00:00", "16:00:00", "weekly"]],
        }

        # member_price parameter value type is incorrect
        data2 = {
            "first_name": "New",
            "last_name": "Doctor",
            "phone_number": "12345678",
            "hospital": self.hospital.id,
            "category": "General Practitioner",
            "member_price": "abc",
            "fee": "150.00",
            "fee_notes": "in clusive 3 Days of Western medicine",
            "language1": "en",
            "language2": None,
            "availability": [["Monday", "08:00:00", "16:00:00", "weekly"]],
        }

        # Non existent hospital represented by a random UUID not in the db
        data3 = {
            "first_name": "New",
            "last_name": "Doctor",
            "phone_number": "12345678",
            "hospital": "65783143-b9d7-4462-a87d-d79f262f96f1",
            "category": "General Practitioner",
            "member_price": "100.00",
            "fee": "150.00",
            "fee_notes": "in clusive 3 Days of Western medicine",
            "language1": "en",
            "language2": None,
            "availability": [["Monday", "08:00:00", "16:00:00", "weekly"]],
        }

        # Sublist in availability does not have 4 elements
        data4 = {
            "first_name": "New",
            "last_name": "Doctor",
            "phone_number": "12345678",
            "hospital": self.hospital.id,
            "category": "General Practitioner",
            "member_price": "100.00",
            "fee": "150.00",
            "fee_notes": "in clusive 3 Days of Western medicine",
            "language1": "en",
            "language2": None,
            "availability": [["Monday", "08:00:00", "16:00:00"]],
        }
        serializer1 = CreateDoctorSerializer(data=data1)
        self.assertTrue(serializer1.is_valid())

        # member_price parameter value type is incorrect
        serializer2 = CreateDoctorSerializer(data=data2)
        self.assertFalse(serializer2.is_valid())

        # Non existent hospital
        serializer3 = CreateDoctorSerializer(data=data3)
        self.assertFalse(serializer3.is_valid())

        # Sublist in availability does not have 4 elements
        serializer4 = CreateDoctorSerializer(data=data4)
        self.assertFalse(serializer4.is_valid())

    def test_doctor_serializer(self):
        data1 = {
            "first_name": "New",
            "last_name": "Doctor",
            "phone_number": "12345678",
            "hospital": self.hospital.id,
            "category": "General Practitioner",
            "member_price": "100.00",
            "fee": "150.00",
            "fee_notes": "in clusive 3 Days of Western medicine",
            "language1": "en",
            "language2": None,
        }
        data2 = {
            "first_name": "New",
            "last_name": "Doctor",
            "phone_number": "12345678",
            "hospital": self.hospital.id,
            "member_price": "120.00",
            "fee": "150.00",
            "fee_notes": "in clusive 3 Days of Western medicine",
            "language1": "en",
            "language2": None,
        }
        serializer1 = DoctorSerializer(data=data1)
        self.assertTrue(serializer1.is_valid())
        serializer2 = DoctorSerializer(data=data2)
        self.assertFalse(serializer2.is_valid())

    def test_availability_serializer(self):

        data1 = {
            "doctor": self.doctor.id,
            "day_of_week": "Monday",
            "start_time": "08:00:00",
            "end_time": "16:00:00",
            "recurrence_pattern": "weekly",
        }
        data2 = {
            "doctor": self.doctor.id,
            "day_of_week": "Monday",
            "start_time": "3029489",
            "end_time": "16:00:00",
            "recurrence_pattern": "weekly",
        }
        serializer1 = AvailabilitySerializer(data=data1)
        self.assertTrue(serializer1.is_valid())
        serializer2 = AvailabilitySerializer(data=data2)
        self.assertFalse(serializer2.is_valid())

        self.availability = Availability.objects.create(
            doctor=self.doctor,
            day_of_week="Monday",
            start_time="09:00:00",
            end_time="17:00:00",
            recurrence_pattern="weekly",
        )

        availability_data1 = AvailabilitySerializer(
            self.availability, exclude_fields=["id", "doctor", "recurrence_pattern"]
        ).data
        expected_data1 = {
            "day_of_week": "Monday",
            "start_time": "09:00:00",
            "end_time": "17:00:00",
        }
        self.assertEqual(availability_data1, expected_data1)

        availability_data2 = AvailabilitySerializer(
            self.availability, include_fields=["start_time", "end_time"]
        ).data
        expected_data2 = {
            "start_time": "09:00:00",
            "end_time": "17:00:00",
        }
        self.assertEqual(availability_data2, expected_data2)
