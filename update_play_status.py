import mysql.connector

def update_player_status():
    mydb = mysql.connector.connect(
        host = "127.0.0.1",
        port = 3306,
        database = "flight_game_team12",
        user = "root",
        password = "xenun333",
        autocommit = True
    )
    mycursor = mydb.cursor()
    #Fetch player information
    mycursor.execute("SELECT id, player_name, co2_budget FROM player")
    player_data_list = mycursor.fetchall()
    for player_data in player_data_list:
        player_id, player_name, co2_budget = player_data
        # Calculate total travel
        mycursor.execute("SELECT SUM(co2_emission_per_km) FROM airplane INNER JOIN choice ON choice.plane_type = airplane.type WHERE choice.player_id = %s", (player_id,))
        total_travelled = mycursor.fetchone()[0] or 0
        # Calculate co2 consume
        mycursor.execute("SELECT SUM(co2_emission_per_km) FROM airplane INNER JOIN choice ON choice.plane_type = airplane.type WHERE choice.player_id = %s", (player_id,))
        co2_consumed = mycursor.fetchone()[0] or 0
        # Update player information
        mycursor.execute("UPDATE player SET total_travelled = %s, co2_consumed = %s WHERE id = %s", (total_travelled,co2_consumed, player_id ))
        print(f"Player '{player_name}' update:")
        print(f"Total Travelled: {total_travelled} km")
        print(f"CO2 Consumed: {co2_consumed} units")
    mycursor.close()
    mydb.close()
update_player_status()
