import discord
import pymongo
from discord.ext import commands
from pymongo import MongoClient

async def pointsDB(db):
    return db["Points"]
    

async def pokemonDB(db):
    return db["Pokemon"]

async def givePoints(msg, cluster):
    """[Gives the sender of the message a point]

    Args:
        msg ([context]): [The person sending the message]
        cluster ([Database Cluster]): [The cluster used for picking out the points table]
    """
    db = await pointsDB(cluster)
    my_query = { "_id": msg.author.id }
    if (db.count_documents(my_query) == 0):
        post = {"_id": msg.author.id, "score":1}
        db.insert_one(post)
        print("AAA GIVE POINTS JUST GAVE SOMEONE THEIR FIRST POINT")
    else:
        user = db.find(my_query)
        for result in user:
            score = result["score"]
        score += 1
        db.update_one({ "_id":msg.author.id }, { "$set":{ "score":score } })
        print("AAA POINTS HAVE BEEN INCREASED")

async def showPoints(ctx, cluster):
    """[summary]

    Args:
        ctx ([context]): [The person sending the message]
        cluster ([Database Cluster]): [The cluster used for picking out the points table]

    Returns:
        [Int]: [Points]
    """
    points = await pointsDB(cluster)

    currentPoints = points.find({}, {'_id': 1, 'score': 1})
    for data in currentPoints:
        if (data["_id"] != ctx.author.id): continue
        print("----ID")
        print(ctx.author.id)
        print(data["_id"])
        score = data["score"]
        await ctx.channel.send(f"{ctx.author.name} has {score} points")

async def resetPoints(ctx, cluster, client):
    def areYouSure(m):
        print("L1")
        print(m.content)
        print("L2")
        print(m.author.name)
        return m.author == ctx.author and m.channel == ctx.channel and (m.content.lower() == "y" or m.content.lower() == "n")

    await ctx.channel.send("Are you sure you want to reset your points? y/n")

    try:
        print("This should run")
        msg = await client.wait_for('message', check=areYouSure, timeout=8.0)
        print(msg.content)
        
            
        if (msg.content == "y"): 
            db = await pointsDB(cluster)
            db.update_one({"_id":ctx.author.id}, {"$set":{"score":0}})
            await ctx.channel.send("{.name}'s points have been reset".format(msg.author))
        else: 
            await ctx.channel.send("{.name}'s points have not been reset".format(msg.author))
    except:
        await ctx.channel.send("Your points did not get reset")

    

async def catchPokemon(ctx, pokemon, IVs, cluster):
    db = await pokemonDB(cluster)
    my_query = { "Trainer": ctx.author.id }

    print("One")
    amount_of_pokemon = db.count_documents(my_query)
    _id = str(ctx.author.id) + "-" + str(amount_of_pokemon)
    print(_id)
    print("Two")

    post = { "_id": _id, "Trainer": ctx.author.id, "Pokemon": pokemon, "IVs": IVs }
    print("Three")
    db.insert_one(post)