
import random
from pprint import pprint
import os
from pokeLoads import get_all_pokemons
from weaknessesRelation import relations
import copy


def clean_windows_terminal():
	input("Presiona cualquier tecla para continuar")
	os.system("cls")

def get_3_pokemons(pokemon_list):
	pokemons = []
	for a in range(3):
		pokemon_to_add = random.choice(pokemon_list)
		if pokemon_to_add not in pokemons:
			pokemons.append(copy.deepcopy(pokemon_to_add))
	return pokemons


# Used to create the player profile
def get_player_profile(pokemon_list):

	return {
		"player_name": input("Cual es tu nickname?"),
		"pokemon_inventory": get_3_pokemons(pokemon_list),
		"total_combats": 0,
		"pokeballs": 3,
		"potions": {"health": 3,
		            "dmg_amp": 3}

	}

# Used to define if the game continue or not
def any_player_pokemon_lives(player_profile):
	if len(player_profile["pokemon_inventory"]) > 0:
		return True

	elif len(player_profile["pokemon_inventory"]) == 0:
		return False

# Used to select my current pokemon on the battlefield
def choice_my_pokemon(player_profile):
	print("A cual de tus pokemons decides convocar?\n")
	choices = [" {}. {} con {} / {} HP".format(i + 1, pokemon["name"],
	                                           pokemon["current_health"], pokemon["base_health"])
	           for i, pokemon in enumerate(player_profile["pokemon_inventory"])]

	print("\n".join(choices), "\n")

	while True:
		try:
			pokemon_choice = player_profile["pokemon_inventory"][int(input("Elige un Pokemon por numero\n")) - 1]
			print("Has seleccionado a {}".format(pokemon_choice["name"]))
			clean_windows_terminal()
			break
		except (ValueError, IndexError):
			print("Opcion invalida")


	return  pokemon_choice

# Used to handle the enemy (cpu) turn
def cpu_pokemon_bot(enemy_pokemon):
	def safe_int(value):
		if isinstance(value, str) and value.isdigit():
			return int(value)
		return 0

	attack_to_use = random.choice(enemy_pokemon["attacks"])

	while (safe_int(attack_to_use["min_level"]) > int(enemy_pokemon["level"]) or safe_int(attack_to_use["damage"]) == 0) :
		attack_to_use = random.choice(enemy_pokemon["attacks"])
		return attack_to_use


# Used to handle the potion's menu and logic in battle
def potion_menu(player_profile, pokemon_in_combat, enemy_pokemon, pokemon_and_dmg_stored):
	while True:
		OPTIONS = ["Usar pocion de curacion: {} disponibles".format(player_profile["potions"]["health"]),
		           "Usar pocion de ampificacion de DMG: {} disponibles".format(player_profile["potions"]["dmg_amp"]),
		           "Regresar al menu principal"]

		for i in range(len(OPTIONS)):
			print("Opcion {}: {}. \n".format(i + 1, OPTIONS[i]))





		try:
			selected_option = int(input("Seleccione un numero para indicar la accion"))
			if 0 < selected_option < 4:
				break
			else:
				print("Opcion Invalida, intente nuevamente...\n")

		except ValueError:

			print("por favor intentalo nuevamente con un numero valido\n")


	if selected_option == 3:
		return  None, menu_handler

	elif selected_option == 2:
		if player_profile["potions"]["dmg_amp"] > 0:
			attack_multiplier = 2
			print("Los ataques de tu pokemon causaran el doble de dmg durante este combate")
			clean_windows_terminal()
			player_profile["potions"]["dmg_amp"] -= 1
			return attack_multiplier, menu_handler
		else:
			print("No te quedan pociones de amplificacion de dmg\n")
			clean_windows_terminal()
			return None, menu_handler



	elif selected_option == 1:
		if player_profile["potions"]["health"] > 0:
			pokemon_in_combat["current_health"] = pokemon_in_combat["base_health"]
			print("Tu pokemon se ha curado unos {} puntos de vida\n". format(int(pokemon_in_combat["base_health"]
			                                                                   -pokemon_in_combat["current_health"])))
			player_profile["potions"]["health"] -= 1
			return None, None
		else:
			print("No te quedan pociones de curacion\n")
			clean_windows_terminal()
			return None, menu_handler


