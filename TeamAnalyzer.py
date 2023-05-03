import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

pokedex_numbers = sys.argv[1:]

if len(pokedex_numbers) != 6:
    print("Error: Please provide exactly 6 Pokedex numbers.")
    sys.exit(1)


pokedex_numbers = [int(n) for n in pokedex_numbers]

# Loop through each Pokedex number and analyze the Pokemon
for pokedex_number in pokedex_numbers:
    # Your code to analyze the Pokemon goes here

    team = []
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue

        pokemon_id = int(arg)
        connection = sqlite3.connect("pokemon.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM imported_pokemon_data WHERE pokedex_number=?", (pokemon_id,))
        pokemon = cursor.fetchone()

        print(f"Analyzing {pokemon[1]}")
        for j, t in enumerate(types):
            if pokemon[3 + j] != "":
                if float(pokemon[3 + j]) > 1:
                    print(f"{t.capitalize()} is weak against {pokemon[1]}")
                elif float(pokemon[3 + j]) < 1:
                    print(f"{t.capitalize()} is strong against {pokemon[1]}")

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

