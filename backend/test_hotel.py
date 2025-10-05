import unittest
from app import Room, Customer, Hotel

class TestHotelBooking(unittest.TestCase):
    def setUp(self):
        self.room = Room(101, "Single", 50, 1)
        self.customer = Customer("Bacho", 150)
        self.hotel = Hotel("Test Hotel", [self.room])

    def test_pay_for_booking(self):
        result = self.customer.pay_for_booking(50)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 100)

    def test_book_only_available_room(self):
        self.hotel.book_room_for_customer(self.customer, 101, 1)
        self.assertFalse(self.room.is_available)

if __name__ == "__main__":
    unittest.main()
