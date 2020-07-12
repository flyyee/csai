from nn_training.keras_model import *
from nn_training.branched_model import *

def load_model(filename, modeltype=None, nlayers=None):
    """
    modeltype and nlayers will not need to be defined if using the default naming for the models
    ./saved_models/<modeltype>-<nlayers>layers-[...].h5
    """
    fninfo = filename.split("/")[-1][:-3].split("-")
    modeltype = fninfo[0] if modeltype == None else modeltype
    nlayers = int(fninfo[1][:-6]) if nlayers == None else nlayers
    version = int(fninfo[2][1:])
    model = \
        KerasCNN(version=version, nlayers=nlayers) if modeltype == "CNN" else \
        KerasLSTM(version=version, nlayers=nlayers) if modeltype == "LSTM" else \
        KerasGRU(version=version, nlayers=nlayers) if modeltype ==  "GRU" else \
        KerasBranched(version=version, nlayers=nlayers) if modeltype == "BranchedModel" else \
        KerasModel(version=version, nlayers=nlayers)
    model.load(filename)
    return model

if __name__ == "__main__":
    # from load_data import load_demo
    from filenames import TEST_FILES
    import numpy
    model = load_model("./saved_models/BranchedModel_GRU-5layers-v4.h5")
    print(model.predict([numpy.array([64.0, 0.0, 0.0]),numpy.array([-367.000000, 0.0, 0.0]),numpy.array([-808.000000, 0.0, 0.0]),numpy.array([83.745102, 0.0, 0.0]),numpy.array([-0.051801, 0.0, 0.0]),numpy.array([-179.720718, 0.0, 0.0]),numpy.array([0.0, 0.0, 0.0]),numpy.array([0.0, 0.0, 0.0])]))
