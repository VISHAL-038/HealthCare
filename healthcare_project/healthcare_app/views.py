from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, DoctorProfileForm, PatientProfileForm, SymptomForm, AppointmentForm, PrescriptionForm, PatientReportForm, PatientHistoryForm, TestimonialForm, LabTestForm
from .models import User, DoctorProfile, PatientProfile, PredictionHistory, Appointment, Prescription, PatientReport, PatientHistory, Medicine, Testimonial, Order, AvailableLabTest, LabTest
import requests
import os
import pandas as pd
from django.conf import settings 
from .serializers import MedicineSerializer
from rest_framework import generics

# ✅ Flask API URL for ML Predictions
FLASK_API_URL = "http://127.0.0.1:5000/predict"

# ✅ Path to the CSV file
CSV_FILE_PATH = os.path.join(settings.BASE_DIR, 'healthcare_app', 'static', 'data', 'disease_data.csv')

# Home Page View
def home(request):
    doctors = DoctorProfile.objects.select_related('user').all()
    testimonials = Testimonial.objects.all().order_by('-created_at')[:5]  # Fetch latest 5 testimonials

    return render(request, "healthcare_app/home.html", {
        "doctors": doctors,
        "testimonials": testimonials
    })



# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')

            if user_type == 'doctor':
                # Providing default values for required fields
                DoctorProfile.objects.create(user=user, specialization="General", experience=0, contact_number="N/A")
                login(request, user)
                return redirect('doctor_dashboard')

            else:
                PatientProfile.objects.create(user=user, age=0, gender="Not Specified", contact_number="N/A")
                login(request, user)
                return redirect('patient_dashboard')

    else:
        form = UserRegisterForm()
    return render(request, 'healthcare_app/register.html', {'form': form})


# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'healthcare_app/login.html')

# User Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# Dashboard View (Redirects based on User Type)
@login_required
def dashboard(request):
    if request.user.user_type == 'doctor':
        return redirect('doctor_dashboard')
    return redirect('patient_dashboard')

# Doctor Dashboard View
@login_required
def doctor_dashboard(request):
    return render(request, 'healthcare_app/doctor_dashboard.html')

# Patient Dashboard View
@login_required
def patient_dashboard(request):
    return render(request, 'healthcare_app/patient_dashboard.html')

@login_required
def disease_prediction(request):
    prediction_result = None
    disease_details = None  # Store disease details here

    if request.method == "POST":
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data["symptoms"]

            try:
                response = requests.post(FLASK_API_URL, json={"symptoms": symptoms})

                if response.status_code == 200:
                    prediction_result = response.json()
                    predicted_disease = prediction_result.get("final_prediction")

                    # ✅ Get additional disease details
                    disease_details = get_disease_details(predicted_disease)

                    # ✅ Save Prediction History
                    PredictionHistory.objects.create(
                        user=request.user,
                        symptoms=symptoms,
                        predicted_disease=predicted_disease
                    )

                else:
                    prediction_result = {"error": "Failed to fetch prediction from API"}

            except requests.exceptions.RequestException as e:
                prediction_result = {"error": f"API request failed: {e}"}

    else:
        form = SymptomForm()

    return render(request, "healthcare_app/disease_prediction.html", {
        "form": form,
        "prediction": prediction_result,
        "disease_details": disease_details  # ✅ Pass disease details to template
    })

def get_disease_details(predicted_disease):
    """Retrieve disease description, tests, and medications from CSV"""
    try:
        df = pd.read_csv(CSV_FILE_PATH)

        # Normalize disease names
        df["Disease"] = df["Prognosis"].str.strip().str.lower()
        predicted_disease = predicted_disease.strip().lower()

        # Find the disease
        disease_info = df[df["Disease"] == predicted_disease]

        if not disease_info.empty:
            return {
                "description": disease_info.iloc[0]["Description"],
                "tests": disease_info.iloc[0]["Medical Test"],
                "medications": disease_info.iloc[0]["Medications"]
            }
        else:
            return {"description": "No details available.", "tests": "N/A", "medications": "N/A"}

    except FileNotFoundError:
        return {"description": "CSV file not found.", "tests": "N/A", "medications": "N/A"}
    except Exception as e:
        return {"description": f"Error fetching data: {e}", "tests": "N/A", "medications": "N/A"}


# Prediction history
@login_required
def prediction_history(request):
    history = PredictionHistory.objects.filter(user=request.user).order_by("-prediction_date")
    return render(request, "healthcare_app/prediction_history.html", {"history": history})

# appoipment
@login_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.status = 'pending'
            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
        doctors = User.objects.filter(user_type='doctor')

    return render(request, "healthcare_app/book_appointment.html", {
        "form": form,
        "doctors": doctors
    })


