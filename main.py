import discord
import pymongo
import requests
import random
import asyncio
from pymongo import MongoClient

import databaseConnection as db
import utility
import items
import request
import abilities
import whosThatPokemon as who
import spawnPokemon as spawn

connection_url = open("connection_url.txt", "r").read()
cluster = MongoClient(connection_url)
pokebotCluster = cluster["Pokebot"]


token = open("token.txt", "r").read()
client = discord.Client()

async def mode(msg):
    return msg.split()[1].lower()

async def parser(ctx, command, message): # TODO message has command as its first element, FIX!
    if command == "quiz":
        quiz = who.QuizGame(client, pokebotCluster)
        await quiz.quiz(ctx)
        # await who.quiz(ctx, client, pokebotCluster)
    elif command == "points":
        await db.showPoints(ctx, pokebotCluster)
    elif command == "reset":
        await db.resetPoints(ctx, pokebotCluster, client)
    elif command == "catch":
        spawner = spawn.PokemonSpawner(ctx, client, pokebotCluster)
        await spawner.spawnPoke()
        await spawner.catch()
        del spawner
        # await spawn.spawnPoke(ctx, client, pokebotCluster)
    elif command == "timer-on":
        await timer(ctx, message, timerOn=True)
    elif command == "timer-off":
        timer.randomSpawns = False
    elif command == "item":
        if (len(message.split()) > 3): item = message.split(" ", 2)
        else: item = message.split()
        if (len(item) <= 2): await ctx.channel.send("You need to give me an item to check!")
        else: await items.item(ctx, item[2])

    elif command == "ability":
        if (len(message.split()) > 3): poke_ability = message.split(" ", 2)
        else: poke_ability = message.split()

        ability_checker = abilities.Ability(ctx)
        if (await ability_checker.is_this_ability(poke_ability[2])):
            print(poke_ability[2] + "<----")
            await ability_checker.ability_lookup(poke_ability[2])
        else:
            await ability_checker.possible_abilities()

        await ability_checker.ability_show()


        # if (len(ability) <= 2): await ctx.channel.send("You need to give me an ability to check!")
        # else: await abilities.ability_show(ctx, ability[2], await abilities.ability_lookup(ctx, ability[2]))

    else:
        pokemon = message.split(" ", 1)[1]
        await utility.show_poke(ctx, pokemon)

async def timer(ctx, message, timerOn):
    if(timer.randomSpawns == True):
        print("Already on")
        return

    timer.randomSpawns = timerOn
    while(timer.randomSpawns):
        await asyncio.sleep(random.randint(15, 30))
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
        return
    print(message)

    command = await mode(message)
    await parser(ctx, command, message)
    # catchingPokemon = False

# catchingPokemon = False
timer.randomSpawns = False
client.run(token)
