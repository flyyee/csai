import numpy as np

# Values of demofile
SPOTTED_CAP = 4
INPUT_COLS = ["tick", "self_x", "self_y", "self_z", "self_yaw", "self_pitch", "spotted", "hold"]
for pnum in range(SPOTTED_CAP):
    INPUT_COLS.extend(["p{}_x".format(pnum), "p{}_y".format(pnum), "p{}_z".format(pnum), "n{}".format(pnum)])

# Demofiles
# TODO: change to a list of demofiles
TRAIN_FILES = [
    "singularity-vs-saw-m3-dust2,76561197978321481,1,07",
    "singularity-vs-saw-m3-dust2,76561197992800908,1,14"
]
TEST_FILES = ["singularity-vs-saw-m3-dust2,76561198120557348,0,68"]

def loadDemo(demofiles, tick_diff=1000):
    # TODO: allow loading of multiple files
    # TODO: keep last few spotted values, instead of first few
    feature_lst = []; target_lst = []; weight_lst = []
    for demofn in demofiles:
        kd = float(demofn[-4:].replace(",", "."))
        with open("./demofiles/{}".format(demofn)) as demofile:
            textdata = demofile.read()
        first_tick = float(textdata.split("\n")[0].replace("tick", "")) - (tick_diff+1)
        textdata = textdata.replace("\n", ",")
        textdata = textdata.replace(",tick", "\n")
        textdata = textdata.replace("spotted", "").replace("hold", "").replace("tick", "")
        curr_feature_lst = []; curr_target_lst = []
        for line in textdata[:-1].split("\n"):
            linedata = list(map(float, line.split(",")))
            if linedata[0] - first_tick in range(tick_diff):
                continue
            first_tick = linedata[0]
            linedata.extend([0.0]*(SPOTTED_CAP*4))
            linedata = linedata[:8+SPOTTED_CAP*4]
            curr_feature_lst.append(linedata)
            curr_target_lst.append(linedata[4:6])
            weight_lst.append(kd)
        curr_feature_lst.pop(); curr_target_lst.pop(0)
        feature_lst += curr_feature_lst
        target_lst += curr_target_lst
    features = np.transpose(np.array(feature_lst))
    targets = np.transpose(np.array(target_lst))
    weights = np.array(weight_lst)
    # assert len(features[0]) == len(targets[0]) == len(weights)
    return features, targets, weights
    # return tf.data.Dataset.from_tensor_slices((feature_ts, target_ts, weight_ts)).batch(batch_size)

if __name__ == "__main__":
    # print(list(loadDemo(TRAIN_FILES)))
    features, targets, weights = loadDemo(TRAIN_FILES)
    print([col[400:405] for col in features])
