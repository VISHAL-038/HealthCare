from django.contrib import admin
from .models import User, DoctorProfile, PatientProfile, PredictionHistory, Appointment, Prescription, PatientReport, PatientHistory, Medicine, Order, Testimonial, AvailableLabTest, LabTest
# OrderItem

# Register all models
admin.site.register(User)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(PredictionHistory)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PatientReport)
admin.site.register(PatientHistory)
admin.site.register(AvailableLabTest)
admin.site.register(LabTest)
# admin.site.register(OrderItem)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("generic_name", "brand_names", "typical_use", "price_range","image_link","price")  # Display columns
    search_fields = ("generic_name", "brand_names")  # Add search functionality
    list_filter = ("typical_use",)  # Add filter optionß

# ✅ Register Order Model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "medicine", "quantity", "total_price", "status", "order_date")
    search_fields = ("user__username", "medicine__generic_name")
    list_filter = ("status", "order_date")

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('patient', 'rating', 'created_at')
    search_fields = ('patient__username', 'feedback')
    list_filter = ('rating', 'created_at')