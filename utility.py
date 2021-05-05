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
    """[Gets the pokemon from the api]

    Args:
        ctx ([context]): [The person sending the message]
        pokeID ([Int]): [The dex number of the pokemon]

    Returns:
        [Json]: [A dict of the info about the pokemon]
    """
    return await r.getPokemon(ctx, pokeID)


async def show_poke(ctx, pokeID, show_name=True, show_type=True):
    """[Finds the pokemon and sends it to be embeded for discord]

    Args:
        ctx ([context]): [The person sending the message]
        pokeID ([Int]): [The dex number of the pokemon]
        show_name (bool, optional): [lets the embed show the name of the pokemon]. Defaults to True.
        show_type (bool, optional): [lets the embed show the type of the pokemon]. Defaults to True.
    """
    pokemon = await r.getPokemon(ctx, pokeID)
    if pokemon == -1: return
    pokemon_name = pokemon["name"]
    pokemon_url = "https://bulbapedia.bulbagarden.net/wiki/" + pokemon_name + "_(Pok%C3%A9mon)"
    pokemon_description = pokemon_types(pokemon)
    pokemon_image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(pokemon["id"]) + ".png"

    await show(pokemon_url, pokemon_image, ctx, title=pokemon_name if show_name else "", description=pokemon_description if show_type else "")


async def show(url, img, ctx, title="", description="", color=0xFF5733):
    """[Displays the object]

    Args:
        url ([String]): [Url bound to the title]
        img ([String]): [Url of the image]
        ctx ([context]): [The person sending the message]
        title (str, optional): [Title of the image]. Defaults to "".
        description (str, optional): [description of the image]. Defaults to "".
        color ([Hex], optional): [Color of the background]. Defaults to 0xFF5733.
    """
    embed = discord.Embed(title=title, url=url, description=description, color=color)
    embed.set_image(url=img)
    await ctx.channel.send(embed=embed)



