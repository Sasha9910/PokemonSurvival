

import pickle
from requests_html import HTMLSession
from srtFilesForPokeLoads import *





name_lvl_list = [(0,0)]
name_lvl_tuple = ()

pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level" : 1,
    "type" : "",
    "current_exp" : 0,
    "evolution" : "",
    "lvl_eperience_to_evolve" : "",
    "attacks" : [ ],
    "weaknesses" : []

}


def get_images_with_src_prefix(pokemon_page, src_prefix_for_type):


    imgs = pokemon_page.html.find("img")
    filtered_img = []
    for img in imgs:
        src_value = img.attrs.get("src", "")
        if src_value.startswith(src_prefix_for_type) and  src_value[len(src_prefix_for_type): -4] not in filtered_img:
            filtered_img.append(src_value[len(src_prefix_for_type): -4])

    return filtered_img



def get_pokemon_evolution(pokemon_page, index):


    evolutions = []
    center_elements = pokemon_page.html.find("table.center")
    nav5c_elements = center_elements[0].find("a.nav5c")
    for nav5c_element in nav5c_elements:
        href_value = nav5c_element.attrs.get("href", "")
        if href_value.startswith(HREF_PREFIX_FOR_EVOLUTION):
            evolution = nav5c_element.text.split()
            if evolution and int(evolution[0]) > index:
                evolution_names = "".join(evolution[1:])
                evolutions.append(evolution_names)

    return (evolutions)

def resolve_non_evolution_avaiable(pokemon):


    if not isinstance(pokemon, str) and len(pokemon) == 0:
        pokemon = "Sin evolucion disponible"

    return pokemon


def contain_prohibited_words(string, prohibited_words):


    words = string.split()
    for word in words:
        if word in prohibited_words:
            return True

    return False

def get_lvl_to_evolve(pokemon_page, SPECIFIC_SRT_TO_DETECT_LVL_TO_EVOLVE):


    lvls_to_evolve = []
    nowraps_elements  = pokemon_page.html.find('td[style="display: normal;"][nowrap]')

    if not nowraps_elements:
        return lvls_to_evolve

    nowrap_elemnt = nowraps_elements[0].text.split("\n")

    for nowrap in nowrap_elemnt:

        if (SPECIFIC_SRT_TO_DETECT_LVL_TO_EVOLVE in nowrap and
                contain_prohibited_words( nowrap, PROHIBITED_WORDS_INTO_SRT_LVL_TO_EVOLVE) == False):
            lvls_to_evolve.append(nowrap)



    return lvls_to_evolve

def resolve_non_exp_to_evolve(exp_to_evolve):


    if exp_to_evolve == "Sin evolucion disponible":
        return "MAXIMA EVOLUCION ALCANZADA"

def one_evolution_remaining(pokemon_evolutions, exp_to_evolve):


    if len(pokemon_evolutions) == 1:
        if len(exp_to_evolve) == 2:
            return pokemon_evolutions[0], exp_to_evolve[1]

        elif len(exp_to_evolve) == 1:
            return pokemon_evolutions[0], exp_to_evolve[0]

    return None, None

def two_evolutions_remaining(pokemon_evolutions, exp_to_evolve):


    if len(pokemon_evolutions) == 2 and len(exp_to_evolve) == 2:
        return pokemon_evolutions[0], exp_to_evolve[0]

    return None, None



def pair_evolve_lvl_with_evolution(evolutions, exp_needed):


    msg = resolve_non_exp_to_evolve(evolutions)
    if msg == "MAXIMA EVOLUCION ALCANZADA":
        return evolutions , msg
    else:
        evo1, exp1 = one_evolution_remaining(evolutions,exp_needed)
        if evo1 != None:
            return (evo1, exp1)
        else:
            evo2, exp2 = two_evolutions_remaining(evolutions,exp_needed)
            return (evo2, exp2)

def get_attacks_elements(URL_ATTACKS ,index):


    url = "{}{}".format(URL_ATTACKS, index)
    session = HTMLSession()
    pokemon_page = session.get(url)
    attacks = []

    for attacks_elements in pokemon_page.html.find(".pkmain")[-1].find("tr.check3"):
        attack = {
            "name": attacks_elements.find("td", first=True).find("a", first=True ).text,
            "type": attacks_elements.find("td")[1].find("img", first = True).attrs["alt"] ,
            "min_level": attacks_elements.find("th", first=True).text.replace(" ", "1"),
            "damage": int(attacks_elements.find("td")[3].text.replace("--", "0"))

        }
        attacks.append(attack)

    return attacks

def assign_lvl_to_pokemon(actual_exp, exp_needed ,index):


    if index == 1:
        return 1, exp_needed

    elif exp_needed =="MAXIMA EVOLUCION ALCANZADA":
        next_pokemon_lvl= 1
        return actual_exp,next_pokemon_lvl
    else:
        return actual_exp, exp_needed


def get_pokemon(index, name_lvl_list, name_lvl_tuple):


    url = "{}{}".format(URL_BASE, index)
    new_pokemon = pokemon_base.copy()
    session = HTMLSession()
    pokemon_page = session.get(url)
    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text.split("\n")[0]

    for list in name_lvl_list:
        if new_pokemon['name'] == list[0]:
            lvl = list[1]
            new_pokemon["level"] = int (lvl.split(" ")[1])
        name_lvl_list.remove(list)


    new_pokemon['type'] = get_images_with_src_prefix(pokemon_page, SRC_PREFIX_FOR_TYPE)
    new_pokemon['evolution'] = resolve_non_evolution_avaiable( get_pokemon_evolution(pokemon_page, index,))
    new_pokemon['lvl_eperience_to_evolve'] =  get_lvl_to_evolve(pokemon_page,
                                                               SPECIFIC_SRT_TO_DETECT_LVL_TO_EVOLVE,
                                                               )


    new_pokemon['evolution'], new_pokemon['lvl_eperience_to_evolve'] =\
        pair_evolve_lvl_with_evolution( new_pokemon['evolution'], new_pokemon['lvl_eperience_to_evolve'] )
    name_lvl_tuple = (  new_pokemon['evolution'] , new_pokemon['lvl_eperience_to_evolve'] )
    name_lvl_list.append(name_lvl_tuple)


    new_pokemon["attacks"] = (get_attacks_elements(URL_ATTACK_PAGE, index))
    if new_pokemon["level"] > 1:
        new_pokemon["base_health"] = 100 + (5 * new_pokemon["level"] )
    new_pokemon["current_health"] = new_pokemon["base_health"]

    return new_pokemon


def get_all_pokemons():


    all_pokemons = []


    try:
        print("Cargando archivo de pokemons")
        with open ("pokefile.pkl", "rb") as pokerfile:
            all_pokemons = pickle.load(pokerfile)
        print("Lista de pokemons cargada\n")

    except FileNotFoundError:
        print("Archivo de pokemons no encontrado \n")
        for pokemon in range(151):
            all_pokemons.append(get_pokemon(pokemon + 1, name_lvl_list, name_lvl_tuple))
            print("*", end="")
            print(all_pokemons[pokemon]["name"])

        with open ("pokefile.pkl", "wb") as pokerfile:
            pickle.dump(all_pokemons, pokerfile)
            print("\n !Todos los pokemons han sido descargados!\n")

    return all_pokemons








