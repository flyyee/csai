# csai

## Branches
Branches naming convention:
- 0.0.1
- a-b-c
- release - type - version number

Types:
1. notifications
2. mouse movements
3. read demos
4. neural network

## Directory Navigation
```
.
|-- demo_parser/
|   |-- app.js
|   |-- package-lock.json
|-- nn_training/
|   |-- branched_model.py
|   |-- filenames.py
|   |-- keras_model.py
|   |-- load_data.py
|   |-- test.py
|   |-- train.py
|-- saved_models/
|-- .gitattributes
|-- com.txt
|-- load_model.py
|-- main.cpp
|-- main.py
|-- MemoryManager.h
|-- README.md
|-- requirements.txt
```

## Installation
### C++
only runs on windows as native windows processes are used,
no non-standard libraries required

### Node.js
1. download nodejs from https://nodejs.org/en/download/
  - download npm together with nodejs during the installation
2. run "npm i" in the directory with app.js

### Python
1. download python3 at https://www.python.org/downloads/
2. run `$ pip3 install -r requirements.txt` to install the tensorflow and numpy libraries
  - Otherwise, run `$ pip install -Iv 'tensorflow>=2.0.0'` and `$ pip install numpy`

### CS:GO
1. install steam from https://store.steampowered.com/about/
2. install csgo from https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/
3. start csgo with the following launch options: `(library > counter-strike: global offensive > properties > set launch option) "-untrusted -insecure"`
  - the latest version of csgo may contain a version of dust2 that is different from the version we are training our model on. copy the folder from dust2 map to your steam: `install location > steamapps\common\Counter-Strike Global Offensive\csgo\maps\workshop`
4. start an offline game with bots with the workshop map de_dust2

## Instructions
### Main CSAI Program
1. compile main.cpp in visual studio 2019
2. run `main.py` and `main.exe`
3. key to activate the program is F5

do not delete any files or folders

### Demo Parser
1. load the demofiles folder with demo files to be parsed
2. run `$ node app.js`

this operation may take some time to complete, depending on the hardware used and the number of demo files

no more than 20 demo files are recommended to be parsed at once

### Training
1. go to the `nn_training` folder: `$ cd nn_training`
2. run `$ python3 train.py <modelname> <nlayers> <version>`
  - `modelname` can be "BaseModel", "CNN", "LSTM", "GRU" or "BranchedModel"

if you do not want weights to be factored in,
go to `keras_model.py` and comment out line 61
```python
61|       # sample_weight=[weight, weight]
```

### Testing
1. go to the `nn_training` folder: `$ cd nn_training`
2. run `$ python3 test.py <filename>`
  - ensure that the file can be found in the `saved_models` folder

note that when using the v1 models,
`INPUT_COLS` will have to be edited at line 7 of `load_data.py` as follows:
```python
7|    INPUT_COLS.extend(["p{}_x".format(pnum), "p{}_y".format(pnum), "p{}_z".format(pnum), "n{}".format(pnum)])
```
