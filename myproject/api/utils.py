from .serializers import AvailabilitySerializer
from myapp.models import Availability, Doctor


def generate_detailed_doctor(doctor: Doctor):

    try:
        found_doctor = Doctor.objects.get(id=doctor.id)
    except Doctor.DoesNotExist:
        return None

    availabilities = Availability.objects.filter(doctor=doctor)

    detailed_doctor = {
        "first_name": doctor.first_name,
        "last_name": doctor.last_name,
        "phone_number": doctor.phone_number,
        "hospital": {
            "name": doctor.hospital.name,
            "phone_number": doctor.hospital.phone_number,
            "address_line_1": doctor.hospital.address_line_1,
            "district": doctor.hospital.district,
            "region": doctor.hospital.region,
        },
        "category": doctor.category,
        "member_price": doctor.member_price,
        "fee": doctor.fee,
        "fee_notes": doctor.fee_notes,
        "language1": doctor.language1,
        "language2": doctor.language2,
        "availability": AvailabilitySerializer(
            availabilities,
            exclude_fields=["id", "doctor", "recurrence_pattern"],
            many=True,
        ).data,
    }

    return detailed_doctor
