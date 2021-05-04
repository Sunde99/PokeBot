import random
import pokeInfo as info
import databaseConnection as db

async def spawnPoke(ctx, client, cluster):
    pokeID = random.randint(1, 893)
    await ctx.channel.send("Catch this")

    await info.show_poke(ctx, pokeID, show_name=False, show_type=False)
    pokemon = await info.get_poke(ctx, pokeID)
    pokemon_name = pokemon["name"]
    await catch(ctx, client, cluster, pokemon_name) #TODO move this out


async def catch(ctx, client, cluster, pokemon_name):
    IVs = [random.randrange(0, 32, 1) for i in range(6)]
    def check(m):
        return m.content.lower() == pokemon_name.lower() and m.channel == ctx.channel

    try:
        msg = await client.wait_for('message', check=check, timeout=10.0)
        await ctx.channel.send('Correct {.name}!'.format(msg.author))
        await savePokemonToDB(ctx, pokemon_name, IVs, cluster)
    except:
        await ctx.channel.send('{} ran away...'.format(pokemon_name))

async def savePokemonToDB(ctx, pokemon, IVs, cluster):
    print("saving")
    await db.catchPokemon(ctx, pokemon, IVs, cluster)
