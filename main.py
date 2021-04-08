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

    command = await mode(message)
    if command == "quiz":
        await who.quiz(ctx, client, cluster)
    elif command == "points":
        await db.showPoints(ctx, cluster)
    elif command == "reset":
        def areYouSure(m):
            print(m.content)
            return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "y" or m.content.lower() == "n")
        await ctx.channel.send("Are you sure you want to reset your points? y/n")

        try:
            msg = await client.wait_for('message', check=areYouSure, timeout=8.0)
            print(msg.content)
            
            if (msg.content == "y"): 
                await db.resetPoints(ctx, cluster)
                await ctx.channel.send("{.name}'s points have been reset".format(msg.author))
            else: await ctx.channel.send("{.name}'s points have not been reset".format(msg.author))
        except:
            await ctx.channel.send("Your points did not get reset")
    else:
        pokemon = message.split(" ", 1)[1]
        await info.show_poke(ctx, pokemon)

client.run(token)
