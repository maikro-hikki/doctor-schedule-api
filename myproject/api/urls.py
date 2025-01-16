from django.urls import path
from . import views

urlpatterns = [
    path("add-doctor", views.addDoctor, name="add_doctor"),
    path("doctor/<str:id>", views.getDoctorWithId, name="get_doctor_with_id"),
    path("doctor", views.getDoctorFiltered, name="doctor"),
]


# path("hospital-list", views.getHospitalList, name="hospital_list"),
# path("add-hospital", views.addHospital, name="add_hospital"),
# path("hospital/<str:id>", views.getHospital, name="get_hospital"),
