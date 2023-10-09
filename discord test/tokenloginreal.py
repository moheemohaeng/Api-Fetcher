import asyncio
import logging
import sys
import discord

client = discord.Client
class MyClient(client):
    def init(client, *, loop=None, **options):
        super().init(loop=loop, **options)


    async def on_ready(client):
        print('Logged on as', client.user)
        print(client.guilds[0].id)




    async def on_message(client, message):
        print(message.content)
        if message.author == client.user:
            pass #await message.channel.send('dddd')
        if message.content.startswith('ping'):
            await message.channel.send('pong')
            client.guilds.text_chanell

    

async def main():

    token = 'NDIyOTkzNTg1MTA5OTkxNDM0.YiWP8w.3ee46y17xFEKQAZqD4GZKNn2uyk'
    client = MyClient()
    await client.start(token, bot=False)
    print("asdf","asdf","asdfasdf")

if __name__ == "__main__":
    # handler = logging.StreamHandler(stream=sys.stdout)
    # handler.setLevel(logging.DEBUG)
    # handler2 = logging.FileHandler("log")
    # handler2.setLevel(logging.ERROR)

    # logger = logging.getLogger("discord")
    # logger.setLevel(logging.DEBUG)
    # logger.addHandler(handler)
    # logger.addHandler(handler2)
    asyncio.run(main())