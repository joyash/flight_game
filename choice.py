import mysql.connector

mydb = mysql.connector.connect(
    host = '127.0.0.1',
    port = 3306,
    database = 'flight_game_team12',
    user = 'root',
    password = 'xenun333',
    autocommit = True
)

#fetch airplane data from the airplane table
def show_airplane():
    mycursor = mydb.cursor()
    mycursor.execute("select type, size, capacity, co2_emission_per_km, max_range FROM airplane")
    results = mycursor.fetchall()

    print("Available airplane from types:")
    for idx, row in enumerate(results, start = 1):
        print(f"{idx}. {row[0]}")
    mycursor.close()

def update_choice():
    show_airplane() # show airplane information to the user
    user_name = input("Enter your player name:  ")
    user_choice_idx = int(input("Enter the number of the airplane type you want to choose:  "))
    mycursor = mydb.cursor()
    # check if the player exist based on their name
    sql = "SELECT id FROM player WHERE player_name = %s"
    mycursor.execute(sql, (user_name,))
    player_record = mycursor.fetchone()

    if player_record:
        player_id = player_record[0]
        mycursor.execute("SELECT type FROM airplane")
        airplane_types = mycursor.fetchall()

        if 1 <= user_choice_idx <= len(airplane_types):
            user_choice = airplane_types[user_choice_idx - 1][0]
            # Retrieve distance_ref from the 'distance' table based on the chosen airplane type
            distance_query = "SELECT record_id FROM distance WHERE departure_code = %s"
            mycursor.execute(distance_query, (user_choice,))
            distance_record = mycursor.fetchone()

            if distance_record:
                distance_ref = distance_record[0]
                # Retrieve co2_spent from the 'player' table based on the player's ID

                co2_query = "SELECT co2_consumed FROM player WHERE id = %s"
                mycursor.execute(co2_query, (player_id))
                co2_record = mycursor.fetchone()

                if co2_record:
                    co2_spent = co2_record[0]

                    # Insert the user's choice into the 'choice' table with retrieved values
                    insert_query = "INSERT INTO choice (player_id, plane_type, distance_ref, co2_spent) VALUES (%s, %s, %s, %s)"
                    mycursor.execute(insert_query, (player_id, user_choice, distance_ref, co2_spent))
                    mydb.commit()

                    print(f"Choice recorded for player with id {player_id}")
                else:
                     print("Co2 data not found for the table.")
            else:
                print("Distance data not found for the chosen airplane type.")
        else:
            print("Invalid choice. Please select a valid airplane type number.")
    else:
        print("Player not found. Please check your player name.")

    mycursor.close()
if __name__ == "__main__":
    update_choice()

