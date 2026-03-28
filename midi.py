from mido import MidiFile, tick2second
import os
import json

note_map = {
    "1_": 48, "2_": 50, "3_": 52, "4_": 53, "5_": 55, "6_": 57, "7_": 59,
    "1": 60,  "2": 62,  "3": 64, "4": 65, "5": 67, "6": 69, "7": 71,
    "1^": 72, "2^": 74, "3^": 76, "4^": 77, "5^": 79, "6^": 81, "7^": 83, "1^^": 84
}

#天才的翻轉功能(我完全沒想到)
notes = {v: k for k, v in note_map.items()}

def midi2parsed(mid):

    result = {
        "left_hand": [],
        "right_hand": [],
        "third_hand": []
    }
    tempo = 500000  # 預設


    TICKS_PER_BEAT = mid.ticks_per_beat

    for track_index, track in enumerate(mid.tracks[:3]):

        events = []

        current_time = 0
        last_time = 0
        active_notes = []

        for msg in track:
            current_time += msg.time

            #有的音樂節奏會變
            if msg.type == "set_tempo":
                tempo = msg.tempo

            delta = current_time - last_time

            if delta > 0:
                duration = tick2second(delta, TICKS_PER_BEAT, tempo)

                if active_notes:
                    chord = sorted(active_notes)
                else:
                    chord = []

                events.append([chord.copy(), round(duration, 4)])
                last_time = current_time
            #按
            if msg.type == "note_on" and msg.velocity > 0:
                note = notes.get(msg.note)
                if note and note not in active_notes:
                    active_notes.append(note)

            #放
            elif msg.type == "note_off":
                note = notes.get(msg.note)
                if note and note in active_notes:
                    active_notes.remove(note)


        
        merged = []
        for chord, duration in events:
            if merged and merged[-1][0] == chord:
                merged[-1][1] += duration
            else:
                merged.append([chord, duration])

        if track_index == 0:
            result["left_hand"] = merged
        elif track_index == 1:
            result["right_hand"] = merged
        elif track_index == 2:
            result["third_hand"] = merged

    return result


def midi():

    ml=[f for f in os.listdir("./MIDI") if f.endswith(".mid")]

    if len(ml) == 0:
        print("沒檔案!去下載midi")
    else:
        print("=======Midi列表=======")
        for i in range(len(ml)):
            print(f"{i+1}: {ml[i]}")
        c= int(input("選midi:"))-1
        #載入 MIDI（這裡可能會炸報錯 好像是檔案的問題）
        mid = MidiFile(f"./MIDI/{ml[c]}")


        parsed = midi2parsed(mid)

        with open("parsed.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=4)

        print("已輸出 parsed.json")