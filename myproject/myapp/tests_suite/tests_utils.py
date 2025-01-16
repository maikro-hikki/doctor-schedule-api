from django.test import TestCase
from myapp.models import Hospital, Doctor
from api.utils import generate_detailed_doctor


class GenerateDetailedDoctorTestCase(TestCase):

    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="Test Hospital1",
            phone_number="12345678",
            address_line_1="123 Test Street1",
            district="Test District1",
            region="Test Region1",
        )
        self.doctor = Doctor.objects.create(
            first_name="Test1",
            last_name="Doctor1",
            phone_number="87654321",
            hospital=self.hospital,
            category="General Practitioner",
            member_price=100.00,
            fee=200.00,
            fee_notes="Test Fee Notes",
            language1="en",
            language2="es",
        )

    def test_generate_detailed_doctor_correct_instance(self):
        detailed_doctor = generate_detailed_doctor(self.doctor)
        self.assertIsNotNone(detailed_doctor)
        self.assertEqual(detailed_doctor["first_name"], "Test1")
        self.assertEqual(detailed_doctor["last_name"], "Doctor1")
        self.assertEqual(detailed_doctor["phone_number"], "87654321")
        self.assertEqual(detailed_doctor["hospital"]["name"], "Test Hospital1")
        self.assertEqual(detailed_doctor["category"], "General Practitioner")
        self.assertEqual(detailed_doctor["member_price"], 100.00)
        self.assertEqual(detailed_doctor["fee"], 200.00)
        self.assertEqual(detailed_doctor["fee_notes"], "Test Fee Notes")
        self.assertEqual(detailed_doctor["language1"], "en")
        self.assertEqual(detailed_doctor["language2"], "es")
