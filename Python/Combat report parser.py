import io


# **************** GLOBAL VARIABLES **************** #

young_dwarves = [8, 3, 2, "Young dwarves", "Young dwarf", "Jeunes Soldates Naines", "Jeune Soldate Naine"]
dwarves = [10, 5, 4, "Dwarves", "Dwarf", "Soldates Naines", "Soldate Naine"]
top_dwarves = [13, 7, 6, "Top dwarves", "Top dwarf", "Naines d'Elites", "Naine d'Elite"]
young_soldiers = [16, 10, 9, "Young soldiers", "Young soldier", "Jeunes Soldates", "Jeune Soldate"]
soldiers = [20, 15, 14, "Soldiers", "Soldier", "Soldates", "Soldate"]
doorkeepers = [30, 1, 25, "Doorkeepers", "Doorkeeper", "Concierges", "Concierge"]
top_doorkeepers = [40, 1, 35, "Top doorkeepers", "Top doorkeeper", "Concierges d'Elites", "Concierge d'Elite"]
fire_ants = [10, 30, 15, "Fire ants", "Fire ant", "Artilleuses", "Artilleuse"]
top_fire_ants = [12, 35, 18, "Top fire ants", "Top fire ant", "Artilleuses d'Elites", "Artilleuse d'Elite"]
top_soldiers = [27, 24, 23, "Top soldiers", "Top soldier", "Soldates d'Elites", "Soldate d'Elite"]
tanks = [35, 55, 1, "Tanks", "Tank", "Tanks", "Tank"]
top_tanks = [50, 80, 1, "Top tanks", "Top tanks", "Tanks d'Elites", "Tank d'Elite"]
killers = [50, 50, 50, "Killers", "Killer", "Tueuses", "Tueuse"]
top_killers = [55, 55, 55, "Top killers", "Top killer", "Tueuses d'Elites", "Tueuse d'Elite"]

antz_units = [young_dwarves, dwarves, top_dwarves, young_soldiers, soldiers, doorkeepers, top_doorkeepers,
              fire_ants, top_fire_ants, top_soldiers, tanks, top_tanks, killers, top_killers]


# ******************* FUNCTIONS ******************** #

# Get a formatted string version of a big number
# e.g. format_number(12345678) will return "12 345 678"
# e.g. format_number(1234.3) will return "1 234"
# e.g. format_number("?") will return "?"
def format_number(number):
    try:
        number = int(round(float(number)))
    except ValueError:
        return "?"
    return '{:,}'.format(number).replace(',', ' ')


# Take an army
# e.g. [111, 222, 0, 0, 333, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Return it as it would be in Antzzz
# For the example above: "111 Young dwarves, 222 Dwarves, 333 Soldiers."
def get_readable_army(army):
    first = True
    readable_army = ""
    offset = 0
    if not is_english:
        offset = 2
    for i in range(14):
        if army[i] > 0:
            if not first:
                readable_army += ", "
            first = False
            if army[i] == 1:
                readable_army += format_number(army[i]) + " " + antz_units[i][4 + offset]
            else:
                readable_army += format_number(army[i]) + " " + antz_units[i][3 + offset]
    if first:
        if is_english:
            readable_army += "None"
        else:
            readable_army += "Aucune"
    return readable_army + "."


# Take a combat report line of troops
# e.g. "111 Young dwarves, 222 Dwarves, 333 Soldiers."
# Return an army
# For the example above: [111, 222, 0, 0, 333, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def parse_troops(line_to_parse):
    army = [0] * 14
    units = line_to_parse.split(", ")
    units[-1] = units[-1].split(".")[0]
    offset = 0
    if not is_english:
        offset = 2
    for unit in units:
        for j in range(14):
            unit = unit.replace("’", "'").replace("é", "E")
            if unit.endswith(antz_units[j][3 + offset]) or unit.endswith(antz_units[j][4 + offset]):
                army[j] = int(''.join(c for c in unit if c.isdigit()))
                break
    return army


