import random
import pokeInfo as info

async def quiz(ctx):
    print("HERE ENTERS QUIZ")
    await info.show_poke(ctx, random.randint(1, 893))