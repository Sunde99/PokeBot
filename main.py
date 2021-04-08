import discord
import requests
import whosThatPokemon as who
import pokeInfo as info

token = open("token.txt", "r").read()
client = discord.Client()

async def mode(msg):
    return msg.split(" ", 1)[1].lower()

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
    print(message)

    if await mode(message) == "quiz":
        await who.quiz(ctx)
    else:
        pokemon = message.split(" ", 1)[1]
        await info.show_poke(ctx, pokemon)

client.run(token)
