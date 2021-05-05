import random
import utility
import request as r
import databaseConnection as db

class QuizGame:

    def __init__(self, client, cluster):
        self.pokeID = random.randint(1, 893)
        self.client = client
        self.cluster = cluster


    async def quiz(self, ctx):
        await ctx.channel.send("Who's this pokemon?")
        pokemon = await utility.get_poke(ctx, self.pokeID)
        await utility.show_poke(ctx, self.pokeID, show_name=False)
        
        pokemon_name = pokemon["name"]

        def check(m):
            return m.content.lower() == pokemon_name.lower() and m.channel == ctx.channel

        try:
            msg = await self.client.wait_for('message', check=check, timeout=6.0)
            await ctx.channel.send('Correct {.name}!'.format(msg.author))
            await db.givePoints(msg, self.cluster)
        except:
            await ctx.channel.send('The answer was {}!'.format(pokemon_name))