# Calculate the remaining army after a fight
# Input:
#   army: e.g. [111, 222, 0, 0, 333, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   dead_troops: e.g. 200
# Output (for the example above): [0, 133, 0, 0, 333, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def get_remaining_troops(army, dead_troops):
    remaining_army = [0] * 14
    for i in range(14):
        remaining_army[i] = army[i]
        if dead_troops > army[i]:
            dead_troops -= army[i]
            remaining_army[i] = 0
        else:
            remaining_army[i] -= dead_troops
            dead_troops = 0
    return remaining_army


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
        if is_english:
            print("/!\\ Defender's damages are too low (<2000) to calculate attacker's Shields level")
        else:
            print("/!\\ Les dégâts du défenseur sont trop faibles (<2000) pour calculer le niveau de Boucliers de "
                  "l'attaquant")
        return "?"
    elif first_turn_defender_damages < 5000:
        if is_english:
            print("/!\\ Defender's damages are low (<5000). Attacker's Shields level might not be correct")
        else:
            print("/!\\ Les dégâts du défenseur sont faibles (<5000). Le niveau de Boucliers de l'attaquant pourrait "
                  "ne pas être correct")

    first_turn_dead_army, total_life_lost = get_first_turn_dead_army(attacker_army, first_turn_attacker_dead)

    if first_turn_dead_army == attacker_army:
        if is_english:
            print("/!\\ Attacker's army got OS, can't calculate attacker's Shields level")
        else:
            print("/!\\ L'armée de l'attaquant a été tuée en 1 tour, il n'est donc pas possible de calculer le niveau "
                  "de Boucliers de l'attaquant")
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
        if is_english:
            print("/!\\ Attacker's damages are too low (<5000) to calculate defender's Shields/Dome/Nest levels")
        else:
            print("/!\\ Les dégâts de l'attaquant sont trop faibles (<5000) pour calculer les niveaux de "
                  "Boucliers/Dôme/Loge de défenseur")
        return "?", "?"
    elif first_turn_attacker_damages < 10000:
        if is_english:
            print("/!\\ Attacker's damages are low (<10,000). Defender's Shields/Dome/Nest levels might not be correct")
        else:
            print("/!\\ Les dégâts de l'attaquant sont faibles (<10 000). Les niveaux de Boucliers/Dôme/Loge du "
                  "défenseur pourraient ne pas être corrects")

    first_turn_dead_army, total_life_lost = get_first_turn_dead_army(defender_army, first_turn_defender_dead)

    if first_turn_dead_army == defender_army:
        if is_english:
            print("/!\\ Defender's army got OS, can't calculate defender's Shields/Dome/Nest levels")
        else:
            print("/!\\ L'armée du défenseur a été tuée en 1 tour, il n'est donc pas possible de calculer les niveaux "
                  "de Boucliers/Dôme/Loge du défenseur")
        return "?", "?"
    else:
        if place == "Hunting Field":
            return int((round(first_turn_attacker_damages / total_life_lost, 1) - 1) * 10)

        # Double round is needed for cases like "round(4.4499, 1) = 4.4" where we want 4.5
        life_multiplier = round(first_turn_attacker_damages / total_life_lost, 2)
        shields = defender_weapons  # Supposition : shield == weapons, determine dome/nest level with that
        place_life_multiplier = life_multiplier - (shields / 10)
        place_level = 0
        if place == "Anthill":
            place_level = int(round((place_life_multiplier - 1 - 0.1) / 0.05))
        elif place == "Nest":
            place_bonus = place_life_multiplier - 1 - 0.3
            place_level = int(round(place_bonus / 0.15, 2))
            modulus = round(place_bonus % 0.15, 2)
            if modulus == 0.05:
                place_level += 1
                shields -= 1
            elif modulus == 0.10:
                shields += 1

        return shields, place_level


# Calculate the stats of an army
# Input:
#   army: e.g. [50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#   weapons, shields, dome, nest: e.g. 23, 23, "?", 27
# Output:
#   [attack, defense, hf_life, anthill_life, nest_life]
#   e.g. [1320, 990, 2970, "?", 6885]
def calculate_army_stats(army, weapons, shields, dome, nest):
    attack, defense, hf_life, anthill_life, nest_life = 0, 0, 0, 0, 0
    damage_multiplier, hf_life_multiplier, anthill_life_multiplier, nest_life_multiplier = 0, 0, 0, 0

    if weapons != "?":
        damage_multiplier = (weapons/10 + 1)
    else:
        attack, defense = "?", "?"
    if shields != "?":
        hf_life_multiplier = (shields/10 + 1)
        if dome != "?":
            anthill_life_multiplier = hf_life_multiplier + 0.1 + (dome * 0.05)
        else:
            anthill_life = "?"
        if nest != "?":
            nest_life_multiplier = hf_life_multiplier + 0.3 + (nest * 0.15)
        else:
            nest_life = "?"
    else:
        hf_life, anthill_life, nest_life = "?", "?", "?"

    for i in range(14):
        if weapons != "?":
            attack += army[i] * antz_units[i][1] * damage_multiplier
            defense += army[i] * antz_units[i][2] * damage_multiplier
        if shields != "?":
            hf_life += army[i] * antz_units[i][0] * hf_life_multiplier
            if dome != "?":
                anthill_life += army[i] * antz_units[i][0] * anthill_life_multiplier
            if nest != "?":
                nest_life += army[i] * antz_units[i][0] * nest_life_multiplier

    return [attack, defense, hf_life, anthill_life, nest_life]


