import random
import pokeInfo as info
import request as r
import databaseConnection as db

async def quiz(ctx, client, cluster):
    pokeID = random.randint(1, 893)
    await ctx.channel.send("Who's this pokemon?")
    pokemon = await info.show_poke(ctx, pokeID, show_name=False)
    
    pokemon_name = pokemon["name"]

    def check(m):
        return m.content.lower() == pokemon_name.lower() and m.channel == ctx.channel

    try:
        msg = await client.wait_for('message', check=check, timeout=6.0)
        await ctx.channel.send('Correct {.name}!'.format(msg.author))
        await db.givePoints(ctx, cluster)
    except:
        await ctx.channel.send('The answer was {}!'.format(pokemon_name))