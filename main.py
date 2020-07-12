from load_model import load_model
import time
from numpy import array

# TODO: define
IO_FN = "com.txt" # file to communicate between ai and csgo helper
MODEL_FN = "./saved_models/BranchedModel_GRU-5layers-v4.h5"

def mod360(v):
    return v - (v//360)*360

prev_timestamp = 0
start_time = int(round(time.time() * 1000))
model = load_model(MODEL_FN) # load the model
# continuously checks for input by csgo helper
while True:
    status = ""; timestamp = prev_timestamp
    # reads game state from shared file with the csgo helper
    while status != "input" or int(timestamp) <= prev_timestamp: # check if line type is input and timestamp is different
        with open(IO_FN) as inputfile:
            last_line = inputfile.readlines()[-1].strip().split(",")
        status, timestamp = last_line[:2]
    strdata = last_line[2:]
    # cleans data to be passed into the neural network
    strdata[6] = strdata[6][7:]; strdata[7] = strdata[7][4:]
    data = [array([float(d), 0.0, 0.0]) for d in strdata]
    curr_yaw, curr_pitch = strdata[4:6] # get the current pitch and yaw
    new_yaw, new_pitch = model.predict(data)[0] # pass game state into neural network
    # calculate the ideal change in pitch and yaw
    change_yaw, change_pitch = mod360(float(new_yaw))-float(curr_yaw), mod360(float(new_pitch))-float(curr_pitch)
    # writes ideal pitch and yaw movements to shared file with csgo helper
    new_timestamp = int(round(time.time() * 1000)) - start_time
    with open(IO_FN, "a") as outputfile:
        outputfile.write("output,{},{},{}\n".format(
            new_timestamp,
            change_yaw,
            change_pitch
        ))
