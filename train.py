import sys

from model import models
from load_data import loadCSV

if __name__ == "__main__":
    cmd_args = sys.argv
    if len(cmd_args) < 2:
        print("No model type specified.")
        print("usage: test.py <model_type> <num_layers=1>")
        sys.exit()
    if cmd_args[1] not in models.keys():
        print("Model type should be one of {}".format(models.keys()))
    nlayers = int(cmd_args[2]) if len(cmd_args) > 2 else 1

    train_data = loadCSV("data/train.csv")
    model = models[cmd_args[1]](nlayers)
    model.summary() # Optional – prints a summary of the model
    model.train(train_data)
    model.save("./saved_models/{}.h5".format(model.__name__))
