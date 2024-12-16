from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.db import transaction
import pandas as pd
import math

from core.models import CarMake, CarModel, Car
from core.permissions.is_admin import IsAdminUserRole
from core.utils.logger import exception_log

class ImportCarsView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAdminUserRole]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
        except Exception as e:
            exception_log(e, __file__)
            return Response({"error": f"Error reading file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        created_objects = {"makes": 0, "models": 0, "cars": 0}

        with transaction.atomic():
            try:
                for _, row in df.iterrows():
                    fuel_mapping = {'P': 'petrol', 'D': 'diesel', 'E': 'electric', 'H': 'hybrid'}
                    transmission_mapping = {'A': 'automatic', 'M': 'manual'}
                    car_class_mapping = {'N': 'normal', 'L': 'luxe', 'S': 'sport', 'U': 'utility'}

                    try:
                        fuel = fuel_mapping[row["Fuel"]]
                        transmission = transmission_mapping[row["Transmission"]]
                        car_class = car_class_mapping[row["Class"]]
                    except KeyError as e:
                        raise ValueError(f"Invalid value for field: {e.args[0]}")

                    
                    make, created = CarMake.objects.get_or_create(name=row["Make"])
                    if created:
                        created_objects["makes"] += 1

                    model, created = CarModel.objects.get_or_create(
                        make=make, 
                        name=row["Model"]
                    )
                    if created:
                        created_objects["models"] += 1

                    is_unlimited = row.get("Unlimited") == 1
                    car_version = row.get("Version", "")
                    car_version = car_version if car_version and not isinstance(car_version, float) or not math.isnan(car_version) else ""
                    car_type = row["Type"]
                    if car_type not in ('suv', 'sedan', 'van', 'hatchback', 'convertible'):
                        raise ValueError("Invalid value for field: Type (Valid Types: suv, sedan, van, hatchback and convertible).")
                    year = row.get('Year')
                    formatted_year = str(int(year) if year and not math.isnan(year) else '')                    
                    max_available_cars = int(row.get("Max") if row.get("Max") is not None and not math.isnan(row.get("Max")) else 1)
                    #TODO: verify agence
                    
                    _car = Car.objects.create(
                        car_make=make,
                        car_model=model,
                        car_type=car_type,
                        car_class=car_class,
                        car_version=car_version,
                        transmission_type=transmission,
                        fuel_type=fuel,
                        seats=row["Seats"],
                        price_per_day=row["Price"],
                        partner_id=row.get("Agence"),
                        max_available_cars=max_available_cars,
                        is_unlimited=is_unlimited,
                        year=formatted_year
                    )
                    created_objects["cars"] += 1

                return Response({
                    "message": "Cars imported successfully.",
                    "details": created_objects
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                exception_log(e, __file__)
                transaction.set_rollback(True)
                return Response({"error": f"Error processing data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
