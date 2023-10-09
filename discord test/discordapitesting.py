import asyncio
import logging
import sys
import discord
from discord.message import MessageReference
import datetime
import json
from bson import json_util
import os
import shutil


from pathlib import Path
from nwlib.protocol.fetched_result import FetchedResult

from pymongo import MongoClient
from pymongo.cursor import CursorType

fetch = FetchedResult()
class MyClient(discord.Client):
    def __init__(self, token, aftertime, beforetime, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.token = token
        self.aftertime = aftertime
        self.beforetime = beforetime


    async def on_ready(client):

        print('Logged on as', client.user)

        os.mkdir('C:/Users/user/Desktop/discord test/meta')
        os.mkdir('C:/Users/user/Desktop/discord test/data')

        host = '192.168.1.45'
        # host = 'localhost'
        port = '25017'
        mongo = MongoClient(host, int(port))
        for guild in client.guilds:
                for channel in guild.text_channels:
                    
                    meta_path = 'C:/Users/user/Desktop/discord test/meta/'+guild.name+'_'+channel.name+'_meta.json'
                    
                    meta = {'python_version':'Python 3.10.2', 'discord.py_version':'1.7.3', 'private_token' : client.token, 'from_date':client.aftertime, 'to_date':client.beforetime,
                        'guild':{'id':guild.id,'name':guild.name, 'created_at':guild.created_at,'description':guild.description,'region':guild.region, 'member_count':guild.member_count},
                        'text_channel' :{'id':channel.id,'name':channel.name, 'created_at':channel.created_at}}
                    print(channel.name, ' channel on=================================================================')

                    with open(meta_path, 'w', encoding='UTF-8') as file:
                        json.dump(meta, file, default=json_util.default, indent =4, ensure_ascii=False)
                    mongo["discord"]["meta"].insert_one(meta).inserted_id

                    # channel_message = {'messages':[]}
                    chats = await channel.history(limit = None, after = client.aftertime, before = client.beforetime).flatten()
                    for chat in chats:
                        file_path = 'C:/Users/user/Desktop/discord test/data/'+str(chat.id)+'.json'
                        reference = chat.to_reference(fail_if_not_exists=True)
                        embeds = []
                        attachments = []
                        for embed in chat.embeds:
                            embeds.append(embed.to_dict())
                        for attachment in chat.attachments:
                            attachments.append({'content_type':attachment.content_type,
                            'filename':attachment.filename, 'height':attachment.height,
                            'id':attachment.id, 'proxy_url':attachment.proxy_url, 'size':attachment.size,
                            'url':attachment.url, 'width':attachment.width})

                        content = {'id':chat.id,'created_at' : chat.created_at, 
                            'author' : {'id': chat.author.id, 'name':chat.author.name, 'discriminator': chat.author.discriminator, 'display_name': chat.author.display_name, 'is_bot':chat.author.bot}, 
                            'content' : chat.content,
                            'reference':{'jump_url' : reference.jump_url, 'guild_id' : reference.guild_id, 'channel_id':reference.channel_id},
                            'embeds':embeds, 'attachments':attachments,
                            }
                        # try:
                        #     content = {'id':chat.id,'created_at' : chat.created_at, 
                        #     'author' : {'id': chat.author.id, 'name':chat.author.name, 'discriminator': chat.author.discriminator, 'display_name': chat.author.display_name, 'is_bot':chat.author.bot}, 
                        #     'content' : chat.content,
                        #     'reference':{'jump_url' : reference.jump_url, 'guild_id' : reference.guild_id, 'channel_id':reference.channel_id},
                        #     'embeds':embeds
                        #     }
                        # except:
                        #     content = {'id':chat.id,'created_at' : chat.created_at, 
                        #     'author' : {'id': chat.author.id, 'name':chat.author.name, 'discriminator': chat.author.discriminator, 'display_name': chat.author.display_name, 'is_bot':chat.author.bot}, 
                        #     'content' : chat.content,
                        #     'reference':{'jump_url' : reference.jump_url, 'guild_id' : reference.guild_id, 'channel_id':reference.channel_id},

                        #     }
                        print(chat.id, ' message on----------------------')
                        # channel_message['messages'].append(content)
                    

                        with open(file_path, 'w', encoding='UTF-8') as file:
                            json.dump(content, file, default=json_util.default, indent = 4,ensure_ascii = False)

                        fetch.add_file(file_name = str(guild.id)+'_'+str(channel.id)+'_'+str(chat.id), meta_file_path=Path(meta_path), data_file_path = Path(file_path))

                        mongo["discord"]["content"].insert_one(content).inserted_id
                
                    


        print('Logout', client.user)                 
        await client.close()



    async def on_message(self,message):
        print(message.content)
        if message.author == self.user:
            await message.channel.send('dddd')
        if message.content.startswith('ping'):
            await message.channel.send('pong')







async def main(token, aftertime, beforetime):


    client = MyClient(token = token, aftertime=aftertime , beforetime=beforetime)
    await client.start(token, bot=False)



if __name__ == "__main__":
    token = 'NDIyOTkzNTg1MTA5OTkxNDM0.YiWP8w.3ee46y17xFEKQAZqD4GZKNn2uyk'
    asyncio.run(main(token = token, aftertime= datetime.datetime(2022,4,10,12,1,1), beforetime=datetime.datetime(2022,6,4,4,4,4)))

    # print('removiiiiiiiiiiiiiiiiiiiiiiiiii')
    # if os.path.exists('C:/Users/user/Desktop/discord test/meta') :
    #     shutil.rmtree('C:/Users/user/Desktop/discord test/meta')
    # if os.path.exists('C:/Users/user/Desktop/discord test/data') :    
    #     shutil.rmtree('C:/Users/user/Desktop/discord test/data')
