import uuid
from django.db import models
from django.urls import reverse


class Patient(models.Model):
    class Gender(models.TextChoices):
        FEMALE = "F", "Female"
        MALE = "M", "Male"
        OTHER = "O", "Other"
        NOT_STATED = "N", "Prefer not to say"

    patient_number = models.CharField(max_length=12, unique=True, editable=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.NOT_STATED)
    phone_number = models.CharField(max_length=25)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=120, blank=True)
    emergency_contact_phone = models.CharField(max_length=25, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "patient"
        verbose_name_plural = "patients"

    def save(self, *args, **kwargs):
        if not self.patient_number:
            self.patient_number = f"PT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.patient_number} — {self.full_name}"

    def get_absolute_url(self):
        return reverse("patient_detail", kwargs={"pk": self.pk})
