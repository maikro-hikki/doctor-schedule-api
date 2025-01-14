from django.contrib import admin
from .models import Availability, Doctor, Hospital

# Register your models here.
admin.site.register(Availability)
admin.site.register(Doctor)
admin.site.register(Hospital)