@login_required
def appointment_list(request):
    if request.user.user_type == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.filter(patient=request.user)

    return render(request, "healthcare_app/appointment_list.html", {"appointments": appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user == appointment.patient:
        appointment.status = 'cancelled'
        appointment.save()
    else:
        messages.error(request, "You can only cancel your own appointments.")

    return redirect('appointment_list')

@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user)
    reports = PatientReport.objects.filter(patient=request.user)
    history = PredictionHistory.objects.filter(user=request.user)
    user_lab_tests = LabTest.objects.filter(user=request.user)

    patient_history, _ = PatientHistory.objects.get_or_create(patient=request.user)

    history_form = PatientHistoryForm(instance=patient_history)
    report_form = PatientReportForm()
    testimonial_form = TestimonialForm()

    if request.method == "POST":
        if "update_history" in request.POST:
            history_form = PatientHistoryForm(request.POST, instance=patient_history)
            if history_form.is_valid():
                history_form.save()
                messages.success(request, "Medical history updated successfully!")
                return redirect("patient_dashboard")

        elif "upload_report" in request.POST:
            report_form = PatientReportForm(request.POST, request.FILES)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.patient = request.user
                report.save()
                messages.success(request, "Report uploaded successfully!")
                return redirect("patient_dashboard")

        elif "submit_testimonial" in request.POST:
            testimonial_form = TestimonialForm(request.POST)
            if testimonial_form.is_valid():
                testimonial = testimonial_form.save(commit=False)
                testimonial.patient = request.user
                testimonial.save()
                messages.success(request, "Your testimonial has been submitted successfully!")
                return redirect("patient_dashboard")

    testimonials = Testimonial.objects.all().order_by('-created_at')[:5]  # Show latest 5 testimonials

    return render(request, "healthcare_app/patient_dashboard.html", {
        "appointments": appointments,
        "reports": reports,
        "history": history,
        "history_form": history_form,
        "report_form": report_form,
        "patient_history": patient_history,
        "testimonial_form": testimonial_form,
        "testimonials": testimonials,
        "user_lab_tests": user_lab_tests,
    })




@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor':
        return redirect('patient_dashboard')

    # Fetch all appointments assigned to this doctor
    appointments = Appointment.objects.filter(doctor=request.user).order_by('date')

    # Get unique patients assigned to the doctor
    patients = User.objects.filter(
        user_type="patient",
        patient_appointments__doctor=request.user
    ).distinct()

    return render(request, 'healthcare_app/doctor_dashboard.html', {
        "appointments": appointments,
        "patients": patients
    })


@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    appointment.status = 'confirmed'
    appointment.save()
    messages.success(request, "Appointment Approved!")
    return redirect('doctor_dashboard')


@login_required
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    appointment.status = 'cancelled'
    appointment.save()
    messages.warning(request, "Appointment Rejected!")
    return redirect('doctor_dashboard')

# ✅ Doctor Issues a Prescription
@login_required
def issue_prescription(request):
    if request.user.user_type != 'doctor':
        return redirect('dashboard')

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm()

    return render(request, 'healthcare_app/issue_prescription.html', {'form': form})

# ✅ View Prescriptions (For Patients)
@login_required
def prescription_list(request):
    if request.user.user_type == 'doctor':
        prescriptions = Prescription.objects.filter(doctor=request.user)
    else:
        prescriptions = Prescription.objects.filter(patient=request.user)

    return render(request, 'healthcare_app/prescription_list.html', {'prescriptions': prescriptions})


@login_required
def patient_details(request, patient_id):
    doctor = request.user
    patient = get_object_or_404(User, id=patient_id, user_type="patient")

    # Ensure the doctor has an appointment with this patient
    if not Appointment.objects.filter(doctor=doctor, patient=patient).exists():
        messages.error(request, "You are not authorized to view this patient's details.")
        return redirect('doctor_dashboard')

    # Fetch patient's medical history, reports, and prescriptions
    patient_history, _ = PatientHistory.objects.get_or_create(patient=patient)
    reports = PatientReport.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(patient=patient, doctor=doctor)

    return render(request, "healthcare_app/patient_details.html", {
        "patient": patient,
        "patient_history": patient_history,
        "reports": reports,
        "prescriptions": prescriptions,

    })



# ✅ List all medicines or create a new one
class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

# ✅ Retrieve, update, or delete a specific medicine
class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

def medicine_shop(request):
    query = request.GET.get("search", "").strip()  # Get search query from the URL

    if query:
        medicines = Medicine.objects.filter(
            brand_names__icontains=query
        ) | Medicine.objects.filter(
            generic_name__icontains=query
        )
    else:
        medicines = Medicine.objects.all()  # Show all medicines if no search query

    return render(request, "healthcare_app/medicines.html", {
        "medicines": medicines,
        "search_query": query,
    })

@login_required
def my_orders_page(request):
    orders = Order.objects.filter(user=request.user).select_related("medicine")

    return render(request, "healthcare_app/my_orders.html", {"orders": orders})

# lab test
@login_required
def available_lab_tests(request):
    """Display a list of available lab tests."""
    tests = AvailableLabTest.objects.all()
    return render(request, "healthcare_app/available_lab_tests.html", {"tests": tests})

@login_required
def book_lab_test(request):
    """Allow users to book a lab test."""
    if request.method == "POST":
        form = LabTestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Assign the logged-in user
            booking.save()
            return redirect("lab_test_success")
    else:
        form = LabTestForm()

    return render(request, "healthcare_app/book_lab_test.html", {"form": form})

@login_required
def lab_test_success(request):
    """Display a success message after booking."""
    return render(request, "healthcare_app/lab_test_success.html")
