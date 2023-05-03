import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []

for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    pokemon_id = int(arg)
    connection = sqlite3.connect("pokemon.sqlite")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM imported_pokemon_data WHERE pokedex_number=?", (pokemon_id,))
    pokemon = cursor.fetchone()

    type1_name = pokemon[2]
    type2_name = ""
    if pokemon[3]:
        type2_name = pokemon[3]

    strengths = []
    weaknesses = []

    for j, t in enumerate(types):
        if pokemon[3 + j] != "":
            if float(pokemon[3 + j]) > 1:
                weaknesses.append(t)
            elif float(pokemon[3 + j]) < 1:
                strengths.append(t)

    print(f"Analyzing {pokemon[1]}")
    print(f"{pokemon[1]} ({type1_name} {type2_name}) is strong against {strengths} but weak against {weaknesses}")

    connection.close()


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    conn = sqlite3.connect('pokemon.sqlite')
    cursor = conn.cursor()
    if len(team) == 6:
        cursor.execute('INSERT INTO teams (team_name, pokemon_1, pokemon_2, pokemon_3, pokemon_4, pokemon_5, pokemon_6) VALUES (?, ?, ?, ?, ?, ?, ?)', (teamName, team[0], team[1], team[2], team[3], team[4], team[5]))
    else:
        print("Error: Team does not have exactly 6 Pokemon.")
    conn.commit()

    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")


