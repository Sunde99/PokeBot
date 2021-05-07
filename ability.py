import utility
import requests

async def possible_abilities(ctx, pokeID):
    """[Look up all possible abilities for a pokemon]

    Args:
        ctx ([context]): [The person sending the message]
        pokeID ([Int]): [The dex number of the pokemon]

    Returns:
        [List]: [A list of the possible abilities]
    """
    abilities = []
    ability_list = utility.get_poke(ctx, pokeID)["abilities"]
    for ability in ability_list:
        abilities.append(ability["name"])
    return abilities

async def ability_lookup(ctx, ability):
    """[Look up the effect of an ability]

    Args:
        ctx ([context]): [The person sending the message]
        ability ([String]): [The ability to look up]

    Returns:
        [String]: [The effect of the ability]
    """
    ability = abliity.strip().replace(" ", "-")
    ability_info = requests.getAbility(ctx, ability)
    ability_effect = "This error shouldn't appear"
    effect_entries = ability_info["effect_entries"]

    for entry in effect_entries:
        if (entry["language"]["name"] == "en"):
            ability_effect = entry["effect"]
    
    return ability_effect
