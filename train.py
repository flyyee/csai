import sys

from keras_model import *
from load_data import loadDemo, TRAIN_FILES

if __name__ == "__main__":
    cmd_args = sys.argv
    nlayers = int(cmd_args[2]) if len(cmd_args) > 2 else 1
    # models = {
    #     "BaseModel": BaseModel(nlayers),
    #     "CNN": CNN(nlayers),
    #     "LSTM": LSTM(nlayers),
    #     "GRU": GRU(nlayers)
    # }
    models = {
        "BaseModel": KerasModel(nlayers),
        # "CNN": KerasCNN(nlayers),
        # "LSTM": KerasLSTM(nlayers),
        # "GRU": KerasGRU(nlayers)
    }
    if len(cmd_args) < 2:
        print("No model type specified.")
        print("usage: train.py <model_type> <num_layers=1>")
        sys.exit()
    if cmd_args[1] not in models.keys():
        print("Model type should be one of {}".format(models.keys()))

    train_data = loadDemo(TRAIN_FILES)
    model = models[cmd_args[1]]
    model.train(train_data)
    model.save()
