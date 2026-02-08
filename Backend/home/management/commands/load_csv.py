from django.core.management.base import BaseCommand
from home.models import DummyData
import csv

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('Medicaldataset.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                DummyData.objects.create(
                    Age=row['Age'],
                    Gender=row['Gender'],
                    HeartRate=row['HeartRate'],
                    SystolicBloodPressure=row['SystolicBloodPressure'],
                    DiastolicBloodPressure=row['DiastolicBloodPressure'],
                    BloodSugar=row['BloodSugar'],
                    CK_MB=row['CK_MB'],
                    Troponin=row['Troponin']
                )

        self.stdout.write(self.style.SUCCESS("CSV data successfully loaded"))
