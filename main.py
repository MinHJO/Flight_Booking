import sqlite3
from datetime import datetime

# Connect to SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('flight_booking.db')
cursor = conn.cursor()

def display_countries():
    cursor.execute('SELECT * FROM countries')
    countries = cursor.fetchall()

    print("\nAvailable Cities:")
    print('| country_id |   country   |    continent    |')
    print('| ---------- | ----------- | --------------- |')
    for country in countries:
        print('| %10s | %11s | %15s |' %country)

def display_flights(country_id):
    # Display all available flights
    cursor.execute('SELECT * FROM flights WHERE country_id = ?', (country_id, ))
    flights = cursor.fetchall()
    
    print("\nAvailable Flights:")
    print('| country_id | flight_id | flight_number |      destination      |   departure_date   | available_seats |   price   |')
    print('| ---------- | --------- | ------------- | --------------------- | ------------------ | --------------- | --------- |')
    for flight in flights:
        print('| %10s | %9s | %13s | %21s | %18s | %15d | %9d |' %flight)

def book_flight(flight_id, num_seats):
    # Book seats for a specific flight
    cursor.execute('SELECT available_seats FROM flights WHERE flight_id = ?', (flight_id,))
    available_seats = cursor.fetchone()[0]

    if available_seats >= num_seats:
        cursor.execute('UPDATE flights SET available_seats = ? WHERE flight_id = ?', (available_seats - num_seats, flight_id))
        conn.commit()
        print(f"Booking successful! {num_seats} seat(s) booked.")
    else:
        print("Not enough available seats.")

def booked_flight(flight_id_to_book):
    cursor.execute('SELECT flight_id, flight_number, destination, departure_date FROM flights WHERE flight_id = ?', (flight_id_to_book, ))
    tickets = cursor.fetchall()
    
    print("\nYour Travel:")
    print('| flight_id | flight_number |      destination      |   departure_date   | number_of_seats |')
    print('| --------- | ------------- | --------------------- | ------------------ | --------------- |')
    for ticket in tickets:
        print('| %9s | %13s | %21s | %18s |' % ticket, ' %14d |' %num_seats_to_book)
    print("ENJOY YOUR TRAVEL.\n")

# Display available flights
display_countries()

country_id_to_book = int(input("Enter the country_id you want to book: "))

display_flights(country_id_to_book)

# Book a flight
flight_id_to_book = int(input("Enter the flight_id you want to book: "))
num_seats_to_book = int(input("Enter the number of seats you want to book: "))
book_flight(flight_id_to_book, num_seats_to_book)

# Display booked flights
booked_flight(flight_id_to_book)

# Close the database connection
conn.close()
