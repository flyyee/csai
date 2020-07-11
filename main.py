from load_model import load_model
import time
from numpy import array

# TODO: define
IO_FN = "com.txt"
MODEL_FN = "./saved_models/BranchedModel_GRU-5layers-v4.h5"

def mod360(v):
    return v - (v//360)*360

prev_timestamp = 0
start_time = int(round(time.time() * 1000))
model = load_model(MODEL_FN)
while True:
    status = ""; timestamp = prev_timestamp
    while status != "input" or int(timestamp) <= prev_timestamp:
        with open(IO_FN) as inputfile:
            last_line = inputfile.readlines()[-1].strip().split(",")
        status, timestamp = last_line[:2]
    strdata = last_line[2:]
    strdata[6] = strdata[6][7:]; strdata[7] = strdata[7][4:]
    data = [array([float(d), 0.0, 0.0]) for d in strdata]
    curr_yaw, curr_pitch = strdata[4:6]
    new_yaw, new_pitch = model.predict(data)[0]
    change_yaw, change_pitch = mod360(float(new_yaw))-float(curr_yaw), mod360(float(new_pitch))-float(curr_pitch)
    new_timestamp = int(round(time.time() * 1000)) - start_time
    with open(IO_FN, "a") as outputfile:
        outputfile.write("output,{},{},{}\n".format(
            new_timestamp,
            change_yaw,
            change_pitch
        ))
