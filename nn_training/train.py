import sys

from keras_model import *
from branched_model import *
from load_data import load_demo
from filenames import TRAIN_FILES

if __name__ == "__main__":
    # parse command line inputs
    cmd_args = sys.argv
    modeltype = cmd_args[1] if len(cmd_args) > 1 else "BaseModel"
    nlayers = int(cmd_args[2]) if len(cmd_args) > 2 else 1
    version = int(cmd_args[3]) if len(cmd_args) > 3 else 1

    train_data = load_demo(TRAIN_FILES) # load train data
    # load the relevant model
    model = \
        KerasCNN(version=version, nlayers=nlayers) if modeltype == "CNN" else \
        KerasLSTM(version=version, nlayers=nlayers) if modeltype == "LSTM" else \
        KerasGRU(version=version, nlayers=nlayers) if modeltype ==  "GRU" else \
        KerasBranched(version=version, nlayers=nlayers) if modeltype == "BranchedModel" else \
        KerasModel(name=modeltype, version=version, nlayers=nlayers)
    model.summary() # prints a summary of the model (can be ommitted)
    model.train(train_data, epochs=10) # trains model for 10 epochs
    model.save() # saves the model to the saved_models folder
