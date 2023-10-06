import mysql.connector
import random

mydb = mysql.connector.connect(
    host =  '127.0.0.1',
    port = 3306,
    database = 'flight_game_team12',
    user = 'root',
    password = 'xenun333',
    autocommit = True
)
#function to retrive and select a random event

def select_random_event():
    mycursor= mydb.cursor()
    #retrive event data from database
    mycursor.execute("SELECT id, info, type, IFNULL(co2_change, 0.0) AS co2_change, IFNULL(distance_change, 0.0) AS distange_change FROM event")
    events_data = mycursor.fetchall()
    # Filter out events with insufficient data
    valid_events = [event for event in events_data if len(event) == 6]
    # calculate total probability
    total_probability = sum(event[3] for event in valid_events)
    # if total probability is 0, add a default event with non-zero probability
    if total_probability == 0:
        default_event = (0, "Default Event", "default", 0.1, 0.01, 0.05)
        valid_events.append(default_event)
        total_probability += 0.1 # adjusting total probability
    #generate a random number
    random_value = random.uniform(0, 1)
    cumulative_probability = 0

    #iterate through events
    for event in valid_events:
        event_id, info, event_type, probability, co2_change, distance_change = event

        # Check for missing values and assign defaults
        if event_type is None:
            event_type = "default_type"  # Assign a default event type
        if probability is None:
            probability = 0.1  # Assign a default probability
        if co2_change is None:
            co2_change = 0.01  # Assign a default CO2 change
        if distance_change is None:
            distance_change = 0.05  # Assign a default distance change

        normalized_probability = probability / total_probability
        cumulative_probability += normalized_probability

        if random_value <= cumulative_probability:
            selected_event = event
            break
    else:
        selected_event = None
    mycursor.close()

    return selected_event
selected_event = select_random_event()

if selected_event:
    event_id, info, event_type, probability, co2_change, distance_change = selected_event
    print("Random Event:")
    print(f"ID: {event_id}")
    print(f"Info: {info}")
    print(f"Type: {event_type}")
    print(f"Probability: {probability}")
    print(f"CO2 Change: {co2_change}")
    print(f"Distance Change: {distance_change}")
else:
    print("No event selected")

