import unittest
from app import Room, Customer, Hotel


#class of test hotel booking
class TestHotelBooking(unittest.TestCase):  #test hotel booking
    def setUp(self):
        self.room = Room(101, "Single", 50, 1)
        self.customer = Customer("Bacho", 150)
        self.hotel = Hotel("Test Hotel", [self.room])
    #function to test pay for booking
    def test_pay_for_booking(self):
        result = self.customer.pay_for_booking(50)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 100)
    #function to test book only available room
    def test_book_only_available_room(self):
        self.hotel.book_room_for_customer(self.customer, 101, 1)
        self.assertFalse(self.room.is_available)

#function to test main
if __name__ == "__main__":
    unittest.main()
