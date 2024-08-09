import random
from pprint import pprint

from pokeLoads import get_all_pokemons


def get_player_profile(pokemon_list):

	return {
		"player_name" : input("Cual es tu nickname?"),
		"pokemon_inventory" : [random.choice(pokemon_list) for a in range(3)],
		"total_combats" : 0,
		"pokeballs" : 0,
		"health_potion" : 0

	}

def any_player_pokemon_lives(player_profile):
	return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0

def choice_my_pokemon(player_profile):
	print("A cual de tus pokemons decides convocar?\n")
	choices = [" {}. {}".format(i + 1, pokemon["name"]) for i, pokemon in enumerate(player_profile["pokemon_inventory"]) ]
	print("\n".join(choices), "\n")

	pokemon_choice = -9
	while not (0 <= pokemon_choice < len(player_profile["pokemon_inventory"])):
		try:
			pokemon_choice = int(input("Elige un Pokemon por numero\n")) - 1
		except ValueError:
			pokemon_choice = -9

	print("Has seleccionado a {}".format(player_profile["pokemon_inventory"][pokemon_choice]["name"]))
	return  player_profile["pokemon_inventory"][pokemon_choice]




def fight(player_profile, enemy_pokemon):
	first_player = random.choice([player_profile, enemy_pokemon])
	print("Un enemigo ha aparecido\n"
	      "{} aparece desde las sombras\n". format(enemy_pokemon["name"]))
	pokemon_in_combat = choice_my_pokemon(player_profile)

	while enemy_pokemon["current_health"] != 0  and  any_player_pokemon_lives(player_profile):
		if first_player == enemy_pokemon:
			




def main():

	pokemon_list = get_all_pokemons()
	player_profile = get_player_profile(pokemon_list)

	while any_player_pokemon_lives(player_profile):
		enemy_pokemon = random.choice(pokemon_list)
		fight(player_profile, enemy_pokemon)


if __name__ == "__main__":
	main()