# Used to handle the pokeball's menu and logic in battle
def pokeball_menu(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored):
	print("Seguro que deseas usar una pokeball para capturar al pokemon?\n")
	capture_chance = int((enemy_pokemon["base_health"] - enemy_pokemon["current_health"]) / enemy_pokemon["base_health"] * 100)

	while True:
		OPTIONS = ["Usar pokeball para capturar al pokemon {} con una vida de {} y una probabilidad de exito de {}%:"
		           " tienes {} actualmente".format(enemy_pokemon["name"], enemy_pokemon["current_health"],
		                                          capture_chance,player_profile["pokeballs"]),
		           "Regresar al menu principal"]

		for i in range(len(OPTIONS)):
			print("Opcion {}: {}. \n".format(i + 1, OPTIONS[i]))




		try:
			selected_option_pokeball_menu = int(input("Seleccione un numero para indicar la accion\n"))
			if 0 < selected_option_pokeball_menu <= 2:
				break

		except ValueError:

			print("por favor intentalo nuevamente con un numero valido")

	if selected_option_pokeball_menu == 2:
		menu_handler(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored)

	elif selected_option_pokeball_menu == 1:
		if player_profile["pokeballs"] > 0:
			capturar_pokemon = [1, 2]
			probabilidad_true = capture_chance/100
			probabilidad_false = 1 - probabilidad_true
			probabilidad_capturar_pokemon= [probabilidad_true, probabilidad_false ]
			resultado_captura = random.choices(capturar_pokemon, probabilidad_capturar_pokemon)

			if resultado_captura[0] == 1:
				player_profile["pokeballs"] -= 1
				pokemon_added = copy.deepcopy(enemy_pokemon)
				player_profile["pokemon_inventory"].append(pokemon_added)
				player_profile["pokemon_inventory"][-1]["current_health"] = enemy_pokemon["base_health"]
				print("El pokemon {} ha sido capturado con exito. (Pierdes una pokeball)\n".format(enemy_pokemon["name"]))
				enemy_pokemon["current_health"] = 0

			elif resultado_captura[0] == 2:
				print("Has fallado al intentar capturar el pokemon. (Pierdes una pokeball)\n")
				player_profile["pokeballs"] -= 1
		else:
			print("Ya no te quedan pokeballs para intentar capturar al pokemon\n")
			menu_handler(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored)



# Used to show the pokemon's hp
def show_pokemon_hp(actual_pokemon):
	pokemon_actual_health = actual_pokemon["current_health"]
	pokemon_base_health = actual_pokemon["base_health"]
	life_bar = "#"

	return print("{} tiene una vida de {} {} / {}\n".format(actual_pokemon["name"],
	                                                      life_bar * int(pokemon_actual_health * 10
	                                                                / pokemon_base_health),
	                                                      pokemon_actual_health,
	                                                      pokemon_base_health))


# Used to show your actual pokemon's list
def show_pokemons(player_profile):
	for i, pokemon in enumerate(player_profile["pokemon_inventory"]):
		print("Tus pokemons son {}. {} con una vida actual de {} / {} y un nivel {}\n".format(i + 1, pokemon["name"],
		                                                                        pokemon["current_health"],
		                                                                        pokemon["base_health"], pokemon["level"]), "\n")

# Used to inspect player's pokemon list and/or choice a new one to the battlefield
def inspect_my_pokemons(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored):
	show_pokemons(player_profile)

	while True:
		decision = input("Deseas intercambiar a tu pokemon actual por otro? (S/N)\n")
		if decision.upper()  in ["S" , "N"]:
			break
		else:
			print("Opcion invalida, intente nuevamente\n")



	if decision.upper() == "N":
		 return None, menu_handler

	elif decision.upper() == "S":
		print("Tus Pokemons para intercambiaqar son:\n")
		show_pokemons(player_profile)

		while True:
			try:
				selected_option = int(input("Seleccione un numero para indicar el pokemon elegido"))
				if 0 < selected_option <= len(player_profile["pokemon_inventory"]):
					return player_profile["pokemon_inventory"][selected_option - 1], None

			except ValueError:
				print("por favor intentalo nuevamente con un numero valido")




