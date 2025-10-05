import logging
#logging configuration
logging.basicConfig(
    filename="bookings.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
#class of room where we have room number, room type, price per night, is available, max guests
class Room:
    def __init__(self, room_number: int, room_type: str, price_per_night: float, max_guests: int):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = True
        self.max_guests = max_guests
    #function to book room
    def book_room(self):
        if self.is_available:
            self.is_available = False
            return True
        return False
    #function to release room
    def release_room(self):
        self.is_available = True
    #function to calculate price
    def calculate_price(self, nights: int):
        return self.price_per_night * nights
    #function to show room information
    def __str__(self):
        status = "Available" if self.is_available else "Booked"
        return f"Room {self.room_number} ({self.room_type}) - {status}, Price per night: ${self.price_per_night}"

#class of customer where we have name, budget, booked rooms
class Customer:
    def __init__(self, name: str, budget: float):
        self.name = name
        self.budget = budget
        self.booked_rooms = []
    #function to add room
    def add_room(self, room: Room):
        self.booked_rooms.append(room)
    #function to remove room
    def remove_room(self, room: Room):
        if room in self.booked_rooms:
            self.booked_rooms.remove(room)
    #function to pay for booking
    def pay_for_booking(self, total_price: float):
        if self.budget >= total_price:
            self.budget -= total_price
            return True
        return False
    #function to show booking summary
    def show_booking_summary(self):
        if not self.booked_rooms:
            return f"{self.name} has no bookings."
        rooms_info = ", ".join([f"{r.room_number}" for r in self.booked_rooms])
        return f"{self.name}'s Booked Rooms: {rooms_info}, Remaining Budget: ${self.budget}"

#class of hotel where we have name, rooms, bookings log
class Hotel:
    def __init__(self, name: str, rooms: list):
        self.name = name
        self.rooms = rooms
        self.bookings_log = []
    #function to show available rooms
    def show_available_rooms(self, room_type: str = None):
        available = [r for r in self.rooms if r.is_available]
        if room_type:
            available = [r for r in available if r.room_type.lower() == room_type.lower()]
        return available

    #function to calculate total booking
    def calculate_total_booking(self, room_number: int, nights: int):
        for room in self.rooms:
            if room.room_number == room_number:
                return room.calculate_price(nights)
        return 0.0
    #function to book room for customer

    def book_room_for_customer(self, customer: Customer, room_number: int, nights: int):
        room = next((r for r in self.rooms if r.room_number == room_number), None)
        if not room or not room.is_available:
            print("Room not available.")
            return False
    #function to calculate total booking
        total_price = self.calculate_total_booking(room_number, nights)
        if not customer.pay_for_booking(total_price):
            print("Not enough budget.")
            return False
    #function to book room
        room.book_room()
        customer.add_room(room)
        self.log_booking(customer, room, total_price)
        print(f"Room {room_number} successfully booked for {customer.name}.")
        return True
    #function to log booking
    def log_booking(self, customer: Customer, room: Room, total_price: float):
        record = f"{customer.name} booked Room {room.room_number} for ${total_price}"
        self.bookings_log.append(record)
        logging.info(record)
    #function to cancel booking
    def cancel_booking(self, customer: Customer, room_number: int):
        room = next((r for r in self.rooms if r.room_number == room_number), None)
        if room and room in customer.booked_rooms:
            room.release_room()
            customer.remove_room(room)
            print(f"Booking for Room {room_number} canceled.")
        else:
            print("No such booking found.")

