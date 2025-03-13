import csv
import os
import sys
import django

# ✅ Get the BASE DIRECTORY
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ Add the project to Python path
sys.path.append(BASE_DIR)

# ✅ Setup Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthcare_project.settings")
django.setup()

from healthcare_app.models import Medicine

CSV_FILE_PATH = os.path.join(BASE_DIR, 'healthcare_app', 'static', 'data', 'medicine_data.csv')

def import_medicine_data():
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Medicine.objects.create(
                generic_name=row['Generic Name'],
                brand_names=row['Common Brand Names'],
                typical_use=row['Typical Use'],
                price_range=row['Approximate Price (per pack/bottle)'],
                image_link=row.get('Image Link', '')
            )
    print("✅ Medicine data imported successfully!")

if __name__ == "__main__":
    import_medicine_data()
