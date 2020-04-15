import sys
import tensorflow as tf

from model import BaseModel

if __name__ == "__main__":
    cmd_args = sys.argv
    if len(sys.argv) < 2:
        print("No saved model specified.")
        print("usage: test.py <savedmodel_type>")
        sys.exit()
    model = BaseModel.load_model("./saved_models/{}.h5".format(sys.argv[1]))
    model.test()
