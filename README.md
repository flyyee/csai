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
Main application:
```
.
|-- demo_parser/
|   |-- app.js
|   |-- package-lock.json
|-- nn_training/
|   |-- demofiles.zip
|   |-- filenames.py
|   |-- load_data.py
|   |-- branched_model.py
|   |-- keras_model.py
|   |-- test.py
|   |-- train.py
|-- saved_models/
|   |-- BaseModel-5layers-v1.h5
|   |-- BaseModel-5layers-v2.h5				
|   |-- CNN-5layers-v1.h5
|   |-- CNN-5layers-v2.h5
|   |-- GRU-5layers-v1.h5
|   |-- GRU-5layers-v2.h5
|   |-- GRU-5layers-v3.h5		
|   |-- LSTM-5layers-v1.h5
|   |-- LSTM-5layers-v2.h5
|   |-- LSTM-5layers-v3.h5
|   |-- BranchedModel_GRU-5layers-v4.h5
|   |-- BranchedModel_LSTM-5layers-v4.h5
|-- main.cpp
|-- MemoryManager.h
|-- main.py
|-- load_model.py
|-- com.txt
```
Report, README and others:
```
|-- finalreport_files/
|-- finalreport.md
|-- README.md
|-- requirements.txt
|-- .gitattributes
```

## Installation
### C++
only runs on windows as native windows processes are used,
no non-standard libraries required

### Node.js
1. download [node.js](https://nodejs.org/en/download/)
  - download npm together with nodejs during the installation
2. run "npm i" in the directory with app.js

### Python
1. download [python3](https://www.python.org/downloads/)
2. run `$ pip3 install -r requirements.txt` to install the tensorflow and numpy libraries
  - Otherwise, run `$ pip install -Iv 'tensorflow>=2.0.0'` and `$ pip install numpy`

### CS:GO
1. install [steam](https://store.steampowered.com/about/)
2. install [csgo](https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/)
3. start csgo with the following launch options: `(library > counter-strike: global offensive > properties > set launch option) "-untrusted -insecure"`
  - the latest version of csgo may contain a version of dust2 that is different from the version we are training our model on. copy the folder from dust2 map to your steam: `install location > steamapps\common\Counter-Strike Global Offensive\csgo\maps\workshop`
4. start an offline game with bots with the workshop map de_dust2

## Instructions
### Main CSAI Program
1. compile `main.cpp` in visual studio 2019
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
2. unzip `demofiles.zip`
3. run `$ python3 train.py <modelname> <nlayers> <version>`
  - `modelname` can be "BaseModel", "CNN", "LSTM", "GRU" or "BranchedModel"

if you do not want weights to be factored in,
go to `keras_model.py` and comment out line 73
```python
73|       # sample_weight=[weight, weight]
```

### Testing
1. go to the `nn_training` folder: `$ cd nn_training`
2. unzip `demofiles.zip`
3. run `$ python3 test.py <filename>`
  - ensure that the file can be found in the `saved_models` folder

note that when using the v1 models,
`INPUT_COLS` will have to be edited at line 7 of `load_data.py` as follows:
```python
7|    INPUT_COLS.extend(["p{}_x".format(pnum), "p{}_y".format(pnum), "p{}_z".format(pnum), "n{}".format(pnum)])
```

if you do not want weights to be factored in,
go to `keras_model.py` and comment out line 86
```python
86|       # sample_weight=[weight, weight]
```
