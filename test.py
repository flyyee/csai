import sys

from load_model import load_model
from load_data import load_demo
from filenames import TEST_FILES

if __name__ == "__main__":
    cmd_args = sys.argv
    modelfn = cmd_args[1]
    model = load_model("./saved_models/" + modelfn)
    # model.summary()
    test_data = load_demo(TEST_FILES)
    model.test(test_data)
