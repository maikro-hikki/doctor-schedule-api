from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from myapp.models import Hospital, Doctor, Availability


class DoctorViewTestCase(APITestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="Test Hospital1",
            phone_number="12345678",
            address_line_1="123 Test Street1",
            district="Test District1",
            region="Test Region1",
        )
        self.hospital2 = Hospital.objects.create(
            name="Test Hospital2",
            phone_number="78901234",
            address_line_1="123 Test Street2",
            district="Test District2",
            region="Test Region2",
        )
        self.doctor = Doctor.objects.create(
            first_name="Test1",
            last_name="Doctor1",
            phone_number="87654321",
            hospital=self.hospital,
            category="General Practitioner",
            fee=100.00,
            language1="en",
        )
        self.doctor2 = Doctor.objects.create(
            first_name="Test2",
            last_name="Doctor2",
            phone_number="10293847",
            hospital=self.hospital,
            category="Cardiology",
            fee=200.00,
            language1="en",
            language2="zn",
        )
        self.doctor3 = Doctor.objects.create(
            first_name="Test3",
            last_name="Doctor3",
            phone_number="12345678",
            hospital=self.hospital2,
            category="General Practitioner",
            fee=300.00,
            language1="en",
            language2="de",
        )
        self.availability = Availability.objects.create(
            doctor=self.doctor,
            day_of_week="Monday",
            start_time="09:00:00",
            end_time="17:00:00",
            recurrence_pattern="weekly",
        )

    def test_get_doctor_with_id(self):
        url = reverse("get_doctor_with_id", args=[self.doctor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["first_name"], "Test1")
        self.assertEqual(response.data["last_name"], "Doctor1")
        self.assertEqual(response.data["hospital"]["name"], "Test Hospital1")

    def test_get_doctor_filtered(self):
        url = reverse("doctor")
        response = self.client.get(
            url, {"district": "Test District1", "category": "Cardiology"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_add_doctor(self):
        url = reverse("add_doctor")
        data1 = {
            "first_name": "New",
            "last_name": "Doctor",
            "phone_number": "12345678",
            "hospital": self.hospital.id,
            "category": "New Category",
            "member_price": "123.00",
            "fee": "150.00",
            "fee_notes": "Not inclusive Western medicine",
            "language1": "zh",
            "language2": "en",
            "availability": [["Monday", "08:00:00", "16:00:00", "weekly"]],
        }
        data2 = {
            "first_name": "New",
            "last_name": "Doctor",
            "phone_number": "12345678",
            "category": "New Category",
            "member_price": "123.00",
            "fee": "150.00",
            "fee_notes": "Not inclusive Western medicine",
            "language1": "zh",
            "language2": "en",
            "availability": [["Monday", "08:00:00", "16:00:00", "weekly"]],
        }
        response1 = self.client.post(url, data1, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(url, data2, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        availabilities = Availability.objects.all()
        new_doctor = Doctor.objects.get(id=response1.data)
        all_doctor = Doctor.objects.all()

        self.assertEqual(all_doctor.count(), 4)
        self.assertEqual(availabilities.count(), 2)
        self.assertEqual(new_doctor.first_name, "New")
        self.assertEqual(new_doctor.hospital, self.hospital)
