import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from healthcare_app.models import AvailableLabTest  # Ensure this model exists

class Command(BaseCommand):
    help = "Import lab tests from CSV file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "healthcare_app/static/data/medical_tests.csv")

        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                test_name = row.get("Test Name")  # ✅ Match CSV column header
                price = row.get("Approximate Price (₹)", "0")  # ✅ Match CSV header
                purpose = row.get("Purpose", "")

                # Ensure the price is converted to a number
                try:
                    price = float(price)
                except ValueError:
                    price = 0

                # Create or update the lab test entry
                AvailableLabTest.objects.update_or_create(
                    name=test_name,
                    defaults={"price": price, "description": purpose}
                )

        self.stdout.write(self.style.SUCCESS("Lab tests imported successfully!"))
