# **************** GLOBAL VARIABLES **************** #

young_dwarves = [8, 3, 2, "Young dwarves", "Young dwarf"]
dwarves = [10, 5, 4, "Dwarves", "Dwarf"]
top_dwarves = [13, 7, 6, "Top dwarves", "Top dwarf"]
young_soldiers = [16, 10, 9, "Young soldiers", "Young soldier"]
soldiers = [20, 15, 14, "Soldiers", "Soldier"]
doorkeepers = [30, 1, 25, "Doorkeepers", "Doorkeeper"]
top_doorkeepers = [40, 1, 35, "Top doorkeepers", "Top doorkeeper"]
fire_ants = [10, 30, 15, "Fire ants", "Fire ant"]
top_fire_ants = [12, 35, 18, "Top fire ants", "Top fire ant"]
top_soldiers = [27, 24, 23, "Top soldiers", "Top soldier"]
tanks = [35, 55, 1, "Tanks", "Tank"]
top_tanks = [50, 80, 1, "Top tanks", "Top tanks"]
killers = [50, 50, 50, "Killers", "Killer"]
top_killers = [55, 55, 55, "Top killers", "Top killer"]

antz_units = [young_dwarves, dwarves, top_dwarves, young_soldiers, soldiers, doorkeepers, top_doorkeepers,
              fire_ants, top_fire_ants, top_soldiers, tanks, top_tanks, killers, top_killers]


# ******************* FUNCTIONS ******************** #

# Get a formatted string version of a big number
# e.g. format_number(12345678) will return "12 345 678"
def format_number(number):
    return '{:,}'.format(number).replace(',', ' ')


# Take an army
# e.g. [111, 222, 0, 0, 333, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Return it as it would be in Antzzz
# For the example above: "111 Young dwarves, 222 Dwarves, 333 Soldiers."
def get_readable_army(army):
    first = True
    readable_army = ""
    for i in range(14):
        if army[i] > 0:
            if not first:
                readable_army += ", "
            first = False
            if army[i] == 1:
                readable_army += format_number(army[i]) + " " + antz_units[i][4]
            else:
                readable_army += format_number(army[i]) + " " + antz_units[i][3]
    if first:
        readable_army += "None"
    return readable_army + "."


# Take a combat report line of troops
# e.g. "111 Young dwarves, 222 Dwarves, 333 Soldiers."
# Return an army
# For the example above: [111, 222, 0, 0, 333, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def parse_troops(line_to_parse):
    army = [0] * 14
    units = line_to_parse.split(", ")
    for unit in units:
        for j in range(14):
            if antz_units[j][3] in unit or antz_units[j][4] in unit:
                army[j] = int(''.join(c for c in unit if c.isdigit()))
                break
    return army


# Calculate the remaining army after a fight
# Input:
#   army: e.g. [111, 222, 0, 0, 333, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   dead_troops: e.g. 200
# Output (for the example above): [0, 133, 0, 0, 333, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def get_remaining_troops(army, dead_troops):
    for i in range(14):
        if dead_troops >= army[i]:
            dead_troops -= army[i]
            army[i] = 0
        else:
            army[i] -= dead_troops
            break
    return army


# Calculate the army that died the first turn, and the life of that army without shields/dome/nest bonuses
# Input:
#   army: e.g. [50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   dead_troops: e.g. 60
# Output:
#   first_turn_dead_army: e.g. [50, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   total_life_lost: e.g. 500 (50*8 + 10*10)
def get_first_turn_dead_army(army, dead_troops):
    first_turn_dead_army = [0] * 14
    total_life_lost = 0

    for i in range(14):
        if dead_troops >= army[i]:
            first_turn_dead_army[i] = army[i]
            dead_troops -= first_turn_dead_army[i]
            total_life_lost += first_turn_dead_army[i] * antz_units[i][0]
        else:
            first_turn_dead_army[i] = dead_troops
            total_life_lost += dead_troops * antz_units[i][0]
            break

    return first_turn_dead_army, total_life_lost


# Calculate the attacker shields level
def calculate_attacker_shields():
    if defender_weapons == "?" or first_turn_defender_damages < 2200:
        print("/!\\ Defender's damages are too low to calculate Attacker's shields level")
        return "?"
    elif first_turn_defender_damages < 5000:
        print("/!\\ Defender's damages are low. Attacker's shields level might not be correct")

    first_turn_dead_army, total_life_lost = get_first_turn_dead_army(attacker_army, first_turn_attacker_dead)

    if first_turn_dead_army == attacker_army:
        print("/!\\ Attacker's army got OS, can't calculate attacker's shields level")
        return "?"
    else:
        return int((round(first_turn_defender_damages / total_life_lost, 1) - 1) * 10)


