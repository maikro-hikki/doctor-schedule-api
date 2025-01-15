import uuid
from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapp.models import Hospital, Doctor, Availability
from .serializers import (
    HospitalSerializer,
    DoctorSerializer,
    AvailabilitySerializer,
    CreateDoctorSerializer,
)
from django.db.models import Q


@api_view(["GET"])
def getDoctor(request, id):

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

    availabilities = Availability.objects.filter(doctor=doctor)

    complete_doctor_info = {
        "id": doctor.id,
        "first_name": doctor.first_name,
        "last_name": doctor.last_name,
        "phone_number": doctor.phone_number,
        "hospital": HospitalSerializer(doctor.hospital).data,
        "category": doctor.category,
        "member_price": doctor.member_price,
        "fee": doctor.fee,
        "fee_notes": doctor.fee_notes,
        "language1": doctor.language1,
        "language2": doctor.language2,
        "availability": AvailabilitySerializer(availabilities, many=True).data,
    }

    # serializer = DoctorSerializer(doctor)
    # return Response(serializer.data)
    return Response(complete_doctor_info)


@api_view(["GET"])
def getDoctorFiltered(request):

    district = request.query_params.get("district")
    category = request.query_params.get("category")
    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")
    language = request.query_params.get("language")

    doctors = Doctor.objects.select_related("hospital")

    if district:
        doctors = doctors.filter(hospital__district__icontains=district)

    if category:
        doctors = doctors.filter(category__icontains=category)

    if min_price:
        if max_price:
            if min_price > max_price:
                res = {"error": "min_price must be less than or equal to max_price"}
                return Response(res, status=400)

            doctors = doctors.filter(fee__gte=min_price, fee__lte=max_price)

    if language:
        doctors = doctors.filter(
            Q(language1__icontains=language) | Q(language2__icontains=language)
        )

    serializer = DoctorSerializer(doctors, many=True)

    return Response(serializer.data)


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


# @api_view(["GET"])
# def getHospitalList(request):
#     hospitals = Hospital.objects.all()
#     serializer = HospitalSerializer(hospitals, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def getHospital(request, id):

#     try:
#         uuid_obj = uuid.UUID(id)
#     except ValueError:
#         res = {"error": "Invalid ID format"}
#         return Response(res, status=400)

#     try:
#         hospital = Hospital.objects.get(id=id)
#     except Hospital.DoesNotExist:
#         res = {"error": "hospital ID does not exist"}
#         return Response(res, status=400)

#     serializer = HospitalSerializer(hospital)
#     return Response(serializer.data)


# @api_view(["POST"])
# def addHospital(request):
#     serializer = HospitalSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
