from django.test import TestCase
from .models import Reservation 
from datetime import datetime

# Create your tests here.


class ReservationModelTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.reservation = Reservation.objects.create(
            first_name="John",
            last_name="Mac Donald"
        )    
        
        
    def test_fields(self):
        self.assertIsInstance(self.reservation.first_name, str)
        self.assertIsInstance(self.reservation.last_name, str)
        
        
    def test_timestamps(self):
        self.assertIsInstance(self.reservation.booking_time, datetime)
        