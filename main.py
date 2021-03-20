import discord

token = open("token.txt", "r").read()
client = discord.Client()
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    await msg.channel.send("Rock smash")


client.run(token)
