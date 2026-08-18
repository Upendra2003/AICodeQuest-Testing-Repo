from datetime import datetime


class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.available = True

    def display(self):
        status = "Available" if self.available else "Occupied"

        print("-" * 45)
        print(f"Room Number : {self.room_number}")
        print(f"Room Type   : {self.room_type}")
        print(f"Price/Night : ${self.price:.2f}")
        print(f"Status      : {status}")


class Guest:
    def __init__(self, guest_id, name, phone):
        self.guest_id = guest_id
        self.name = name
        self.phone = phone

    def display(self):
        print("-" * 45)
        print(f"Guest ID : {self.guest_id}")
        print(f"Name     : {self.name}")
        print(f"Phone    : {self.phone}")


class Reservation:
    def __init__(
        self,
        reservation_id,
        guest,
        room,
        nights
    ):
        self.reservation_id = reservation_id
        self.guest = guest
        self.room = room
        self.nights = nights
        self.check_in = datetime.now()
        self.checked_out = False

    def total_bill(self):
        return self.room.price * self.nights

    def display(self):
        status = (
            "Checked Out"
            if self.checked_out
            else "Active"
        )

        print("-" * 50)
        print(
            f"Reservation ID : "
            f"{self.reservation_id}"
        )
        print(
            f"Guest          : "
            f"{self.guest.name}"
        )
        print(
            f"Room           : "
            f"{self.room.room_number}"
        )
        print(
            f"Room Type      : "
            f"{self.room.room_type}"
        )
        print(
            f"Nights         : "
            f"{self.nights}"
        )
        print(
            f"Total Bill     : "
            f"${self.total_bill():.2f}"
        )
        print(f"Status         : {status}")


