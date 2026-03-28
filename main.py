import json
import time
import player
import parser
import midi

s=0

while s!="-1":
    
    json_data = json.load(open("song.json", "r", encoding="utf-8"))
    print("======================")
    print("目錄:")
    for idx, song in enumerate(json_data["songs"]):
        print(f"{idx+1}. {song['title']}")
    s = input("選歌(0:midi模式):")
    if s != "0":
        parser.compile(s)

        time.sleep(3)
        player.play(s)
        player.start(1)
    else:
        midi.midi()
        time.sleep(3)
        player.start(2)


