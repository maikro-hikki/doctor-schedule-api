from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from ..models import Hospital, Doctor, Availability

# from api.serializers import (
#     HospitalSerializer,
#     DoctorSerializer,
#     AvailabilitySerializer,
#     CreateDoctorSerializer,
# )


class DoctorAPITestCase(APITestCase):
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

    def test_get_doctor(self):
        url = reverse("get_doctor", args=[str(self.doctor.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_doctor_filtered(self):
        url = reverse("doctor")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_doctor(self):
        url = reverse("add_hospital")
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "phone_number": "98765432",
            "hospital": self.hospital.id,
            "category": "General Practitioner",
            "member_price": 150.25,
            "fee": 250.75,
            "fee_notes": "Some fee notes",
            "language1": "fr",
            "language2": "de",
            "availability": [
                ["Tuesday", "09:00:00", "17:00:00", "weekly"],
                ["Thursday", "10:00:00", "16:00:00", "bi-weekly"],
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
