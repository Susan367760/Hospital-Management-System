from django.contrib import admin
from django.urls import include, path
from patient import views as patient_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", patient_views.dashboard, name="dashboard"),
    path("accounts/register/", patient_views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("patients/", include("patient.urls")),
]
