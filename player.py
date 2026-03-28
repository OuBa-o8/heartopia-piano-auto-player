import threading
import time
import keyboard
import json
import parser

note_map={
  #"鋼琴"
    "1_": "z",
    "2_": "x",
    "3_": "c",
    "4_": "v",
    "5_": "b",
    "6_": "n",
    "7_": "m",
    "1": "a",
    "2": "s",
    "3": "d",
    "4": "f",
    "5": "g",
    "6": "h",
    "7": "j",
    "1^": "q",
    "2^": "w",
    "3^": "e",
    "4^": "r",
    "5^": "t",
    "6^": "y",
    "7^": "u",
    "1^^":"i"
}
#,
#  "其他":{
#    "1": "y",
#    "2": "u",
#    "3": "i",
#    "4": "o",
#    "5": "p",
#    "6": "h",
#    "7": "j",
#    "1^": "k",
#    "2^": "l",
#    "3^": ";",
#    "4^": "n",
#    "5^": "m",
#    "6^": ",",
#    "7^": ".",
#    "1^^":"/"
#  }


def play_hand(events):

    for chord, duration in events:

        pressed = []

        for note in chord:
            if note in note_map:
                key = note_map[note]
                keyboard.press(key)
                pressed.append(key)

        time.sleep(duration)

        for key in pressed:
            keyboard.release(key)


def play(song):

    json_data = json.load(open("song.json", "r", encoding="utf-8"))

    global music
    music = json_data["songs"][int(song)-1]

    global note_map
    note_map = json.load(open("instrument.json", "r", encoding="utf-8"))[music["instrument"]]


def start(n):

    song = json.load(open("parsed.json", "r", encoding="utf-8"))
    left_hand = song["left_hand"]
    right_hand = song["right_hand"]
    third_hand = song["third_hand"]
    left_total = sum(duration for chord, duration in left_hand)
    right_total = sum(duration for chord, duration in right_hand)
    third_total = sum(duration for chord, duration in third_hand)
    print("left:", left_total)
    print("right:", right_total)
    print("third:",third_total)
    Fthread = threading.Thread(target=play_hand, args=(right_hand,))
    Sthread = threading.Thread(target=play_hand, args=(left_hand,))
    Tthread = threading.Thread(target=play_hand, args=(third_hand,))
    Fthread.start()
    Sthread.start()
    Tthread.start()
    Fthread.join()
    Sthread.join()
    Tthread.join()
    if n==1:
        print(f"{music['title']}演奏結束")
    else:
        print("播放完畢")
    