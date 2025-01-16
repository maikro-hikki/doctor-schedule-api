from decimal import Decimal
import uuid
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import generate_detailed_doctor
from myapp.models import Doctor
from .serializers import (
    DoctorSerializer,
    AvailabilitySerializer,
    CreateDoctorSerializer,
    HospitalSerializer,
)
from django.db.models import Q


@api_view(["GET"])
def getDoctorWithId(request, id):

    try:
        uuid_obj = uuid.UUID(id)
    except ValueError:
        res = {"error": "Invalid ID format"}
        return Response(res, status=400)

    try:
        doctor = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        res = {"error": "doctor ID does not exist"}
        return Response(res, status=400)

    complete_doctor = generate_detailed_doctor(doctor)
    if complete_doctor is None:
        res = {"error": "doctor ID does not exist"}
        return Response(res, status=400)

    return Response(complete_doctor)


@api_view(["GET"])
def getDoctorFiltered(request):

    district = request.query_params.get("district")
    category = request.query_params.get("category")
    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")
    language = request.query_params.get("language")

    filters = Q()

    if district:
        filters &= Q(hospital__district=district)

    if category:
        filters &= Q(category=category)

    if min_price:
        if max_price:
            try:
                min_price_decimal = Decimal(min_price)
                max_price_decimal = Decimal(max_price)
            except ValueError:
                res = {"error": "min_price and max_price must be decimal numbers"}
                return Response(res, status=400)

            if min_price_decimal > max_price_decimal:
                res = {"error": "min_price must be less than or equal to max_price"}
                return Response(res, status=400)

            filters &= Q(fee__range=(min_price_decimal, max_price_decimal))

    if language:
        language_filter = Q(language1__icontains=language) | Q(
            language2__icontains=language
        )
        filters &= language_filter

    doctors = Doctor.objects.filter(filters)

    complete_doctors = []
    for doctor in doctors:
        complete_doctor = generate_detailed_doctor(doctor)
        if complete_doctor is None:
            res = {"error": "doctor ID does not exist"}
            return Response(res, status=400)

        complete_doctors.append(complete_doctor)

    return Response(complete_doctors)


@api_view(["POST"])
def addDoctor(request):
    request_serializer = CreateDoctorSerializer(data=request.data)
    if request_serializer.is_valid() == False:
        return Response(request_serializer.errors, status=400)

    new_doctor = {
        "first_name": request_serializer.validated_data.get("first_name"),
        "last_name": request_serializer.validated_data.get("last_name"),
        "phone_number": request_serializer.validated_data.get("phone_number"),
        "hospital": request_serializer.validated_data.get("hospital"),
        "category": request_serializer.validated_data.get("category"),
        "member_price": request_serializer.validated_data.get("member_price"),
        "fee": request_serializer.validated_data.get("fee"),
        "fee_notes": request_serializer.validated_data.get("fee_notes"),
        "language1": request_serializer.validated_data.get("language1"),
        "language2": request_serializer.validated_data.get("language2"),
    }

    doctor_serializer = DoctorSerializer(data=new_doctor)
    if doctor_serializer.is_valid() == False:
        return Response(doctor_serializer.errors, status=400)

    saved_doctor = doctor_serializer.save()

    for time_schedule in request_serializer.validated_data.get("availability"):
        time_schedule = {
            "doctor": saved_doctor.id,
            "day_of_week": time_schedule[0],
            "start_time": time_schedule[1],
            "end_time": time_schedule[2],
            "recurrence_pattern": time_schedule[3],
        }
        availability_serializer = AvailabilitySerializer(data=time_schedule)
        if availability_serializer.is_valid() == False:
            saved_doctor.delete()
            return Response(availability_serializer.errors, status=400)
        else:
            availability_serializer.save()

    return Response(saved_doctor.id, status=201)


@api_view(["POST"])
def addHospital(request):
    serializer = HospitalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
