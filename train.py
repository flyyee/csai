import sys

from keras_model import *
from load_data import loadDemo
from filenames import TRAIN_FILES

if __name__ == "__main__":
    cmd_args = sys.argv
    nlayers = int(cmd_args[1]) if len(cmd_args) > 1 else 1
    models = [
        KerasModel(nlayers=nlayers),
        KerasCNN(nlayers=nlayers),
        KerasLSTM(nlayers=nlayers),
        KerasGRU(nlayers=nlayers)
    ]

    train_data = loadDemo(TRAIN_FILES)
    for model in models:
        model.summary()
        model.train(train_data, epochs=10)
        model.save()
