import discord
import requests
import request as r


def pokemon_types(pokemon):
    """[Returns the type(s) of the pokemon]

    Args:
        pokemon ([Json]): [A dict of the pokemon]

    Returns:
        [String]: [The types of the pokemon]
    """

    types = pokemon["types"]
    return "[" + types[0]["type"]["name"] + "]" if (len(types) == 1) \
        else "[" + types[0]["type"]["name"] + ", " + types[1]["type"]["name"] + "]"

async def get_poke(ctx, pokeID):
    return await r.getPokemon(ctx, pokeID)

async def show_poke(ctx, pokeID, show_name=True, show_type=True):
    pokemon = await r.getPokemon(ctx, pokeID)
    if pokemon == -1: return
    await embed(pokemon, ctx, show_name, show_type)


async def embed(pokemon, ctx, show_name=True, show_type=True):
    """[Displays the pokemon in discord with name, picture and types]

    Args:
        pokemon ([Json]): [A dict of the pokemon]
        ctx ([context]): [Used to send the embed]
    """
    pokemon_name = pokemon["name"]
    pokemon_url = "https://bulbapedia.bulbagarden.net/wiki/" + pokemon_name + "(Pok%C3%A9mon)"
    pokemon_description = pokemon_types(pokemon)
    pokemon_image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(pokemon["id"]) + ".png"

    embed=discord.Embed(title=pokemon_name if show_name else "", url=pokemon_url, description=pokemon_description if show_type else "", color=0xFF5733)
    embed.set_image(url=pokemon_image)
    await ctx.channel.send(embed=embed)
