import discord
import pymongo
import requests
from pymongo import MongoClient

import databaseConnection as db
import pokeInfo as info
import whosThatPokemon as who

connection_url = open("connection_url.txt", "r").read()
cluster = MongoClient(connection_url)

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
        await who.quiz(ctx, client, cluster)
    elif await mode(message) == "points":
        await db.showPoints(ctx, cluster)
    else:
        pokemon = message.split(" ", 1)[1]
        await info.show_poke(ctx, pokemon)

client.run(token)