# Inspect enemy pokemon
def inspect_pokemon_in_combat(enemy_pokemon, player_profile, pokemon_in_combat, pokemon_and_dmg_stored ):
	show_pokemon_hp(enemy_pokemon)
	clean_windows_terminal()
	menu_handler(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored)

# Used to handle the main menu and battle logic on the player's turn
def menu_handler(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored, *args):
	os.system("cls")
	decision = main_combat_menu()
	if decision == 1:
		selected_pokemon_index, result_function = inspect_my_pokemons(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored)
		if selected_pokemon_index is not None:
			pokemon_selected = selected_pokemon_index
			print("Tu actual pokemon es {}\n".format(pokemon_selected["name"]))
			return pokemon_selected, 1
		elif result_function is None:
			result_function(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored, *args)

		else:
			print("No se han realizado cambios\n")

	elif decision == 2:
		inspect_pokemon_in_combat(enemy_pokemon, player_profile, pokemon_in_combat, pokemon_and_dmg_stored)

	elif decision == 3:
		my_attack, attack_multiplier = get_my_attack(pokemon_in_combat)
		if args:
			dmg_maked = make_dmg(pokemon_in_combat, enemy_pokemon, my_attack ,attack_multiplier, *args)
		else:
			dmg_maked = make_dmg(pokemon_in_combat, enemy_pokemon, my_attack, attack_multiplier,)
		save_dmg_to_convert_exp(pokemon_in_combat,dmg_maked,pokemon_and_dmg_stored)
		return None, None
	elif decision == 4:
		attack_multiplier_with_potion, result = potion_menu(player_profile, pokemon_in_combat, enemy_pokemon, pokemon_and_dmg_stored)
		if attack_multiplier_with_potion != None:
			if callable(result):
				result(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored, attack_multiplier_with_potion)
		elif attack_multiplier_with_potion == None:
			if not callable(result):
				print("tu decision ha curado a tu pokemon y como resultado acaba tu turno")
	elif decision == 5:
		pokeball_menu(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored)

# Used to make damage to the enemy pokemon ( can be used by the cpu too)
def make_dmg(current_pokemon, pokemon_injured, attack_to_use, attack_multiplier, *args):
	total_attack_to_inform = None
	attack_weakness_list =  copy.deepcopy(relations())
	pokemon_type = pokemon_injured["type"]
	for see in pokemon_type:
		attack_weakness = None
		if attack_weakness == None or attack_weakness < attack_weakness_list[attack_to_use["type"]][see]:
			attack_weakness = attack_weakness_list[attack_to_use["type"]][see]
	if args:
		arguments = args[0]
		total_attack = int(attack_to_use["damage"] * attack_multiplier * attack_weakness * arguments)
	else:
		total_attack = int(attack_to_use["damage"] * attack_multiplier * attack_weakness)

	if total_attack >= pokemon_injured["current_health"]:
		total_attack_to_inform = pokemon_injured["current_health"]
	elif total_attack < pokemon_injured["current_health"]:
		total_attack_to_inform = total_attack


	print("{} ha usado {} contra {} causando {} puntos de dmg\n\n".format(current_pokemon["name"],
	                                                                      attack_to_use["name"],
	                                                                      pokemon_injured["name"],
	                                                                      total_attack_to_inform))

	pokemon_injured["current_health"] = max(0, int(pokemon_injured["current_health"] - total_attack))
	show_pokemon_hp(pokemon_injured)

	return total_attack


