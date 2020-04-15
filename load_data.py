import tensorflow as tf

# Columns of CSV file
FEATURE_COLS = [
    # Current player yaw and pitch
    "self_yaw", "self_pitch",
    # Current player location
    "self_x", "self_y",
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
    return input_cols, output_cols, label_col
