import pytchat
import pafy
import pandas as pd

chat = pytchat.create(video_id="DWcJFNfaw9c")  #라이브 방송 주소 입력


while chat.is_alive():
    for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]-{c.message}")
