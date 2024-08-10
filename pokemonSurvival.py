
import random
from pprint import pprint
import os
from pokeLoads import get_all_pokemons


def clean_windows_terminal():
	input("Presiona cualquier tecla para continuar")
	os.system("cls")

# Used to create the player profile
def get_player_profile(pokemon_list):

	return {
		"player_name": input("Cual es tu nickname?"),
		"pokemon_inventory": [random.choice(pokemon_list) for a in range(3)],
		"total_combats": 0,
		"pokeballs": 0,
		"potions": {"health": 0,
		            "dmg_amp": 0}

	}

# Used to define if the game continue or not
def any_player_pokemon_lives(player_profile):

	return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0

# Used to select my current pokemon on the battlefield
def choice_my_pokemon(player_profile):
	print("A cual de tus pokemons decides convocar?\n")
	choices = [" {}. {} con {} / {} HP".format(i + 1, pokemon["name"],
	                                           pokemon["current_health"], pokemon["base_health"])
	           for i, pokemon in enumerate(player_profile["pokemon_inventory"])]

	print("\n".join(choices), "\n")

	pokemon_choice = -9
	while not (0 <= pokemon_choice < len(player_profile["pokemon_inventory"])):
		try:
			pokemon_choice = int(input("Elige un Pokemon por numero\n")) - 1
		except ValueError:
			pokemon_choice = -9

	print("Has seleccionado a {}".format(player_profile["pokemon_inventory"][pokemon_choice]["name"]))
	clean_windows_terminal()
	return  player_profile["pokemon_inventory"][pokemon_choice]

# Used to handle the enemy (cpu) turn
def cpu_pokemon_bot(enemy_pokemon):
	attack_to_use = random.choice(enemy_pokemon["attacks"])
	while int(attack_to_use["min_level"]) > int(enemy_pokemon["level"]) or int(attack_to_use["damage"]) == 0 or attack_to_use["damage"] == "":
		attack_to_use = random.choice(enemy_pokemon["attacks"])
	return attack_to_use


# Used to handle the potion's menu and logic in battle
def potion_menu(player_profile, pokemon_in_combat, enemy_pokemon):
	OPTIONS = ["Usar pocion de curacion: {} disponibles".format(player_profile["potions"]["health"]),
	           "Usar pocion de ampificacion de DMG: {} disponibles".format(player_profile["potions"]["dmg_amp"]),
	           "Regresar al menu principal"]

	for i in range(len(OPTIONS)):
		print("Opcion {}: {}. \n".format(i + 1, OPTIONS[i]))

	selected_option = None

	while  selected_option is None or not (1 <= selected_option <= len(OPTIONS)):

		try:
			selected_option = int(input("Seleccione un numero para indicar la accion"))

		except ValueError:
			selected_option = None

	if selected_option == 3:
		return menu_handler(player_profile, enemy_pokemon, pokemon_in_combat)

	elif selected_option == 2:
		if player_profile["potions"]["dmg_amp"] > 0:
			attack_multiplier = 2
			print("Los ataques de tu pokemon causaran el doble de dmg durante este combate")
			clean_windows_terminal()
			player_profile["potions"]["dmg_amp"] -= 1
			return attack_multiplier
		else:
			print("No te quedan pociones de amplificacion de dmg\n")
			clean_windows_terminal()
			menu_handler(player_profile, enemy_pokemon, pokemon_in_combat)



	elif selected_option == 1:
		if player_profile["potions"]["health"] > 0:
			pokemon_in_combat["current_health"] = pokemon_in_combat["base_health"]
			print("Tu pokemon se ha curado unos {} puntos de vida\n". format(int(pokemon_in_combat["base_health"]
			                                                                   -pokemon_in_combat["current_health"])))
			player_profile["potions"]["health"] -= 1
		else:
			print("No te quedan pociones de curacion\n")
			clean_windows_terminal()
			menu_handler(player_profile, enemy_pokemon, pokemon_in_combat)


# Used to handle the pokeball's menu and logic in battle
def pokeball_menu(player_profile, enemy_pokemon, pokemon_in_combat):
	print("Seguro que deseas usar una pokeball para capturar al pokemon?\n")
	capture_chance = int((enemy_pokemon["base_health"] - enemy_pokemon["current_health"]) / enemy_pokemon["base_health"] * 100)

	OPTIONS = ["Usar pokeball para capturar al pokemon {} con una vida de {} y una probabilidad de exito de {}%:"
	           " tienes {} actualmente".format(enemy_pokemon["name"], enemy_pokemon["current_health"],
	                                          capture_chance,player_profile["pokeballs"]),
	           "Regresar al menu principal"]

	for i in range(len(OPTIONS)):
		print("Opcion {}: {}. \n".format(i + 1, OPTIONS[i]))

	selected_option = None

	while selected_option is None or not (1 <= selected_option <= len(OPTIONS)):

		try:
			selected_option = int(input("Seleccione un numero para indicar la accion\n"))

		except ValueError:
			selected_option = None

	if selected_option == 2:
		menu_handler(player_profile, enemy_pokemon, pokemon_in_combat)

	elif selected_option == 1:
		if player_profile["pokeballs"] > 0:
			capturar_pokemon = [True, False]
			probabilidad_true = capture_chance/100
			probabilidad_false = 1 - probabilidad_true
			probabilidad_capturar_pokemon= [probabilidad_true, probabilidad_false ]
			resultado_captura = random.choices(capturar_pokemon, probabilidad_capturar_pokemon)
			if resultado_captura == True:
				print("El pokemon [] ha sido capturado con exito. (Pierdes una pokeball)\n".format(enemy_pokemon["name"]))
				player_profile["pokeballs"] -= 1
				player_profile["pokemon_inventory"].append(enemy_pokemon)

			elif resultado_captura == False:
				print("Has fallado al intentar capturar el pokemon. (Pierdes una pokeball)\n")
				player_profile["pokeballs"] -= 1


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
		print("Tus pokemons son {}. {} con una vida actual de {} / {}\n".format(i + 1, pokemon["name"],
		                                                                        pokemon["current_health"],
		                                                                        pokemon["base_health"]), "\n")

