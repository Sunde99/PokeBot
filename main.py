import discord
import requests

token = open("token.txt", "r").read()
client = discord.Client()

def poke(msg):
    """[Gets the name of the pokemon from the message]

    Args:
        msg ([context]): [The message]

    Returns:
        [String]: [The pokemon]
    """
    pokemon = msg.split(" ", 1)[1]
    return pokemon

def check_status(url):
    """[Only lets valid requests pass]

    Args:
        url ([String]): [The url to be requested]

    Returns:
        [Bool]: [Whether the url is valid or not]
    """
    request_status = requests.get(url).status_code
    print(request_status)
    if request_status != 200:
        return False
    return True

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

async def embed(pokemon, ctx):
    """[Displays the pokemon in discord with name, picture and types]

    Args:
        pokemon ([Json]): [A dict of the pokemon]
        ctx ([context]): [Used to send the embed]
    """
    pokemon_name = pokemon["name"]
    pokemon_url = "https://bulbapedia.bulbagarden.net/wiki/" + pokemon_name + "(Pok%C3%A9mon)"
    pokemon_description = pokemon_name + " is a \n" + pokemon_types(pokemon) + " type."
    pokemon_image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(pokemon["id"]) + ".png"

    embed=discord.Embed(title=pokemon_name, url=pokemon_url, description=pokemon_description, color=0xFF5733)
    embed.set_image(url=pokemon_image)
    await ctx.channel.send(embed=embed)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    message = ctx.content

    if not message.lower().startswith("pokemon"):
        return

    url = "https://pokeapi.co/api/v2/pokemon/" + poke(message)
    print(url)
    if not check_status(url):
        await ctx.channel.send("something went wrong")
        return

    pokemon = requests.get(url).json()
    await ctx.channel.send(pokemon["name"])

    await embed(pokemon, ctx)

client.run(token)