def select_new_pokemon_in_combat(player_profile):
	while True:
		show_pokemons(player_profile)
		try:
			selected_option = int(input("Seleccione un numero para indicar el pokemon elegido"))
			if 0 < selected_option <= len(player_profile["pokemon_inventory"]):
				return player_profile["pokemon_inventory"][selected_option - 1]


		except ValueError:

			print("por favor intentalo nuevamente con un numero valido\n")


# Used to handle the main menu on the player's turn
def main_combat_menu():
	OPTIONS = ["Inspeccionar y Gestionar Pokemons",
	           "Inspeccionar pokemon enemigo",
	           "Realizar ataque",
	           "Usar Pociones",
	           "Usar Pokebolas"]

	for i in range(len(OPTIONS)):
		print("Opcion {}: {}. \n".format(i+1, OPTIONS[i]))


	selected_option = None


	while selected_option is None or not (1 <= selected_option <= len(OPTIONS)):

		try:
			selected_option = int(input("Seleccione un numero para indicar la accion"))

		except ValueError:
			selected_option = None

	return selected_option


def get_reward_from_combat():
	items = ["pokeball", "dmg_amp_potion", "health_potion", "exp_boost"]
	probabilities = [0.25, 0.25, 0.25, 0.25]
	return random.choices(items, probabilities)

def get_inital_battle_info(pokemon):
	return "{} | lvl {} | HP {}". format(pokemon["name"],
	                                    pokemon["level"],
	                                    pokemon["current_health"])


def get_reward(items_reward, player_profile):
	if items_reward == "pokeball":
		print("Has obtenido una pokeball\n")
		clean_windows_terminal()
		player_profile["pokeballs"] += 1

	elif items_reward == "dmg_amp_potion":
		print("Has obtenido una pocion de amplificacion de dmg\n")
		clean_windows_terminal()
		player_profile["potions"]["dmg_amp"] += 1

	elif items_reward == "health_potion":
		print("Has obtenido una pocion de curacion\n")
		clean_windows_terminal()
		player_profile["potions"]["health"] += 1

	elif items_reward == "exp_boost":
		print("Has obtenido un aumento de experiencia para todos tus pokemons\n")
		clean_windows_terminal()
		for pokemon in player_profile["pokemon_inventory"]:
			pokemon["current_exp"] += 50

def save_dmg_to_convert_exp(pokemon, dmg, pokemon_and_dmg_stored ):


	if pokemon["name"] in pokemon_and_dmg_stored:
		pokemon_and_dmg_stored[pokemon["name"]] += dmg
	else:
		pokemon_and_dmg_stored[pokemon["name"]] = dmg


##### MADE CORRECTIONS ######
def assign_exp_gained(pokemon_inventory, pokemons_used):
	for pokemon, dmg in pokemons_used.items():
		calculated_exp = calculate_exp(dmg)
		for poke in pokemon_inventory:
			if  pokemon in poke["name"]:
				print("{} ha ganado {} exp points\n".format(pokemon, calculated_exp))
			for index, pokemon_updated in enumerate(pokemon_inventory):
				if pokemon_updated["name"] == pokemon:
					pokemon_inventory[index]["current_exp"] += calculated_exp

def calculate_exp(dmg):
	return  dmg // 10


