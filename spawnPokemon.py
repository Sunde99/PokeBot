import random
import utility
import databaseConnection as db

class PokemonSpawner:

    def __init__(self, ctx, client, cluster):
        self.pokeID = random.randint(1,893)
        self.IVs = [random.randrange(0, 32, 1) for i in range(6)]
        self.ctx = ctx
        self.client = client
        self.cluster = cluster
        self.pokemon = {}
        self.pokemon_name = ""

    async def spawnPoke(self):
        await self.ctx.channel.send("Catch this!")
        await utility.show_poke(self.ctx, self.pokeID, show_name=False, show_type=False)
        self.pokemon = await utility.get_poke(self.ctx, self.pokeID)
        self.pokemon_name = self.pokemon["name"]

    async def catch(self):
        def check(m):
            return m.content.lower() == self.pokemon_name.lower() and m.channel == self.ctx.channel

        try:
            msg = await self.client.wait_for('message', check=check, timeout=10.0)
            await self.ctx.channel.send('Correct {.name}!'.format(msg.author))
            print("Saving")
            await db.catchPokemon(msg, self.pokemon_name, self.IVs, self.cluster)
            print("Saved")
        except:
            await self.ctx.channel.send('{} ran away...'.format(self.pokemon_name))

