from load_model import load_model
from datetime import datetime
import keyboard

# TODO: define
IO_FN = ""
MODEL_FN = ""
KEY = ""

prev_timestamp = 0
start_time = datetime.now().microsecond*1000
model = load_model(MODEL_FN)
while True:
    keyboard.wait(KEY)
    status = "input"; timestamp = prev_timestamp
    while status != "input" and int(timestamp) <= prev_timestamp:
        with open(IO_FN) as inputfile:
            last_line = inputfile.readlines()[-1].strip().split(",")
        status, timestamp = last_line[:2]
    data = last_line[2:]
    curr_yaw, curr_pitch = data[4:6]
    new_yaw, new_pitch = model.predict([data])[0]m
    change_yaw, change_pitch = new_yaw-curr_yaw, new_pitch-curr_pitch
    new_timestamp = datetime.now().microsecond*1000 - start_time
    with open(IO_FN, "a") as outputfile:
        outputfile.write("output,{},{},{}\n".format(timeinms, new_timestamp, change_yaw, change_pitch))