# Used to handle the individual fight (PvP )
def fight(player_profile, enemy_pokemon, pokemon_list):

	first_player = random.choice([player_profile, enemy_pokemon])
	print("Un enemigo ha aparecido\n"
	      "{} aparece desde las sombras\n". format(enemy_pokemon["name"]), "-- INICIO DEL COMBATE---\n")
	pokemon_in_combat = choice_my_pokemon(player_profile)
	enemy = get_inital_battle_info(enemy_pokemon)
	you = get_inital_battle_info(pokemon_in_combat)
	print("Contrincantes {} VS {} \n".format(you, enemy))
	print("Presione cualquier tecla para ver cual de los dos pokemons obtiene el primer turno\n")
	os.system("cls")
	pokemon_and_dmg_stored = {}
	while enemy_pokemon["current_health"] != 0 and any_player_pokemon_lives(player_profile) == True:

		if first_player == enemy_pokemon:

			print("---TURNO ENEMIGO---\n")
			attack_to_use = cpu_pokemon_bot(enemy_pokemon)
			attack_multiplier = 1
			make_dmg(enemy_pokemon, pokemon_in_combat, attack_to_use, attack_multiplier)
			print(attack_to_use)
			print("---FIN TURNO ENEMIGO---\n")
			first_player = player_profile
			clean_windows_terminal()


			if pokemon_in_combat["current_health"] == 0:
				for i , pokemon in enumerate(player_profile["pokemon_inventory"]):
					if pokemon["name"] == pokemon_in_combat["name"]:
						del player_profile["pokemon_inventory"][i]
				if any_player_pokemon_lives(player_profile) == True:
					pokemon_in_combat = select_new_pokemon_in_combat(player_profile)
			elif any_player_pokemon_lives(player_profile) == False:
				break


		else:
			print("---TU TURNO---\n", "Que deseas hacer?")
			pokemon_selected, result_function = menu_handler(player_profile, enemy_pokemon, pokemon_in_combat, pokemon_and_dmg_stored)
			if result_function == 1:
				pokemon_in_combat = pokemon_selected
			first_player = enemy_pokemon
			print("---FIN DE TU TURNO---\n")
			clean_windows_terminal()

		if enemy_pokemon["current_health"] == 0:

			items_reward = get_reward_from_combat()
			get_reward(items_reward, player_profile)
			player_profile["total_combats"] += 1
			assign_exp_gained(player_profile["pokemon_inventory"], pokemon_and_dmg_stored)
			lvl_up(player_profile["pokemon_inventory"])
			evolve(player_profile["pokemon_inventory"], pokemon_list)


def get_my_attack(my_pokemon):
	saved_attacks = []
	print("Lista de ataques disponibles\n")
	for i, attack in enumerate(my_pokemon["attacks"]):
		if attack["min_level"].isdigit():
			if int(attack["min_level"]) <= int(my_pokemon["level"]) and int(attack["damage"]) != 0 and attack["damage"] != "":
				saved_attacks.append(attack)
	for index, attack_available in enumerate(saved_attacks):
			print("Ataque {}: {} de tipo {} con un dmg base de {}\n".format( index + 1 , attack_available["name"], attack_available["type"], attack_available["damage"] ))

	while True:
		try:
			my_attack = saved_attacks[int(input("Seleccione el numero del ataque que desea usar\n")) - 1]
			break

		except (ValueError, IndexError):
			print("Seleccione un ataque valido\n")

	attack_multiplier = 1

	return my_attack, attack_multiplier

def lvl_up(pokemon_inventory):
	for pokemon in pokemon_inventory:
		if pokemon["current_exp"] > 10:
			pokemon["current_exp"] = pokemon["current_exp"] % 10
			pokemon["level"] += 1
			pokemon["current_health"] = pokemon["base_health"]


def evolve(pokemon_inventory, pokemon_list):
	for i,pokemon in enumerate(pokemon_inventory):
		if pokemon['evolution'] != "MAXIMA EVOLUCION ALCANZADA" and pokemon["level"] == pokemon["lvl_eperience_to_evolve"]:
			non_evolved_pokemon_name = pokemon["name"]
			evolved_pokemon_name = pokemon["evolution"]
			evolved_pokemon = next((poke for poke in pokemon_list if poke["name"] == evolved_pokemon_name), None)

			if evolved_pokemon:
				if pokemon["name"] == non_evolved_pokemon_name:
					pokemon_inventory[i] = evolved_pokemon


def main():

	pokemon_list = get_all_pokemons()
	pokemon_enemy_list = copy.deepcopy(pokemon_list)
	player_profile = get_player_profile(pokemon_list)

	while any_player_pokemon_lives(player_profile):
		enemy_pokemon = random.choice(pokemon_enemy_list)
		fight(player_profile, enemy_pokemon, pokemon_list)
	print("felicidades sobreviviste a {} combates ".format(player_profile["total_combats"]))


if __name__ == "__main__":
	main()