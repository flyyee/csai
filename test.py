import sys

from keras_model import *
from load_data import load_demo
from filenames import TEST_FILES

if __name__ == "__main__":
    cmd_args = sys.argv
    nlayers = int(cmd_args[1]) if len(cmd_args) > 1 else 1
    models = {
        "BaseModel": KerasModel(nlayers=nlayers),
        "CNN": KerasCNN(nlayers=nlayers),
        "LSTM": KerasLSTM(nlayers=nlayers),
        "GRU": KerasGRU(nlayers=nlayers)
    }
    for modelname, model in models:
        model.load("./saved_models/{}-{}layers.h5".format(modelname, nlayers))
        model.summary()
        test_data = load_demo(TEST_FILES)
        model.test(test_data)