# Used to inspect player's pokemon list and/or choice a new one to the battlefield
def inspect_my_pokemons(player_profile, enemy_pokemon, pokemon_in_combat):
	show_pokemons(player_profile)

	decision= None

	while decision is None or decision.upper() not in ["S" , "N"]:
		decision = input("Deseas intercambiar a tu pokemon actual por otro? (S/N)\n")

	if decision.upper() == "N":
		menu_handler(player_profile, enemy_pokemon, pokemon_in_combat)

	elif decision.upper() == "S":
		show_pokemons(player_profile)

		selected_option = None

		while selected_option is None or not (1 <= selected_option <= len(player_profile["pokemon_inventory"])):

			try:
				selected_option = int(input("Seleccione un numero para indicar la accion"))

			except ValueError:
				selected_option = None

		return selected_option


# Inspect enemy pokemon
def inspect_pokemon_in_combat(enemy_pokemon, player_profile, pokemon_in_combat ):
	show_pokemon_hp(enemy_pokemon)
	menu_handler(player_profile, enemy_pokemon, pokemon_in_combat)

# Used to handle the main menu and battle logic on the player's turn
def menu_handler(player_profile, enemy_pokemon, pokemon_in_combat):
	os.system("cls")
	decision = main_combat_menu()
	if decision == 1:
		selected_pokemon_index = inspect_my_pokemons(player_profile, enemy_pokemon, pokemon_in_combat)
		if selected_pokemon_index is not None:
			pokemon_in_combat = player_profile["pokemon_inventory"][inspect_my_pokemons(player_profile, enemy_pokemon, pokemon_in_combat  )-1]
		print("Tu actual pokemon es {}\n".format(pokemon_in_combat["name"]))
	elif decision == 2:
		inspect_pokemon_in_combat(enemy_pokemon, player_profile, pokemon_in_combat)


	elif decision == 3:
		pass
	elif decision == 4:
		potion_menu(player_profile, pokemon_in_combat, enemy_pokemon)
	elif decision == 5:
		pokeball_menu(player_profile, enemy_pokemon,pokemon_in_combat)

# Used to make damage to the enemy pokemon ( can be used by the cpu too)
def make_dmg(current_pokemon, pokemon_injured, attack_to_use, attack_multiplier):
	print("{} ha usado {} contra {} causando {} puntos de dmg\n\n".format(current_pokemon["name"],
	                                                                  attack_to_use["name"],
	                                                                  pokemon_injured["name"],
	                                                                  attack_to_use["damage"]))

	pokemon_injured["current_health"] = max(0, int (pokemon_injured["current_health"] -
	                                                attack_to_use["damage"] * attack_multiplier))
	show_pokemon_hp(pokemon_injured)


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
	print("{} | lvl {} | HP {}". format(pokemon["name"],
	                                    pokemon["level"],
	                                    pokemon["current_health"])
	      )


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

# Used to handle the individual fight (PvP )
def fight(player_profile, enemy_pokemon):
	attack_multiplier = 1
	first_player = random.choice([player_profile, enemy_pokemon])
	print("Un enemigo ha aparecido\n"
	      "{} aparece desde las sombras\n". format(enemy_pokemon["name"]), "-- INICIO DEL COMBATE---\n")
	pokemon_in_combat = choice_my_pokemon(player_profile)
	print("Contrincantes {} VS {}\n".format(get_inital_battle_info(pokemon_in_combat),
	                                      get_inital_battle_info(enemy_pokemon))
	      )
	print("Presione cualquier tecla para ver cual de los dos pokemons obtiene el primer turno\n")
	os.system("cls")

	while enemy_pokemon["current_health"] != 0 and any_player_pokemon_lives(player_profile):

		if first_player == enemy_pokemon:

			print("---TURNO ENEMIGO---\n")
			attack_to_use = cpu_pokemon_bot(enemy_pokemon)
			attack_multiplier = 1
			make_dmg(enemy_pokemon, pokemon_in_combat, attack_to_use, attack_multiplier)
			print(attack_to_use)
			print("---FIN TURNO ENEMIGO---\n")
			first_player = player_profile
			clean_windows_terminal()
		else:
			print("---TU TURNO---\n", "Que deseas hacer?")
			menu_handler(player_profile, enemy_pokemon, pokemon_in_combat)

			first_player = enemy_pokemon
			print("---FIN DE TU TURNO---\n")
			clean_windows_terminal()

		if enemy_pokemon["current_health"] == 0:

			items_reward = get_reward_from_combat()
			get_reward(items_reward, player_profile)





def main():

	pokemon_list = get_all_pokemons()
	player_profile = get_player_profile(pokemon_list)

	while any_player_pokemon_lives(player_profile):
		enemy_pokemon = random.choice(pokemon_list)
		fight(player_profile, enemy_pokemon)


if __name__ == "__main__":
	main()