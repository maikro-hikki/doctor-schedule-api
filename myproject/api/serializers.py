from rest_framework import serializers
from myapp.models import Doctor, Hospital, Availability


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = "__all__"


class CreateDoctorSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=8)
    hospital = serializers.UUIDField(allow_null=True)
    category = serializers.CharField(max_length=100)
    member_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True
    )
    fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    fee_notes = serializers.CharField(allow_null=True)
    language1 = serializers.CharField()
    language2 = serializers.CharField(allow_null=True)
    availability = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()), allow_null=True
    )

    def validate_hospital(self, value):
        if value is not None:
            try:
                hospital_object = Hospital.objects.get(id=value)
            except Hospital.DoesNotExist:
                raise serializers.ValidationError("Hospital ID does not exist")
        return value

    def validate_availability(self, value):
        # Check the size of each nested list
        for sublist in value:
            if len(sublist) != 4:
                raise serializers.ValidationError(
                    "Each sublist in availability must contain exactly 3 elements"
                )

        return value


class PriceRangeSerializer(serializers.Serializer):
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)


# class DoctorFilteredSerializer(serializers.Serializer):
#     district = serializers.CharField(required=False)
#     category = serializers.CharField(required=False)
#     price = PriceRangeSerializer(required=False)
#     language = serializers.CharField(required=False)
