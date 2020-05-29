import numpy as np

# Values of demofile
SPOTTED_CAP = 15
INPUT_COLS = ["tick", "self_x", "self_y", "self_z", "self_yaw", "self_pitch", "spotted", "hold"]
for pnum in range(SPOTTED_CAP):
    INPUT_COLS.extend(["p{}_x".format(pnum), "p{}_y".format(pnum), "p{}_z".format(pnum), "n{}".format(pnum)])

# Demofiles
TRAIN_FILES = [
    "singularity-vs-saw-m3-dust2,76561197978321481,1,07",
    "singularity-vs-saw-m3-dust2,76561197992800908,1,14",
    "singularity-vs-saw-m3-dust2,76561197994395491,0,86",
    "singularity-vs-saw-m3-dust2,76561197997981170,1,40",
    "singularity-vs-saw-m3-dust2,76561198012987839,1,54",
    "singularity-vs-saw-m3-dust2,76561198028941177,0,67",
    "singularity-vs-saw-m3-dust2,76561198079764052,1,00",
    "singularity-vs-saw-m3-dust2,76561198111983523,0,58"
]
TEST_FILES = [
    "singularity-vs-saw-m3-dust2,76561198047402862,1,36",
    "singularity-vs-saw-m3-dust2,76561198120557348,0,68"
]

def loadDemo(demofiles, tick_diff=100):
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
            curr_feature_lst.append(linedata[:8] + linedata[-SPOTTED_CAP*4:])
            curr_target_lst.append(linedata[4:6])
            weight_lst.append(kd)
        curr_feature_lst.pop(); curr_target_lst.pop(0)
        feature_lst += curr_feature_lst
        target_lst += curr_target_lst
    features = np.transpose(np.array(feature_lst))
    targets = np.transpose(np.array(target_lst))
    weights = np.array(weight_lst)
    return features, targets, weights

if __name__ == "__main__":
    # print(list(loadDemo(TRAIN_FILES)))
    features, targets, weights = loadDemo(TRAIN_FILES)
    print(len(features), len(features[0]))
    print([col[100:105] for col in features])
