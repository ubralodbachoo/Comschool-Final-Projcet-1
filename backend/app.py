import logging

#ლოგირების კონფიგურაცია
logging.basicConfig(
    filename="bookings.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

#ოთახის კლასი სადაც გვაქვს ოთახის ნომერი, ოთახის ტიპი, ფასი ღამეში, ხელმისაწვდომია თუ არა, მაქსიმალური სტუმრები
class Room:
    def __init__(self, room_number: int, room_type: str, price_per_night: float, max_guests: int):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = True
        self.max_guests = max_guests

    #ფუნქცია ოთახის დასაჯავშნად
    def book_room(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    #ფუნქცია ოთახის გასათავისუფლებლად
    def release_room(self):
        self.is_available = True

    #ფუნქცია ფასის გამოსათვლელად
    def calculate_price(self, nights: int):
        return self.price_per_night * nights

    #ფუნქცია ოთახის ინფორმაციის საჩვენებლად
    def __str__(self):
        status = "ხელმისაწვდომი" if self.is_available else "დაჯავშნული"
        return f"ოთახი {self.room_number} ({self.room_type}) - {status}, ფასი ღამეში: ${self.price_per_night}"


#მომხმარებლის კლასი სადაც გვაქვს სახელი, ბიუჯეტი, დაჯავშნული ოთახები
class Customer:
    def __init__(self, name: str, budget: float):
        self.name = name
        self.budget = budget
        self.booked_rooms = []
        self.room_prices = {}

    #ფუნქცია ოთახის დასამატებლად
    def add_room(self, room: Room, total_price: float):
        self.booked_rooms.append(room)
        self.room_prices[room.room_number] = total_price

    #ფუნქცია ოთახის წასაშლელად
    def remove_room(self, room: Room):
        if room in self.booked_rooms:
            self.booked_rooms.remove(room)

            #ვშლით ღირებულებას dictionary-დან
            if room.room_number in self.room_prices:
                del self.room_prices[room.room_number]

    #ფუნქცია დაბრუნების თანხის მისაღებად
    def get_room_price(self, room_number: int):
        return self.room_prices.get(room_number, 0.0)

    #ფუნქცია თანხის დასაბრუნებლად
    def refund_money(self, amount: float):
        self.budget += amount

    #ფუნქცია ჯავშნის გადასახდელად
    def pay_for_booking(self, total_price: float):
        if self.budget >= total_price:
            self.budget -= total_price
            return True
        return False

    #ფუნქცია ჯავშნის ინფორმაციის საჩვენებლად
    def show_booking_summary(self):
        if not self.booked_rooms:
            return f"{self.name}-ს არ აქვს ჯავშანი."
        rooms_info = ", ".join([f"{r.room_number}" for r in self.booked_rooms])
        return f"{self.name}-ის დაჯავშნული ოთახები: {rooms_info}, დარჩენილი ბიუჯეტი: ${self.budget}"


#სასტუმროს კლასი სადაც გვაქვს სახელი, ოთახები
class Hotel:
    def __init__(self, name: str, rooms: list):
        self.name = name
        self.rooms = rooms

    #ფუნქცია ხელმისაწვდომი ოთახების საჩვენებლად
    def show_available_rooms(self, room_type: str = None):
        available = [r for r in self.rooms if r.is_available]
        if room_type:
            available = [r for r in available if r.room_type.lower() == room_type.lower()]
        return available

    #ფუნქცია სრული ჯავშნის გამოსათვლელად
    def calculate_total_booking(self, room_number: int, nights: int):
        for room in self.rooms:
            if room.room_number == room_number:
                return room.calculate_price(nights)
        return 0.0

    #ფუნქცია მომხმარებლისთვის ოთახის დასაჯავშნად
    def book_room_for_customer(self, customer: Customer, room_number: int, nights: int):
        room = next((r for r in self.rooms if r.room_number == room_number), None)
        if not room or not room.is_available:
            print("ოთახი არ არის ხელმისაწვდომი.")
            return False

        #სრული ფასის გამოთვლა
        total_price = self.calculate_total_booking(room_number, nights)
        if not customer.pay_for_booking(total_price):
            print("არ არის საკმარისი ბიუჯეტი.")
            return False

        #ოთახის დაჯავშნა
        room.book_room()
        customer.add_room(room, total_price)
        self.log_booking(customer, room, total_price)
        print(f"ოთახი {room_number} წარმატებით დაიჯავშნა {customer.name}-ისთვის.")
        return True

    #ფუნქცია ჯავშნის ჩასაწერად ლოგში
    def log_booking(self, customer: Customer, room: Room, total_price: float):
        record = f"{customer.name}-მ დაჯავშნა ოთახი {room.room_number} ${total_price}-ად"
        logging.info(record)

    #ფუნქცია ჯავშნის გასაუქმებლად
    def cancel_booking(self, customer: Customer, room_number: int):
        room = next((r for r in self.rooms if r.room_number == room_number), None)
        if room and room in customer.booked_rooms:

            #ვიღებთ გადახდილ თანხას
            refund_amount = customer.get_room_price(room_number)
            
            room.release_room()
            customer.remove_room(room)

            #ვაბრუნებთ თანხას
            customer.refund_money(refund_amount)

            #ვლოგავთ გაუქმებას
            cancel_record = f"{customer.name}-მ გააუქმა ოთახი {room_number} - დაბრუნდა ${refund_amount}"
            logging.info(cancel_record)
            
            print(f"ოთახი {room_number}-ის ჯავშანი გაუქმდა. ${refund_amount} დაუბრუნდა {customer.name}-ს.")
        else:
            print("ასეთი booking ვერ მოიძებნა.")
