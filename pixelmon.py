import pypokedex as pokedex
pokemon_types = ['normal',
       'fire',
       'water',
       'electric',
       'grass',
       'ice',
       'fighting',
       'poison',
       'ground',
       'flying',
       'psychic',
       'bug',
       'rock',
       'ghost',
       'dragon',
       'dark',
       'steel',
       'fairy',
       'typeless']

pokemon_type_indexes = {
    'normal': 0,
    'fire': 1,
    'water': 2,
    'electric': 3,
    'grass': 4,
    'ice': 5,
    'fighting': 6,
    'poison': 7,
    'ground': 8,
    'flying': 9,
    'psychic': 10,
    'bug': 11,
    'rock': 12,
    'ghost': 13,
    'dragon': 14,
    'dark': 15,
    'steel': 16,
    'fairy': 17,

    # ??? and typeless are the same thing
    'typeless': 18,
    '???': 18,
}

# defender - x-axis
# attacker - y-axis
damage_multiplication_array = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 2, 0, 1, 1, 1 / 2, 1, 1],
                               [1, 1/2, 1/2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1/2, 1, 1/2, 1, 2, 1, 1],
                               [1, 2, 1/2, 1, 1/2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1/2, 1, 1, 1, 1],
                               [1, 1, 2, 1/2, 1/2, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1/2, 1, 1, 1, 1],
                               [1, 1/2, 2, 1, 1/2, 1, 1, 1/2, 2, 1/2, 1, 1/2, 2, 1, 1/2, 1, 1/2, 1, 1],
                               [1, 1/2, 1/2, 1, 2, 1/2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1/2, 1, 1],
                               [2, 1, 1, 1, 1, 2, 1, 1/2, 1, 1/2, 1/2, 1/2, 2, 0, 1, 2, 2, 1/2, 1],
                               [1, 1, 1, 1, 2, 1, 1, 1/2, 1/2, 1, 1, 1, 1/2, 1/2, 1, 1, 0, 2, 1],
                               [1, 2, 1, 2, 1/2, 1, 1, 2, 1, 0, 1, 1/2, 2, 1, 1, 1, 2, 1, 1],
                               [1, 1, 1, 1/2, 2, 1, 2, 1, 1, 1, 1, 2, 1/2, 1, 1, 1, 1/2, 1, 1],
                               [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1/2, 1, 1, 1, 1, 0, 1/2, 1, 1],
                               [1, 1/2, 1, 1, 2, 1, 1/2, 1/2, 1, 1/2, 2, 1, 1, 1/2, 1, 2, 1/2, 1/2, 1],
                               [1, 2, 1, 1, 1, 2, 1/2, 1, 1/2, 2, 1, 2, 1, 1, 1, 1, 1/2, 1, 1],
                               [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1/2, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1/2, 0, 1],
                               [1, 1, 1, 1, 1, 1, 1/2, 1, 1, 1, 2, 1, 1, 2, 1, 1/2, 1, 1/2, 1],
                               [1, 1/2, 1/2, 1/2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1/2, 2, 1],
                               [1, 1/2, 1, 1, 1, 1, 2, 1/2, 1, 1, 1, 1, 1, 1, 2, 2, 1/2, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

def pokemon(pokemon_name):
    pokemon_name = pokemon_name.lower().strip().replace(" ", "-")
    print(pokemon_name)
    return pokedex.get(name=pokemon_name)

def types_of_pokemon(name):
    return pokemon(name).types

def damage_multipliers_of_types(pokemon_type_1, pokemon_type_2="typeless"):
    x1 = pokemon_type_indexes[pokemon_type_1]
    x2 = pokemon_type_indexes[pokemon_type_2]
    damage_multipliers_array = []
    for defenders in damage_multiplication_array:
        damage_multipliers_array.append(defenders[x1] * defenders[x2])

    damage_multipliers_dict = {
        4: [],
        2: [],
        1: [],
        0.5: [],
        0.25: [],
        0: [],
    }
    for attacker_index, multiplier in enumerate(damage_multipliers_array[:-1]):
        damage_multipliers_dict[multiplier].append(pokemon_types[attacker_index])
    damage_multipliers_dict.pop(1)
    damage_multipliers_dict = {key: value for key, value in damage_multipliers_dict.items() if value != []}

    return damage_multipliers_dict

def damage_multipliers_of_pokemon(pokemon_name):
    return damage_multipliers_of_types(*types_of_pokemon(pokemon_name)).items()

print(damage_multipliers_of_pokemon("Flutter Mane"))