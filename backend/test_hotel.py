import unittest
from app import Room, Customer, Hotel

# ჰოტელის დაჯავშნის ტესტის კლასს ვქმნით
class TestHotelBooking(unittest.TestCase):  # ჰოტელის დაჯავშნის ტესტი
    # ყოველი ტესტის დაწყებამდე საჭირო ობიექტების შექმნა
    def setUp(self):
        self.room = Room(101, "Single", 50, 1)  # ოთახის ობიექტი: ნომერი, ტიპი, ღირებულება, მაქს. სტუმრები
        self.customer = Customer("Bacho", 150)  # კლიენტის ობიექტი: სახელი, ბიუჯეტი
        self.hotel = Hotel("Test Hotel", [self.room])  # ჰოტელის ობიექტი: სახელი, ოთახების სია

    # ფუნქცია, რომელიც ტესტავს გადახდას დაჯავშნისთვის
    def test_pay_for_booking(self):
        result = self.customer.pay_for_booking(50)  # კლიენტი იხდის 50 ერთეულს
        self.assertTrue(result)  # ვამოწმებთ, რომ გადახდა წარმატებით მოხდა
        self.assertEqual(self.customer.budget, 100)  # ვამოწმებთ, რომ ბიუჯეტი შემცირდა სწორად

    # ფუნქცია, რომელიც ტესტავს, რომ მხოლოდ თავისუფალი ოთახი შეიძლება დაჯავშნოთ
    def test_book_only_available_room(self):
        self.hotel.book_room_for_customer(self.customer, 101, 1)  # ვცდილობთ ოთახის დაჯავშნას
        self.assertFalse(self.room.is_available)  # ვამოწმებთ, რომ ოთახი აღარ არის თავისუფალი

# მთავარი ფუნქცია ტესტების გასაშვებად
if __name__ == "__main__":
    unittest.main()
