import requests

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

async def getItem(ctx, item):
    url = "https://pokeapi.co/api/v2/item/" + item
    if not check_status(url):
        await ctx.channel.send("something went wrong")
        return -1
    
    return requests.get(url).json()


async def getPokemon(ctx, pokeID):
    """[Gets the pokemon from the api]

    Args:
        ctx ([context]): [The person sending the message]
        pokeID ([Int]): [The dex number of the pokemon]

    Returns:
        [Json]: [A dict of the info about the pokemon]
    """
    url = "https://pokeapi.co/api/v2/pokemon/" + str(pokeID)
    print(url)
    if not check_status(url):
        await ctx.channel.send("something went wrong")
        return -1

    pokemon = requests.get(url).json()
    return pokemon

    # await ctx.channel.send(pokemon["name"])