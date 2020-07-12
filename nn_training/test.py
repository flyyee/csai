import sys

from load_model import load_model
from load_data import load_demo
from filenames import TEST_FILES

if __name__ == "__main__":
    # load the model based on the filename inputted by the user
    cmd_args = sys.argv
    modelfn = cmd_args[1]
    model = load_model("./saved_models/" + modelfn)
    model.summary() # prints a summary of the model (can be ommitted)
    test_data = load_demo(TEST_FILES) # load test data
    model.test(test_data)
