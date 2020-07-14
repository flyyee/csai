# CSAI
## Project Members
Koh Luck Heng, Gerrard Tai
- [Video Presentation](https://youtu.be/PmsJ2kOf1VQ)
- [GitHub Repo](https://github.com/flyyee/csai/tree/master)

## Project Introduction
CSAI is a program aided by machine learning that helps new Counter-Strike Global Offensive, or CSGO, players with no Internet connection learn to play the game.

Most new players will pick up the necessary skills for playing by watching more experienced players play in the matches they are in, or from youtube videos. A big part of picking up the game is learning where to look. For beginners, CSGO can be extremely complicated, especially when learning the ins and outs of a map they have never seen before. They will not know where they should be looking at certain points of the game in expectation of an enemy, at the entrance to their left, or the stairway by their right. Usually, they would amass such knowledge through watching more experienced players play - something they are unable to do when they have no Internet. Thus, CSAI was born of such noble intentions of providing knowledge to the world.

When playing a CSGO match, the user starts CSAI. At the press of a key, CSAI is fired up, reading information about the user’s current state in the game. The information it sends to the neural network are the user’s current position in the map, where he is currently looking and the positions his team has spotted enemies in that round. The neural net processes this, and returns the ideal position the user should be looking at. The program then shifts the user’s crosshair to face that position. In this fashion, CSAI takes into account all this data and uses machine learning to teach new players how to improve on the game.

## Machine Learning Algorithm
As stated earlier, information related to the current state of the game, such as the player’s current position on the map, the direction that he is looking at and the positions of the enemies spotted by his team, are sent to the neural network.

For our machine learning algorithm, we experimented with 4 different types of neural network layers

The first type is the dense layer, which is a basic layer with each cell having just one filter, where the inputs to the cell are evaluated using weights and biases that are changed depending on how far the output prediction deviates from the target value. The outcome of the calculation then passed into an activation function, usually either the `sigmoid`, `tanh` or `ReLU` functions, which serve to regulate the outputs of the cell which will be passed on to the next layer. For the dense layer, this activation function is the `sigmoid` function, which is defined as:
```
σ(x) = 1/[1+e^(-x)]
```
![Dense layer](./finalreport_files/Dense.jpg)

The second type is the convolutional neural network, or CNN. This network is different from the default dense layer as groups of neighbouring inputs will be passed into each filter, such that related information will be processed together. Here, the activation function used is the `ReLU` function, which will only return the input if it is more than 0:
```
ReLU(x) = max(0,x)
```
Usually, the CNN layer would be followed by a MaxPool layer, which will take the maximum of the outputs of adjacent CNN cells so as to reduce the effect of noise or small changes to the input data. CNNs are commonly used for image classification as regions of the image can be processed together.
![CNN layer](./finalreport_files/CNN.jpg)

The third type of model is the Long-Short Term Memory model, or LSTM. This is a type of Recurrent Neural Network, where the results of the evaluation in one cell is passed on to the next, therefore causing earlier information processed to affect later operations. For LSTM, there is another memory path for information to pass on from cell to cell, which facilitates information storage within the LSTM layer. Furthermore, it has 3 more filters to regulate the information that is passed on between cells, namely:
- The forget gate, which prevents unimportant information to be passed on to the next cell
- The input gate, which determines the information to be passed on in the memory path of the LSTM layer
- The output gate, which determines the information to be passed on to the next cell

The aforementioned additional filters all use the `sigmoid` activation function. However, the original RNN filter now uses the `tanh` activation function, which is defined as
```
tanh(x) = [e^x-e^(-x)]/[e^x+e^(-x)]
```
![LSTM layer](./finalreport_files/LSTM.jpg)

Last but not least, we have the Gated Recurrent Unit, GRU. This layer ditches the additional memory path and condenses some of the filters of the LSTM such that less operations need to be made, speeding up evaluation time. Therefore, the filters in the GRU layer are:
- The reset gate, which combines the functionality of the forget gate and input gate of the LSTM and decides what new information to discard and add. The activation function used is the `sigmoid` function.
- The update gate, which is another gate to decide how much past information to forget. The activation function used is the `sigmoid` function
- The original RNN filter which uses the `tanh` activation function

![GRU layer](./finalreport_files/GRU.jpg)

The four models are chosen as they are some of the more common neural network models used today. In particular, we predicted that the LSTM and GRU would be useful since they would be able to remember previous evaluations, which will be helpful when processing the enemies spotted data.

After the evaluation, the neural network returns two values: the ideal yaw and pitch values that the player should be facing in that situation.

## Dataset and Features

```js
// writes game state to text file after every tick
// in demo_parser/app.js
```

An example of 1 datapoint on our dataset:
```
tick116863
1701.1904296875,997.8906860351562,1.9261016845703125
3.4002685546875,157.12646484375
spotted6
hold1
-2009.73876953125,1518.663818359375,87.60804748535156,102993
334.4256591796875,1617.818603515625,6.078970909118652,112577
334.4256591796875,1617.818603515625,6.078970909118652,112613
894.9175415039062,2470.05859375,160.48446655273438,112679
595.3279418945312,2594.00244140625,95.53994750976562,114295
595.138427734375,2592.861572265625,95.56367492675781,114369
```

```py
# loading demo information from text files at Python side
# in nn_training/load_data.py
```

## Machine Learning Development
To code our models, we used the tensorflow machine learning library, which comes with many built-in optimised neural network models that we can use.

In creating our model, we used the `tf.keras.Model` object since it contains specialised functions for compilation, fitting, evaluation and prediction, simplifying the building and training process of our models. Using the aforementioned object, each new layer would be linked to previous layers like this:
```
new_layer = <tf.keras.layer object>(params)(prev_layer)
```
As seen in the snippet below, the preprocessing layer and main neural network layers are defined with functions that can be customised, while the output of the main neural network layer will be passed into 2 branches of 1 dense layer each, the outputs from which being the final predictions for the yaw and pitch values. The `tf.keras.Model` object is then initialised with the list of inputs (from the preprocessing layer) and list of outputs (yaw and pitch outputs from the 2 dense layer branches).
```py
# initialising the model
# in nn_training/keras_model.py
```

The preprocessing layer is simply a list of `tf.keras.layers.Input` objects, one for each of the 68 inputs mentioned above.
```py
# general preprocessing layer
# in nn_training/keras_model.py
```

For the main neural network layers, we stringed the relevant built-in keras layers provided by tensorflow back-to-back. We used 5 layers of each neural network model for our training, though it is possible for us to specify a different number of layers for this function. Listed below are the keras layers used for each of the types of models we experimented with.
- Dense: `tf.keras.layers.Dense`
- CNN: `tf.keras.layers.Conv1D`, `tf.keras.layers.Dropout` & `tf.keras.layers.MaxPool1D`
- LSTM: `tf.keras.layers.LSTM`
- GRU: `tf.keras.layers.GRU`

```py
# main neural network layers for dense model
# other models are defined in similar ways
# in nn_training/keras_model.py
```

As we created a different branched model for our 4th experiment, we needed to change up the formats of the preprocessing and neural network layers. The inputs for the player information and spotted enemy information was split up, while the two branches had to be defined separately before being concatenated at a later layer.
```py
# preprocessing layer for branched model
# in nn_training/branched_model.py
```
```py
# main neural network layers for branched model
# in nn_training/branched_model.py
```

When using the model for prediction, the inputs also have to be preprocessed first by trimming the enemy spotted data if there are more than 15 sets of it, or by padding the enemy spotted data if there is less.
```py
# prediction with the model
# in nn_training/keras_model.py
```

Although the `tf.keras.Model` object has already greatly condensed the development process, we still found that there was a steep learning curve as we had little knowledge about manipulating tensors, and found the documentation and error messages difficult to read. Hence, the debugging process involved quite a lot of trial and error based on suggested code snippets from Stack Overflow

## Training Experiments and Results
For our first experiment, we fed all of our inputs through 5 layers of each model type. Due to limited preprocessing, we fed in the ticks where each enemy was spotted, instead of the time difference between the current tick and the tick where the enemy is spotted. We also used the kd ratio of each match as supplementary weights to the evaluation.
![Experiment 1](./finalreport_files/Experiment1.jpg)

In the second experiment, we improved our preprocessing bit by feeding the time difference between the current tick and the tick when the enemy is spotted into our model, as well as only taking spotted enemy players into account. We also decreased the tick interval of our data from 100 ticks to 32 ticks such that more data points are used to train our models.
![Experiment 2](./finalreport_files/Experiment2.jpg)

In the third experiment, we decided to exclude the kd ratio as we figured that since we are already using data from professional players, there wasn’t much need to differentiate between their proficiency. We also decided to stop training the dense and CNN models since we felt that
- The Dense layer was too simple
- The CNN layer would probably take into account of information that belonged to different sets of enemy data, therefore possibly confusing the model by allowing it to associate unrelated sets of data
- The LSTM and GRU would be more suited for the nature of our dataset.

![Experiment 3](./finalreport_files/Experiment3.jpg)

For our fourth experiment, we decided to first evaluate the player information and spotted enemy information separately, before merging them in a later layer. Here, we only used the RNN models to evaluate the spotted enemy information – since this is where the memory functions of RNNs are most important – while dense layers are used in other parts.
![Experiment 4](./finalreport_files/Experiment4.jpg)

Each experiment was trained for 10 epochs.

Unfortunately, we have not been able to get a satisfactory accuracy value for all 4 of our experiments. However, the accuracy of 0% is not completely representative of the accuracy of the model’s outputs. This is because the eye angle pitch and yaw values the model outputs do not have to completely match the correct pitch and yaw values, but rather just be in the same region. For example, an output pitch and yaw value that deviates from the correct output we provide it by just 1pixel would be deemed as incorrect and affect the accuracy, but such precision is realistically unnecessary. As the pitch and yaw values are also floating point integers, it is unlikely that they would match exactly, leading to this phenomenon.

Since all of our demo files are retrieved from matches in the same map, it can be quite certain that our models are probably overfitted to the layout of the map. However, we thought about this before and decided to go ahead with this since we figured that it would have been difficult for us to load all of the necessary demo files for our model to be able to play on multiple CSGO maps and even if we managed to do that, we fear that the differences between the maps would only confuse our model. If we were to expand our project to work on other CSGO maps in the future, we would probably have to train different models for each of the maps such that the predictions made would be more specialised.

## Application Deep Dive

```cpp
// function to locate memory addresses of client and engine
// in MemoryManager.h
```
```cpp
// waiting for F5 and reading information from memory
// in main.cpp
```

```cpp
// writing inputs to the model in text file
// in main.cpp (cont'd from previous c++ snippet)
```

```py
# main python program loop
# in main.py
```

```cpp
// reading model outputs from text file
// in main.cpp (cont'd from previous c++ snippet)
```

```cpp
// moving the user's view angle
// in main.cpp
```

## Team Effort
Gerrard:
- Retrieving demofiles
- C++ program to send information between CSGO and Python program

Luck Heng:
- Neural network development
- Python program to send information between neural network and C++ program

## Conclusion
Overall, this project has been extremely insightful in beginning research into possible applications of machine learning into teaching beginners in CSGO how to play the game. Working on CSAI has shed light into the world of applications interfacing with games and the core principles behind machine learning development. If we had a higher budget and more time, we would likely look into the following areas for improvement:
- Using cloud computing and better machines to increase our resources and decrease the training time
- Using larger and more diverse datasets in order to
  - Allow our model to group certain regions of the maps together
  - Train more models that will be able to work on different maps
  - Train specific models to mimic certain playstyles of professional players
- Creating custom neural network layers that are better able to process the data from the demofiles
