from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PatientForm
from .models import Patient


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    context = {
        "total_patients": Patient.objects.count(),
        "recent_patients": Patient.objects.all()[:5],
    }
    return render(request, "patient/dashboard.html", context)


@login_required
def patient_list(request):
    query = request.GET.get("q", "").strip()
    patients = Patient.objects.all()
    if query:
        patients = patients.filter(
            Q(patient_number__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(email__icontains=query)
        )
    return render(request, "patient/patient_list.html", {"patients": patients, "query": query})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "patient/patient_detail.html", {"patient": patient})


@login_required
def patient_create(request):
    form = PatientForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        patient = form.save()
        messages.success(request, f"{patient.full_name} was registered successfully.")
        return redirect("patient_detail", pk=patient.pk)
    return render(request, "patient/patient_form.html", {"form": form, "page_title": "Register patient"})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, instance=patient)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Patient details updated.")
        return redirect("patient_detail", pk=patient.pk)
    return render(request, "patient/patient_form.html", {
        "form": form, "page_title": "Update patient", "patient": patient
    })


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        name = patient.full_name
        patient.delete()
        messages.success(request, f"{name}'s demo record was deleted.")
        return redirect("patient_list")
    return render(request, "patient/patient_confirm_delete.html", {"patient": patient})