class Hotel:
    def __init__(self):
        self.rooms = []
        self.guests = []
        self.reservations = []

        self.next_guest_id = 1
        self.next_reservation_id = 1001

        self.initialize_rooms()

    # ----------------------------------------
    # Initialize Hotel Rooms
    # ----------------------------------------

    def initialize_rooms(self):

        self.rooms.append(
            Room(101, "Single", 50)
        )

        self.rooms.append(
            Room(102, "Single", 50)
        )

        self.rooms.append(
            Room(201, "Double", 80)
        )

        self.rooms.append(
            Room(202, "Double", 80)
        )

        self.rooms.append(
            Room(301, "Deluxe", 120)
        )

        self.rooms.append(
            Room(302, "Deluxe", 120)
        )

        self.rooms.append(
            Room(401, "Suite", 200)
        )

    # ----------------------------------------
    # Find Room
    # ----------------------------------------

    def find_room(self, room_number):

        for room in self.rooms:
            if room.room_number == room_number:
                return room

        return None

    # ----------------------------------------
    # Find Guest
    # ----------------------------------------

    def find_guest(self, guest_id):

        for guest in self.guests:
            if guest.guest_id == guest_id:
                return guest

        return None

    # ----------------------------------------
    # Find Reservation
    # ----------------------------------------

    def find_reservation(
        self,
        reservation_id
    ):

        for reservation in self.reservations:
            if (
                reservation.reservation_id
                == reservation_id
            ):
                return reservation

        return None

    # ----------------------------------------
    # Display All Rooms
    # ----------------------------------------

    def display_rooms(self):

        print("\n========== HOTEL ROOMS ==========")

        for room in self.rooms:
            room.display()

    # ----------------------------------------
    # Display Available Rooms
    # ----------------------------------------

    def available_rooms(self):

        print(
            "\n========== AVAILABLE ROOMS =========="
        )

        found = False

        for room in self.rooms:

            if room.available:
                room.display()
                found = True

        if not found:
            print("No rooms are currently available.")

    # ----------------------------------------
    # Search Rooms By Type
    # ----------------------------------------

    def search_room_type(self):

        room_type = input(
            "Enter room type: "
        ).strip().lower()

        found = False

        for room in self.rooms:

            if (
                room.room_type.lower()
                == room_type
                and room.available
            ):
                room.display()
                found = True

        if not found:
            print(
                "No available rooms "
                "of this type."
            )

    # ----------------------------------------
    # Register Guest
    # ----------------------------------------

    def register_guest(self):

        name = input(
            "Enter guest name: "
        ).strip()

        phone = input(
            "Enter phone number: "
        ).strip()

        if not name or not phone:
            print(
                "Name and phone are required."
            )
            return

        guest = Guest(
            self.next_guest_id,
            name,
            phone
        )

        self.guests.append(guest)

        print(
            "\nGuest registered successfully."
        )

        print(
            f"Guest ID: {self.next_guest_id}"
        )

        self.next_guest_id += 1

    # ----------------------------------------
    # Display Guests
    # ----------------------------------------

    def display_guests(self):

        if not self.guests:
            print("No guests registered.")
            return

        print("\n========== GUESTS ==========")

        for guest in self.guests:
            guest.display()

    # ----------------------------------------
    # Make Reservation
    # ----------------------------------------

    def make_reservation(self):

        if not self.guests:
            print(
                "Please register a guest first."
            )
            return

        self.display_guests()

        try:
            guest_id = int(
                input("Enter guest ID: ")
            )
        except ValueError:
            print("Invalid guest ID.")
            return

        guest = self.find_guest(guest_id)

        if guest is None:
            print("Guest not found.")
            return

        self.available_rooms()

        try:
            room_number = int(
                input("Enter room number: ")
            )
        except ValueError:
            print("Invalid room number.")
            return

        room = self.find_room(room_number)

        if room is None:
            print("Room not found.")
            return

        if not room.available:
            print("Room is already occupied.")
            return

        try:
            nights = int(
                input("Enter number of nights: ")
            )
        except ValueError:
            print("Invalid number of nights.")
            return

        if nights <= 0:
            print(
                "Number of nights must be positive."
            )
            return

        reservation = Reservation(
            self.next_reservation_id,
            guest,
            room,
            nights
        )

        self.reservations.append(reservation)

        room.available = False

        print(
            "\nReservation created successfully."
        )

        print(
            f"Reservation ID: "
            f"{self.next_reservation_id}"
        )

        print(
            f"Total Bill: "
            f"${reservation.total_bill():.2f}"
        )

        self.next_reservation_id += 1

    # ----------------------------------------
    # Display Reservations
    # ----------------------------------------

    def display_reservations(self):

        if not self.reservations:
            print(
                "No reservations available."
            )
            return

        print(
            "\n========== RESERVATIONS =========="
        )

        for reservation in self.reservations:
            reservation.display()

    # ----------------------------------------
    # Search Reservation
    # ----------------------------------------

    def search_reservation(self):

        try:
            reservation_id = int(
                input(
                    "Enter reservation ID: "
                )
            )
        except ValueError:
            print("Invalid reservation ID.")
            return

        reservation = self.find_reservation(
            reservation_id
        )

        if reservation is None:
            print("Reservation not found.")
            return

        reservation.display()

    # ----------------------------------------
    # Check Out Guest
    # ----------------------------------------

    def checkout(self):

        try:
            reservation_id = int(
                input(
                    "Enter reservation ID: "
                )
            )
        except ValueError:
            print("Invalid reservation ID.")
            return

        reservation = self.find_reservation(
            reservation_id
        )

        if reservation is None:
            print("Reservation not found.")
            return

        if reservation.checked_out:
            print(
                "Guest has already checked out."
            )
            return

        bill = reservation.total_bill()

        reservation.checked_out = True

        reservation.room.available = True

        print(
            "\n========== CHECKOUT =========="
        )

        print(
            f"Guest: "
            f"{reservation.guest.name}"
        )

        print(
            f"Room: "
            f"{reservation.room.room_number}"
        )

        print(
            f"Total Bill: ${bill:.2f}"
        )

        print(
            "Checkout completed successfully."
        )

    # ----------------------------------------
    # Calculate Hotel Revenue
    # ----------------------------------------

    def calculate_revenue(self):

        total = 0

        for reservation in self.reservations:

            if reservation.checked_out:
                total += reservation.total_bill()

        print(
            "\nTotal completed revenue: "
            f"${total:.2f}"
        )

    # ----------------------------------------
    # Hotel Statistics
    # ----------------------------------------

    def statistics(self):

        total_rooms = len(self.rooms)

        available = 0
        occupied = 0

        for room in self.rooms:

            if room.available:
                available += 1
            else:
                occupied += 1

        active_reservations = 0

        for reservation in self.reservations:

            if not reservation.checked_out:
                active_reservations += 1

        total_revenue = 0

        for reservation in self.reservations:

            if reservation.checked_out:
                total_revenue += (
                    reservation.total_bill()
                )

        print(
            "\n========== HOTEL STATISTICS =========="
        )

        print(
            f"Total Rooms          : {total_rooms}"
        )

        print(
            f"Available Rooms      : {available}"
        )

        print(
            f"Occupied Rooms       : {occupied}"
        )

        print(
            f"Registered Guests    : "
            f"{len(self.guests)}"
        )

        print(
            f"Total Reservations   : "
            f"{len(self.reservations)}"
        )

        print(
            f"Active Reservations  : "
            f"{active_reservations}"
        )

        print(
            f"Completed Revenue    : "
            f"${total_revenue:.2f}"
        )

    # ----------------------------------------
    # Cancel Reservation
    # ----------------------------------------

    def cancel_reservation(self):

        try:
            reservation_id = int(
                input(
                    "Enter reservation ID: "
                )
            )
        except ValueError:
            print("Invalid reservation ID.")
            return

        reservation = self.find_reservation(
            reservation_id
        )

        if reservation is None:
            print("Reservation not found.")
            return

        if reservation.checked_out:
            print(
                "Completed reservations "
                "cannot be cancelled."
            )
            return

        reservation.room.available = True

        self.reservations.remove(
            reservation
        )

        print(
            "Reservation cancelled successfully."
        )

    # ----------------------------------------
    # Menu
    # ----------------------------------------

    def menu(self):

        print("\n")
        print("=" * 50)
        print("       HOTEL RESERVATION SYSTEM")
        print("=" * 50)

        print("1.  Display All Rooms")
        print("2.  Display Available Rooms")
        print("3.  Search Room By Type")
        print("4.  Register Guest")
        print("5.  Display Guests")
        print("6.  Make Reservation")
        print("7.  Display Reservations")
        print("8.  Search Reservation")
        print("9.  Check Out Guest")
        print("10. Cancel Reservation")
        print("11. Calculate Revenue")
        print("12. Hotel Statistics")
        print("13. Exit")

        print("=" * 50)


# ----------------------------------------
# Main Program
# ----------------------------------------

def main():

    hotel = Hotel()

    print(
        "Welcome to the Hotel "
        "Reservation Management System!"
    )

    while True:

        hotel.menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            hotel.display_rooms()

        elif choice == "2":

            hotel.available_rooms()

        elif choice == "3":

            hotel.search_room_type()

        elif choice == "4":

            hotel.register_guest()

        elif choice == "5":

            hotel.display_guests()

        elif choice == "6":

            hotel.make_reservation()

        elif choice == "7":

            hotel.display_reservations()

        elif choice == "8":

            hotel.search_reservation()

        elif choice == "9":

            hotel.checkout()

        elif choice == "10":

            hotel.cancel_reservation()

        elif choice == "11":

            hotel.calculate_revenue()

        elif choice == "12":

            hotel.statistics()

        elif choice == "13":

            print(
                "\nThank you for using "
                "the Hotel Reservation System."
            )
            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-13."
            )


if __name__ == "__main__":
    main()
