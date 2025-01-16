from rest_framework import serializers
from myapp.models import Doctor, Hospital, Availability


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        include_fields = kwargs.pop("include_fields", None)
        exclude_fields = kwargs.pop("exclude_fields", None)

        super(AvailabilitySerializer, self).__init__(*args, **kwargs)

        if include_fields is not None:
            allowed = set(include_fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name)


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

    # Also checks if the hospital ID is reistered in the database
    def validate_hospital(self, value):
        if value is not None:
            try:
                hospital_object = Hospital.objects.get(id=value)
            except Hospital.DoesNotExist:
                raise serializers.ValidationError("Hospital ID does not exist")
        return value

    # The sublists in availability must have 4 items
    def validate_availability(self, value):
        for sublist in value:
            if len(sublist) != 4:
                raise serializers.ValidationError(
                    "Each sublist in availability must contain exactly 3 elements"
                )

        return value


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
