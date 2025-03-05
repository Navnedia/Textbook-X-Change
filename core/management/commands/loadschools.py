import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from core.models import School

class Command(BaseCommand):
    help = "Load school data from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file.")

    def handle(self, *args, **options):
        file_path = options['csv_file']
        schools = []

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            # If your CSV has a header row with field names like NAME, WEBSITE, LATITUDE, LONGITUDE
            for row in reader:
                try:
                    school = School(
                        name=row['NAME'].strip(),
                        website=row['WEBSITE'].strip(),
                        lat=Decimal(row['LATITUDE'].strip()),
                        long=Decimal(row['LONGITUDE'].strip())
                    )
                    schools.append(school)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row {row}: {e}"))

        # Bulk create for better performance
        School.objects.bulk_create(schools, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(schools)} schools."))