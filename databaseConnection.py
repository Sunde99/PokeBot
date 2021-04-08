import discord
import pymongo
from discord.ext import commands
from pymongo import MongoClient


async def getDB(cluster):
    db = cluster["Pokebot"]
    return db

async def pointsDB(db):
    points = db["Points"]
    return points

async def givePoints(msg, cluster):
    """[Gives the sender of the message a point]

    Args:
        msg ([context]): [The person sending the message]
        cluster ([Database Cluster]): [The cluster used for picking out the points table]
    """
    points = await pointsDB(await getDB(cluster))
    my_query = { "_id": msg.author.id }
    if (points.count_documents(my_query) == 0):
        post = {"_id": msg.author.id, "score":1}
        points.insert_one(post)
        print("AAA GIVE POINTS JUST GAVE SOMEONE THEIR FIRST POINT")
    else:
        user = points.find(my_query)
        for result in user:
            score = result["score"]
        score += 1
        points.update_one({"_id":msg.author.id}, {"$set":{"score":score}})
        print("AAA POINTS HAVE BEEN INCREASED")

async def showPoints(ctx, cluster):
    """[summary]

    Args:
        ctx ([context]): [The person sending the message]
        cluster ([Database Cluster]): [The cluster used for picking out the points table]

    Returns:
        [Int]: [Points]
    """
    points = await pointsDB(await getDB(cluster))

    currentPoints = points.find({}, {'_id': 0})
    for data in currentPoints:
        score = data["score"]
        await ctx.channel.send(f"{ctx.author.name} has {score} points")
