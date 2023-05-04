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
    fields = [f[0] for f in cursor.description]

    name = pokemon[29]
    type1 = pokemon[35]
    type2 = pokemon[36]
    strengths = []
    weaknesses = []
    for type in types:
 
        against_column_name = "against_" + type

        cursor.execute("PRAGMA table_info(imported_pokemon_data)")
        fields = [f[1] for f in cursor.fetchall()]
        against_column_index = fields.index(against_column_name)

        if pokemon[against_column_index]:
            against_value = float(pokemon[against_column_index])
            if against_value > 1:
                strengths.append(type)
            elif against_value < 1:
                weaknesses.append(type)


    print(f"Analyzing {i}\n{name} ({type1} {type2}) is strong against {strengths} but weak against {weaknesses}")


    connection.close()


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Check that the team has exactly 6 Pokemon
    while len(team) != 6:
        print("Error: Team does not have exactly 6 Pokemon.")
        answer = input("Would you like to try again? (Y)es or (N)o: ")
        if answer.upper() == "N" or answer.upper() == "NO":
            print("Bye for now!")
            sys.exit()

        # Re-prompt the user for their team
        team = []
        for i in range(6):
            pokemon_id = input("Enter Pokemon #" + str(i+1) + " ID: ")
            team.append(int(pokemon_id))

    # Write the pokemon team to the "teams" table
    conn = sqlite3.connect('pokemon.sqlite')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO teams (team_name, pokemon_1, pokemon_2, pokemon_3, pokemon_4, pokemon_5, pokemon_6) VALUES (?, ?, ?, ?, ?, ?, ?)', (teamName, team[0], team[1], team[2], team[3], team[4], team[5]))
    conn.commit()

    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")



