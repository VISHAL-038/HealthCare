from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, DoctorProfileForm, PatientProfileForm, SymptomForm, AppointmentForm, PrescriptionForm, PatientReportForm, PatientHistoryForm, TestimonialForm, LabTestForm
from .models import User, DoctorProfile, PatientProfile, PredictionHistory, Appointment, Prescription, PatientReport, PatientHistory, Medicine, Cart, Testimonial, Order, AvailableLabTest, LabTest
import requests
import os
import pandas as pd
from django.conf import settings 
from .serializers import MedicineSerializer
from rest_framework import generics
import plotly.express as px
from django.utils.timezone import now
import plotly.graph_objects as go
from django.utils import timezone
from decimal import Decimal

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
    # Redirect if the user is not a doctor
    if request.user.user_type != "doctor":
        return redirect("patient_dashboard")

    # Fetch all appointments assigned to this doctor
    appointments = Appointment.objects.filter(doctor=request.user).order_by("date")

    # Get unique patients assigned to the doctor
    patients = User.objects.filter(
        user_type="patient",
        patient_appointments__doctor=request.user
    ).distinct()

    today = now()

    if appointments.exists():
        # Convert appointments to a DataFrame
        df = pd.DataFrame(list(appointments.values("date", "status", "patient")))

        # 📅 Monthly Appointments Trend
        df["Month"] = pd.to_datetime(df["date"]).dt.strftime("%b %Y")
        appointment_counts = df.groupby("Month").size().reset_index(name="Count")
        fig_monthly = px.line(
            appointment_counts,
            x="Month",
            y="Count",
            title="📅 Monthly Appointment Trend",
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["#007BFF"],
        )
        fig_monthly.update_layout(title_x=0.5)

        # 📅 Appointments per Weekday
        df["Weekday"] = pd.to_datetime(df["date"]).dt.day_name()
        weekday_counts = df["Weekday"].value_counts().reset_index()
        weekday_counts.columns = ["Weekday", "Count"]
        fig_weekly = px.bar(
            weekday_counts,
            x="Weekday",
            y="Count",
            title="📅 Weekly Bookings",
            text_auto=True,
            color_discrete_sequence=["#28a745"],
        )
        fig_weekly.update_layout(title_x=0.5)

        # 🩺 Confirmed vs Canceled Appointments
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_status = px.pie(
            status_counts,
            names="Status",
            values="Count",
            title="🩺 Confirmed vs Canceled Appointments",
            color_discrete_sequence=["#007BFF", "#FF5733"],
        )
        fig_status.update_layout(title_x=0.5)

        # Convert charts to HTML
        chart_monthly = fig_monthly.to_html(full_html=False)
        chart_weekly = fig_weekly.to_html(full_html=False)
        chart_status = fig_status.to_html(full_html=False)
    else:
        chart_monthly = chart_weekly = chart_status = None

    return render(
        request,
        "healthcare_app/doctor_dashboard.html",
        {
            "appointments": appointments,
            "patients": patients,
            "chart_monthly": chart_monthly,
            "chart_weekly": chart_weekly,
            "chart_status": chart_status,
        },
    )



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
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, medicine=medicine)

    if not created:
        cart_item.quantity += 1  # ✅ Increment quantity if item already exists
        cart_item.save()

    messages.success(request, "Added to cart!")
    return redirect("medicine_shop")

# ✅ View Cart
# ✅ Fix in view_cart()
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)  # ✅ Add ()

    return render(request, "healthcare_app/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
    })




# ✅ Remove from Cart
@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("view_cart")

# ✅ Proceed to Checkout (Move from Cart to Order)
@login_required
def checkout(request):
    from decimal import Decimal  # ✅ Ensure Decimal import

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            medicine=item.medicine,
            quantity=item.quantity,
            total_price=Decimal(str(item.total_price() or "0.00")),  # ✅ Fix NoneType issue
            status="pending"
        )

    cart_items.delete()
    messages.success(request, "Order placed successfully!")
    return redirect("my_orders_page")

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

@login_required
def health_trends(request):
    predictions = PredictionHistory.objects.filter(prediction_date__gte=timezone.now() - timezone.timedelta(days=30))
    symptom_chart_html = disease_chart_html = heatmap_chart_html = None
    
    if predictions.exists():
        df = pd.DataFrame(list(predictions.values('symptoms', 'predicted_disease')))
        df['symptoms'] = df['symptoms'].str.split(',\s*')
        all_symptoms = [symptom.strip() for sublist in df['symptoms'] for symptom in sublist if symptom]
        symptom_counts = pd.Series(all_symptoms).value_counts().reset_index()
        symptom_counts.columns = ['Symptom', 'Count']

        fig_symptoms = px.bar(
            symptom_counts.head(10), x='Symptom', y='Count', title="Top 10 Symptoms This Month",
            text_auto=True, color_discrete_sequence=['#007BFF']
        )
        fig_symptoms.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=50, b=100),
            title_x=0.5, font=dict(size=14)
        )
        symptom_chart_html = fig_symptoms.to_html(full_html=False)

        disease_counts = df['predicted_disease'].value_counts().reset_index()
        disease_counts.columns = ['Disease', 'Count']
        fig_diseases = px.bar(
            disease_counts.head(10), y='Disease', x='Count', title="Top 10 Diagnosed Diseases",
            text_auto=True, orientation='h', color_discrete_sequence=['#FF5733']
        )
        fig_diseases.update_layout(
            margin=dict(l=150, r=50, t=50, b=50), title_x=0.5, font=dict(size=14)
        )
        disease_chart_html = fig_diseases.to_html(full_html=False)

        heatmap_df = df.explode('symptoms').dropna(subset=['symptoms', 'predicted_disease'])
        symptom_matrix = pd.crosstab(index=heatmap_df['symptoms'], columns=heatmap_df['predicted_disease'])
        fig_heatmap = go.Figure(
            data=go.Heatmap(
                z=symptom_matrix.values, x=symptom_matrix.columns, y=symptom_matrix.index,
                colorscale='Viridis', hoverongaps=False
            )
        )
        fig_heatmap.update_layout(
            title="Symptom Co-Occurrence Heatmap", xaxis_title="Diseases", yaxis_title="Symptoms",
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            title_x=0.5, font=dict(size=14)
        )
        heatmap_chart_html = fig_heatmap.to_html(full_html=False)
    
    return render(request, 'healthcare_app/health_trends.html', {
        'symptom_chart': symptom_chart_html,
        'disease_chart': disease_chart_html,
        'heatmap_chart': heatmap_chart_html,
    })