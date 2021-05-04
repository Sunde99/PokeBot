import discord
import pymongo
import requests
import random
import asyncio
from pymongo import MongoClient

import databaseConnection as db
import pokeInfo as info
import whosThatPokemon as who
import spawnPokemon as spawn

connection_url = open("connection_url.txt", "r").read()
cluster = MongoClient(connection_url)
pokebotCluster = cluster["Pokebot"]


token = open("token.txt", "r").read()
client = discord.Client()



async def mode(msg):
    return msg.split(" ", 1)[1].lower()

async def parser(ctx, command, message):
    if command == "quiz":
        await who.quiz(ctx, client, pokebotCluster)
    elif command == "points":
        await db.showPoints(ctx, pokebotCluster)
    elif command == "reset":

        def areYouSure(m):
            print(m.content)
            return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "y" or m.content.lower() == "n")

        await ctx.channel.send("Are you sure you want to reset your points? y/n")

        try:
            msg = await client.wait_for('message', check=areYouSure, timeout=8.0)
            print(msg.content)
            
            if (msg.content == "y"): 
                await db.resetPoints(ctx, pokebotCluster)
                await ctx.channel.send("{.name}'s points have been reset".format(msg.author))
            else: await ctx.channel.send("{.name}'s points have not been reset".format(msg.author))
        except:
            await ctx.channel.send("Your points did not get reset")
    elif command == "catch":
        await spawn.spawnPoke(ctx, client, pokebotCluster)
    elif command == "timer-on":
        await timer(ctx, message, timerOn=True)
    elif command == "timer-off":
        timer.randomSpawns = False
    else:
        pokemon = message.split(" ", 1)[1]
        await info.show_poke(ctx, pokemon)

async def timer(ctx, message, timerOn):
    if(timer.randomSpawns == True):
        print("Already on")
        return

    timer.randomSpawns = timerOn
    while(timer.randomSpawns):
        await asyncio.sleep(random.randint(200, 600))
        if (timer.randomSpawns):
            await parser(ctx, "catch", message)



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(ctx):
    # if (catchingPokemon):
    #     print("Is working")
    #     return
        
    if ctx.author == client.user:
        return


    message = ctx.content

    if not message.lower().startswith("pokemon "):
        if (random.randint(0,5) > 2):
            await parser(ctx, "catch", message)
        return
    print(message)

    command = await mode(message)
    await parser(ctx, command, message)
    catchingPokemon = False

# catchingPokemon = False
timer.randomSpawns = False
client.run(token)
