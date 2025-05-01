from django.contrib import admin
from .models import User, DoctorProfile, PatientProfile, PredictionHistory, Appointment, Prescription, PatientReport, PatientHistory, Medicine, Order, Testimonial, AvailableLabTest, LabTest, HealthPredictionHistory
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
admin.site.register(HealthPredictionHistory)
# admin.site.register(OrderItem)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = (
        "generic_name", 
        "brand_names", 
        "typical_use", 
        "price_range", 
        "image_link", 
        "price", 
        "dosage_instructions",  # Added to display dosage instructions
        "side_effects",  # Added to display side effects
        "ingredients",  # Added to display ingredients
        "is_prescription_required",  # Added to display prescription requirement
    )
    
    # Search functionality to search by fields
    search_fields = ("generic_name", "brand_names", "typical_use")
    
    # Filters to narrow down results in the admin interface
    list_filter = (
        "typical_use", 
        "is_prescription_required",  # Added to filter by prescription requirement
    )
    
    # Fields to be editable directly in the list view
    list_editable = ("price", "is_prescription_required")  # Price and prescription requirement can be edited directly in the list view

    # Customize the form layout for the detail view (optional)
    fieldsets = (
        (None, {
            'fields': ('generic_name', 'brand_names', 'typical_use', 'price_range', 'price', 'image_link', 'dosage_instructions', 'side_effects', 'ingredients', 'storage_instructions', 'warnings', 'prescription_instructions', 'is_prescription_required')
        }),
    )
    

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