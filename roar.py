import mysql.connector
import random

# Establish a MySQL database connection
mydb = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game_team12',
    user='root',
    password='xenun333',
    autocommit=True
)

# Function to select a random event
def select_random_event():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT info, type, probability, co2_change, distance_change FROM event")
    events_data = mycursor.fetchall()

    if not events_data:
        return None

    selected_event = random.choice(events_data)
    mycursor.close()

    return selected_event

# Call the function to get a random event
selected_event = select_random_event()

# Display the selected event details
if selected_event:
    info, event_type, probability, co2_change, distance_change = selected_event
    print("Random Event:")
    print(f"Info: {info}")
    print(f"Type: {event_type}")
    print(f"Probability: {probability}")
    print(f"CO2 Change: {co2_change}")
    print(f"Distance Change: {distance_change}")
else:
    print("No event selected")