# ********************** MAIN ********************** #

# The combat report from Antzzz
combat_report = io.open("combat-report.txt", mode="r", encoding="utf-8")
is_english = True

if __name__ == '__main__':

    attack_place = ["?", "?"]

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
            attack_place = ["Hunting Field", "Terrain de Chasse"]
        elif "Terrain de Chasse" in line:
            attack_place = ["Hunting Field", "Terrain de Chasse"]
            is_english = False
        elif "Anthill" in line:
            attack_place = ["Anthill", "fourmilière"]
        elif "fourmilière" in line:
            attack_place = ["Anthill", "fourmilière"]
            is_english = False
        elif "Nest" in line:
            attack_place = ["Nest", "Loge Impériale"]
        elif "Loge Impériale" in line:
            attack_place = ["Nest", "Loge Impériale"]
            is_english = False

        elif "Attacking troops" in line or "Troupes en attaque" in line:
            attacker_army = parse_troops(line.split(":")[1])
        elif "Defending troops" in line or "Troupes en défense" in line:
            defender_army = parse_troops(line.split(":")[1])

        elif "inflict" in line or "inflige" in line:
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
                weapons_lvl = int(round(bonus_attack / base_attack, 1) * 10)
                if attacker_weapons == "?":
                    if base_attack < 10:
                        if is_english:
                            print("/!\\ Attacker's base damages are too low (<10) to calculate attacker's Weapons level")
                        else:
                            print("/!\\ Les dégâts de base de l'attaquant sont trop faibles (<10) pour calculer le "
                                  "niveau d'Armes de l'attaquant")
                    else:
                        first_turn_attacker_damages = base_attack + bonus_attack
                        attacker_weapons = weapons_lvl
                        first_turn_defender_dead = dead
                else:
                    if base_attack < 10:
                        if is_english:
                            print(
                                "/!\\ Defender's base damages are too low (<10) to calculate defender's weapons level")
                        else:
                            print("/!\\ Les dégâts de base du défenseur sont trop faibles (<10) pour calculer le "
                                  "niveau d'Armes du défenseur")
                    else:
                        first_turn_defender_damages = base_attack + bonus_attack
                        defender_weapons = weapons_lvl
                        first_turn_attacker_dead = dead
            turn += 0.5

        elif line == "\n" and turn > 1:
            break

    turn = int(turn) - 1

    combat_report.close()

    attacker_shields = calculate_attacker_shields()
    if attack_place[0] == "Hunting Field":
        defender_shields, ignore = calculate_defender_shields_and_place_level(attack_place[0])
    elif attack_place[0] == "Anthill":
        defender_shields, defender_dome = calculate_defender_shields_and_place_level(attack_place[0])
    elif attack_place[0] == "Nest":
        defender_shields, defender_nest = calculate_defender_shields_and_place_level(attack_place[0])

    attacker_surviving_army = get_remaining_troops(attacker_army, total_attacker_dead)
    defender_surviving_army = get_remaining_troops(defender_army, total_defender_dead)

    attacker_surviving_troops = get_readable_army(attacker_surviving_army)
    defender_surviving_troops = get_readable_army(defender_surviving_army)

    attacker_surviving_army_stats = calculate_army_stats(attacker_surviving_army, attacker_weapons, attacker_shields,
                                                         "?", "?")
    defender_surviving_army_stats = calculate_army_stats(defender_surviving_army, defender_weapons, defender_shields,
                                                         defender_dome, defender_nest)

    # RESULTS

    if is_english:
        print("\nFighting place: " + attack_place[0])
        print("Turns: " + str(int(turn)))

        print("\n# Attacker stats:")
        print("Weapons = " + str(attacker_weapons))
        print("Shields = " + str(attacker_shields))

        print("\n# Defender stats:")
        print("Weapons = " + str(defender_weapons))
        hf_warning, dome_warning, nest_warning = "", "", ""
        if defender_shields != "?":
            if defender_dome != "?":
                hf_warning = " (might be off: see dome/nest warning(s) to know more)"
                dome_warning = " (might be off: +1 Shields = -2 Dome, and vice versa)"
            if defender_nest != "?":
                hf_warning = " (might be off: see dome/nest warning(s) to know more)"
                nest_warning = " (might be off: +3 Shields = -2 Nest, and vice versa)"
        print("Shields = " + str(defender_shields) + hf_warning)
        print("Dome = " + str(defender_dome) + dome_warning)
        print("Nest = " + str(defender_nest) + nest_warning)

        print("\n# Attacker's army:")
        print("Before:", get_readable_army(attacker_army))
        print("After (no xp!):", attacker_surviving_troops)

        if attacker_surviving_troops != "None.":
            print("\n# Attacker army stats after (no xp!):")
            print("Attack:", format_number(attacker_surviving_army_stats[0]))
            print("Defense:", format_number(attacker_surviving_army_stats[1]))
            print("HF life:", format_number(attacker_surviving_army_stats[2]))

        print("\n# Defender's army:")
        print("Before:", get_readable_army(defender_army))
        print("After (no xp!):", defender_surviving_troops)

        if defender_surviving_troops != "None.":
            print("\n# Defender army stats after (no xp!):")
            print("Attack:", format_number(defender_surviving_army_stats[0]))
            print("Defense:", format_number(defender_surviving_army_stats[1]))
            print("HF life:", format_number(defender_surviving_army_stats[2]) + hf_warning)
            print("Anthill life:", format_number(defender_surviving_army_stats[3]) + dome_warning)
            print("Nest life:", format_number(defender_surviving_army_stats[4]) + nest_warning)

    else:
        print("\nLieu du combat: " + attack_place[1])
        print("Tours: " + str(int(turn)))

        print("\n# Stats de l'attaquant:")
        print("Armes = " + str(attacker_weapons))
        print("Boucliers = " + str(attacker_shields))

        print("\n# Stats du défenseur:")
        print("Armes = " + str(defender_weapons))
        hf_warning, dome_warning, nest_warning = "", "", ""
        if defender_shields != "?":
            if defender_dome != "?":
                hf_warning = " (peut être imprécis : voir le(s) avertissement(s) lié(s) au Dôme/à la Loge Impériale " \
                             "pour en savoir plus) "
                dome_warning = " (peut être imprécis : +1 Boucliers = -2 Dôme, et vice versa)"
            if defender_nest != "?":
                hf_warning = " (peut être imprécis : voir le(s) avertissement(s) lié(s) au Dôme/à la Loge Impériale " \
                             "pour en savoir plus) "
                nest_warning = " (peut être imprécis : +3 Boucliers = -2 Loge Impériale, et vice versa)"
        print("Boucliers = " + str(defender_shields) + hf_warning)
        print("Dôme = " + str(defender_dome) + dome_warning)
        print("Loge = " + str(defender_nest) + nest_warning)

        print("\n# Armée de l'attaquant:")
        print("Avant:", get_readable_army(attacker_army))
        print("Après (sans xp !):", attacker_surviving_troops)

        if attacker_surviving_troops != "Aucune.":
            print("\n# Stats de l'armée en attaque après le combat (sans xp !):")
            print("Attaque:", format_number(attacker_surviving_army_stats[0]))
            print("Défense:", format_number(attacker_surviving_army_stats[1]))
            print("Vie TdC:", format_number(attacker_surviving_army_stats[2]))

        print("\n# Armée du défenseur:")
        print("Avant:", get_readable_army(defender_army))
        print("Après (sans xp !):", defender_surviving_troops)

        if defender_surviving_troops != "Aucune.":
            print("\n# Stats de l'armée en défense après le combat (sans xp !):")
            print("Attaque:", format_number(defender_surviving_army_stats[0]))
            print("Défense:", format_number(defender_surviving_army_stats[1]))
            print("Vie TdC:", format_number(defender_surviving_army_stats[2]) + hf_warning)
            print("Vie Dôme:", format_number(defender_surviving_army_stats[3]) + dome_warning)
            print("Vie Loge Impériale:", format_number(defender_surviving_army_stats[4]) + nest_warning)
