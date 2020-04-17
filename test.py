import sys
import tensorflow as tf

from model import BaseModel

if __name__ == "__main__":
    cmd_args = sys.argv
    if len(cmd_args) < 2:
        print("No saved model specified.")
        print("usage: test.py <savedmodel_type>")
        sys.exit()
    model = BaseModel.load_model("./saved_models/{}.h5".format(cmd_args[1]))
    model.test()
