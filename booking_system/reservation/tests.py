from django.test import TestCase
from reservation import models
from datetime import datetime

class MenuTest(TestCase):
    def test_get_item(self):
        item = models.Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")
        
class BookingTest(TestCase):
    def test_get_item(self):
        item = models.Booking.objects.create(name='Birthday', no_of_guests=5, booking_date=datetime.now())
        self.assertEqual(str(item), "Birthday : 5")