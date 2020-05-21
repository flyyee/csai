import tensorflow as tf

# Columns of CSV file
# TODO: delete
FEATURE_COLS = [
    # Current player location
    "self_x", "self_y", "self_z",
    # Current player yaw and pitch
    "self_yaw", "self_pitch",
    # hold
    "hold",
    # Teammates' locations
    "t1_x", "t1_y", "t2_x", "t2_y", "t3_x", "t3_y", "t4_x", "t4_y",
    # Enemy locations
    "e1_x", "e1_y", "e2_x", "e2_y", "e3_x", "e3_y", "e4_x", "e4_y", "e5_x", "e5_y",
]
TARGET_COLS = [
    # Yaw and pitch to move to
    "dest_yaw", "dest_pitch"
]
WEIGHT_COL = "kd"

# Values of demofile
SPOTTED_CAP = 4
INPUT_COLS = ["tick", "self_x", "self_y", "self_z", "self_yaw", "self_pitch", "spotted", "hold"]
for pnum in range(SPOTTED_CAP):
    INPUT_COLS.extend(["p{}_x".format(pnum), "p{}_y".format(pnum), "p{}_z".format(pnum), "n{}".format(pnum)])

INPUT_REFS = [tf.constant(col).experimental_ref() for col in INPUT_COLS]

# Demofiles
# TODO: change to a list of demofiles
TRAIN_FILES = "./demofiles/singularity-vs-saw-m3-dust2,76561197978321481,1,07"

# TODO: delete
def loadCSV(csv, batch_size, **kwargs):
    feature_cols = tf.data.experimental.make_csv_dataset(
        csv,
        batch_size,
        select_columns=FEATURE_COLS,
        ignore_errors=True,
        **kwargs
    )
    target_cols = tf.data.experimental.make_csv_dataset(
        csv,
        batch_size,
        select_columns=TARGET_COLS,
        ignore_errors=True,
        **kwargs
    )
    weight_col = input_cols = tf.data.experimental.make_csv_dataset(
        csv,
        batch_size,
        select_columns=[WEIGHT_COL],
        ignore_errors=True,
        **kwargs
    )
    return Dataset.zip((input_cols, output_cols, label_col))

def loadDemo(demofn, tick_diff=1000, batch_size=2):
    # TODO: allow loading of multiple files
    # TODO: keep last few spotted values, instead of first few
    kd = float(demofn[-4:].replace(",", "."))
    with open(demofn) as demofile:
        textdata = demofile.read()
    first_tick = float(textdata.split("\n")[0].replace("tick", "")) - (tick_diff+1)
    textdata = textdata.replace("\n", ",")
    textdata = textdata.replace(",tick", "\n")
    textdata = textdata.replace("spotted", "").replace("hold", "").replace("tick", "")
    feature_lst = []; target_lst = []
    for line in textdata[:-1].split("\n"):
        linedata = list(map(float, line.split(",")))
        if linedata[0] - first_tick in range(tick_diff):
            continue
        first_tick = linedata[0]
        linedata.extend([0.0]*(SPOTTED_CAP*4))
        linedata = linedata[:8+SPOTTED_CAP*4]
        feature_lst.append(linedata)
        target_lst.append(linedata[4:6])
    feature_lst.pop(); target_lst.pop(0)
    feature_ts = tf.convert_to_tensor(feature_lst)
    target_ts = tf.convert_to_tensor(target_lst)
    weight_ts = tf.convert_to_tensor([kd]*len(target_lst))
    return tf.data.Dataset.from_tensor_slices((feature_ts, target_ts, weight_ts)).batch(batch_size)

if __name__ == "__main__":
    print(list(loadDemo(TRAIN_FILES))[:5])
