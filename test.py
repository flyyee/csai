import sys

from keras_model import *
from load_data import loadDemo, TEST_FILES

if __name__ == "__main__":
    cmd_args = sys.argv
    nlayers = int(cmd_args[2]) if len(cmd_args) > 2 else 1
    if len(cmd_args) < 2:
        print("No saved model specified.")
        print("usage: test.py <savedmodel_type>")
        sys.exit()
    models = {
        "BaseModel": KerasModel(nlayers),
        # "CNN": KerasCNN(nlayers),
        # "LSTM": KerasLSTM(nlayers),
        # "GRU": KerasGRU(nlayers)
    }
    model = models[cmd_args[1]]
    model.load("./saved_models/{}.h5".format(cmd_args[1]))
    test_data = loadDemo(TEST_FILES)
    model.test(test_data)
