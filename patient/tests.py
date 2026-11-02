from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Patient


class PatientModelTests(TestCase):
    def test_patient_number_is_generated(self):
        patient = Patient.objects.create(
            first_name="Alex",
            last_name="Example",
            date_of_birth=date(1990, 1, 1),
            phone_number="0700000000",
        )
        self.assertTrue(patient.patient_number.startswith("PT-"))
        self.assertEqual(patient.full_name, "Alex Example")


class PatientViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="demo", password="StrongPass123!")
        self.client.login(username="demo", password="StrongPass123!")

    def test_patient_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("patient_list"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_for_authenticated_user(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
