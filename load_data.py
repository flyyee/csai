import numpy as np

# Values of demofile
SPOTTED_CAP = 15
INPUT_COLS = ["tick", "self_x", "self_y", "self_z", "self_yaw", "self_pitch", "spotted", "hold"]
for pnum in range(SPOTTED_CAP):
    INPUT_COLS.extend(["p{}_x".format(pnum), "p{}_y".format(pnum), "p{}_z".format(pnum), "p{}_tick".format(pnum)])

def spotted_tick_diff(curr_tick, spotted_lst):
    for i, val in enumerate(spotted_lst):
        if i % 4 != 3 or val == 0.0:
            continue
        spotted_lst[i] = curr_tick - val
    return spotted_lst

def load_demo(demofiles, tick_diff=32):
    feature_lst = []; target_lst = []; weight_lst = []
    for demofn in demofiles:
        kd = float(demofn[-4:].replace(",", "."))
        with open("./demofiles/{}".format(demofn)) as demofile:
            textdata = demofile.read()
        prev_tick = float(textdata.split("\n")[0].replace("tick", "")) - (tick_diff+1)
        textdata = textdata.replace("\n", ",")
        textdata = textdata.replace(",tick", "\n")
        textdata = textdata.replace("spotted", "").replace("hold", "").replace("tick", "")
        curr_feature_lst = []; curr_target_lst = []
        for line in textdata[:-1].split("\n"):
            linedata = list(map(float, line.split(",")))
            if (linedata[0] - prev_tick < tick_diff):
                continue
            prev_tick = linedata[0]
            rem_len = len(linedata)-8
            if rem_len < SPOTTED_CAP*4:
                 linedata.extend([0.0]*(SPOTTED_CAP*4-rem_len))
            curr_feature_lst.append(linedata[:8] + spotted_tick_diff(linedata[0], linedata[-SPOTTED_CAP*4:]))
            curr_target_lst.append(linedata[4:6])
            weight_lst.append(kd)
        curr_feature_lst.pop(); curr_target_lst.pop(0); weight_lst.pop()
        feature_lst += curr_feature_lst
        target_lst += curr_target_lst
        print("Loaded demo {} with {} sets of data".format(demofn, len(curr_feature_lst)))
    while len(feature_lst) % 3 != 0:
        feature_lst.pop(); target_lst.pop(); weight_lst.pop()
    features = np.transpose(np.array(feature_lst))
    targets = np.transpose(np.array(target_lst))
    weights = np.array(weight_lst)
    return features, targets, weights

if __name__ == "__main__":
    from filenames import TRAIN_FILES
    # print(list(loadDemo(TRAIN_FILES)))
    features, targets, weights = load_demo(TRAIN_FILES[0:1])
    print(features[-1])