# Calculate the defender shields and dome or nest levels (depending of the place of the fight)
# Input:
#   place: Can be "Hunting Field", "Anthill" or "Nest"
# Output:
#   shields: The defender shields level
#   place_level: The defender dome or nest level, if the fight occurs in dome or nest
def calculate_defender_shields_and_place_level(place):
    if attacker_weapons == "?" or first_turn_attacker_damages < 5000:
        print("/!\\ Attacker's damages are too low to calculate Defender's shields/dome/nest level")
        return "?", "?"
    elif first_turn_attacker_damages < 10000:
        print("/!\\ Attacker's damages are low. Defender's shields/dome/nest level might not be correct")

    first_turn_dead_army, total_life_lost = get_first_turn_dead_army(defender_army, first_turn_defender_dead)

    if first_turn_dead_army == defender_army:
        print("/!\\ Defender's army got OS, can't calculate defender's shields/anthill/nest levels")
        return "?", "?"
    else:
        if place == "Hunting Field":
            return int((round(first_turn_attacker_damages / total_life_lost, 1) - 1) * 10)

        life_multiplier = round(first_turn_attacker_damages / total_life_lost, 1)
        shields = defender_weapons  # Supposition : shield == weapons, determine dome/nest level with that
        place_life_multiplier = life_multiplier - (shields / 10)
        place_level = 0
        if place == "Anthill":
            place_level = int((place_life_multiplier - 1 - 0.1) / 0.05)
        elif place == "Nest":
            place_bonus = place_life_multiplier - 1 - 0.3
            place_level = int(place_bonus / 0.15)
            modulus = round(place_bonus % 0.15, 2)
            if modulus == 0.05:
                place_level += 1
                shields -= 1
            elif modulus == 0.10:
                shields += 1

        return shields, place_level


# ********************** MAIN ********************** #

# The combat report from Antzzz
combat_report = open("combat-report.txt")

if __name__ == '__main__':

    attack_place = "?"

    attacker_army = []
    defender_army = []

    attacker_weapons = "?"
    attacker_shields = "?"
    defender_weapons = "?"
    defender_shields = "?"
    defender_dome = "?"
    defender_nest = "?"

    first_turn_attacker_damages = "?"
    first_turn_defender_damages = "?"
    first_turn_attacker_dead = 0
    first_turn_defender_dead = 0

    total_attacker_dead = 0
    total_defender_dead = 0

    turn = 1
    attacker_turn = True
    while True:
        line = combat_report.readline()
        if line == '':  # End of file
            break

        if "Hunting Field" in line:
            attack_place = "Hunting Field"
        elif "Anthill" in line:
            attack_place = "Anthill"
        elif "Nest" in line:
            attack_place = "Nest"

        elif "Attacking troops" in line:
            attacker_army = parse_troops(line.split(":")[1])
        elif "Defending troops" in line:
            defender_army = parse_troops(line.split(":")[1])

        elif "inflict" in line:
            splitted_line = line.split("(")
            second_split = splitted_line[1].split(")")
            splitted_line[1] = second_split[0]
            splitted_line.append(second_split[1])
            dead = int(''.join(c for c in splitted_line[2] if c.isdigit()))

            if attacker_turn:
                total_defender_dead += dead
            else:
                total_attacker_dead += dead
            attacker_turn = not attacker_turn

            if turn < 2:
                base_attack = int(''.join(c for c in splitted_line[0] if c.isdigit()))
                bonus_attack = int(''.join(c for c in splitted_line[1] if c.isdigit()))
                weapons = int(round(bonus_attack / base_attack, 1) * 10)
                if attacker_weapons == "?":
                    if base_attack < 10:
                        print("/!\\ Attacker's damages are too low to calculate attacker's weapons level")
                    else:
                        first_turn_attacker_damages = base_attack + bonus_attack
                        attacker_weapons = weapons
                        first_turn_defender_dead = dead
                else:
                    if base_attack < 10:
                        print("/!\\ Defender's damages are too low to calculate defender's weapons level")
                    else:
                        first_turn_defender_damages = base_attack + bonus_attack
                        defender_weapons = weapons
                        first_turn_attacker_dead = dead
            turn += 0.5

        elif line == "\n" and turn > 1:
            break

    turn = int(turn) - 1

    combat_report.close()

    attacker_shields = calculate_attacker_shields()
    if attack_place == "Hunting Field":
        defender_shields, ignore = calculate_defender_shields_and_place_level(attack_place)
    elif attack_place == "Anthill":
        defender_shields, defender_dome = calculate_defender_shields_and_place_level(attack_place)
    elif attack_place == "Nest":
        defender_shields, defender_nest = calculate_defender_shields_and_place_level(attack_place)

    # RESULTS

    print("\nFighting place: " + attack_place)
    print("Turns: " + str(int(turn)))

    print("\n# Attacker stats:")
    print("attacker_weapons = " + str(attacker_weapons))
    print("attacker_shields = " + str(attacker_shields))

    print("\n# Defender stats:")
    print("defender_weapons = " + str(defender_weapons))
    print("defender_shields = " + str(defender_shields))
    print("defender_dome = " + str(defender_dome))
    print("defender_nest = " + str(defender_nest))

    print("\n# Attacker's army:")
    print("Before:", get_readable_army(attacker_army))
    print("After (no xp!):", get_readable_army(get_remaining_troops(attacker_army, total_attacker_dead)))

    print("\n# Defender's army:")
    print("Before:", get_readable_army(defender_army))
    print("After (no xp!):", get_readable_army(get_remaining_troops(defender_army, total_defender_dead)))
