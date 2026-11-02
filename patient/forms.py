from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "first_name", "last_name", "date_of_birth", "gender",
            "phone_number", "email", "address",
            "emergency_contact_name", "emergency_contact_phone",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data["date_of_birth"]
        from datetime import date
        if date_of_birth > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth
