from django.urls import path
from .views import (
    home, register, user_login, user_logout, dashboard, doctor_dashboard, patient_dashboard,
    disease_prediction, prediction_history, book_appointment, appointment_list, cancel_appointment,
    approve_appointment, reject_appointment, prescription_list, issue_prescription, patient_details,
    MedicineDetailView, MedicineListCreateView, medicine_shop, my_orders_page, 
    available_lab_tests, book_lab_test, lab_test_success, health_trends  # ✅ Import lab test views
)
from .views_medicine import medicine_list, place_order, my_orders

urlpatterns = [
    # Home Page
    path('', home, name='home'),

    # Authentication Routes
    path('auth/register/', register, name='register'),
    path('auth/login/', user_login, name='login'),
    path('auth/logout/', user_logout, name='logout'),

    # Dashboard Routes
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', patient_dashboard, name='patient_dashboard'),
    path("patient/<int:patient_id>/", patient_details, name="patient_details"),

    # Disease Prediction
    path('predict/', disease_prediction, name='disease_prediction'),
    path("history/", prediction_history, name="prediction_history"),

    # Appointments
    path('appointments/book/', book_appointment, name='book_appointment'),
    path('appointments/', appointment_list, name='appointment_list'),
    path('appointments/cancel/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),

    # Doctor Actions
    path('appointments/approve/<int:appointment_id>/', approve_appointment, name='approve_appointment'),
    path('appointments/reject/<int:appointment_id>/', reject_appointment, name='reject_appointment'),

    # Prescriptions
    path('prescriptions/', prescription_list, name='prescription_list'),
    path('prescriptions/issue/', issue_prescription, name='issue_prescription'),

    # API for Medicine Data Management
    path('api/medicine/all/', MedicineListCreateView.as_view(), name='medicine-list'),
    path('api/medicine/<int:pk>/', MedicineDetailView.as_view(), name='medicine-detail'),

    # API for Public Medicine Browsing & Orders
    path('api/shop/medicines/', medicine_list, name='shop_medicine_list'),
    path('api/shop/order/', place_order, name='shop_place_order'),
    path('api/shop/my-orders/', my_orders, name='shop_my_orders'),

    # ✅ Serve the medicine shop frontend page
    path('medicines/', medicine_shop, name='medicine_shop'),
    path('my-orders/', my_orders_page, name='my_orders_page'),  # ✅ Added missing comma

    # ✅ Lab test booking URLs
    path("lab-tests/", available_lab_tests, name="available_lab_tests"),
    path("book-lab-test/", book_lab_test, name="book_lab_test"),
    path("lab-test-success/", lab_test_success, name="lab_test_success"),

    # trends
    path('health-trends/', health_trends, name='health_trends'),
]
