import tensorflow as tf
from numpy import transpose
from load_data import INPUT_COLS

"""
To load and predict the models,
    model = load_model(<filename>)
    model.predict(<data>)
"""

class KerasModel():
    def __init__(self, name="BaseModel", version=1, units=128, steps=1, dropout=0.2, activation="sigmoid", nlayers=1, batch_size=3):
        self.name = name; self.version = version
        self.units = units; self.steps=steps; self.dropout = dropout; self.activation = activation
        self.nlayers = nlayers; self.batch_size = batch_size
        self.inputs, self.preprocess = self.build_preprocess()
        self.core_layers = self.create_model()
        self.yaw_output = tf.keras.layers.Dense(1, name="target_yaw")(self.core_layers)
        self.pitch_output = tf.keras.layers.Dense(1, name="target_pitch")(self.core_layers)
        self.model = tf.keras.Model(
            inputs=self.inputs,
            outputs=[self.yaw_output, self.pitch_output],
            name=self.name
        )

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=[tf.keras.metrics.Accuracy()]
        )

    def build_preprocess(self):
         columns = [tf.keras.layers.Input(shape=1, name=title) for title in INPUT_COLS]
         concatenated = tf.keras.layers.concatenate(columns)
         return columns, tf.reshape(
            concatenated,
            tf.constant([self.batch_size, self.steps, len(columns)])
        )

    def create_model(self):
        prev_layer = self.preprocess
        for _ in range(self.nlayers):
            new_layer = tf.keras.layers.Dense(
                self.units,
                activation=self.activation
            )(prev_layer)
            prev_layer = new_layer
        return prev_layer

    def train(self, data, epochs=1, **kwargs):
        inputs, targets, weights = data
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath="./checkpoints/{}-{}layers.ckpt".format(self.name, self.nlayers),
            save_weights_only=True
        )
        self.model.fit(
            {title: inputs[i] for i, title in enumerate(INPUT_COLS)},
            {"target_yaw": targets[0], "target_pitch": targets[1]},
            batch_size=self.batch_size,
            epochs=epochs,
            sample_weight=[weights, weights],
            callbacks=[checkpoint],
            **kwargs
        )

    def test(self, data, **kwargs):
        inputs, targets, weights = data
        self.model.evaluate(
            {title: inputs[i] for i, title in enumerate(INPUT_COLS)},
            {"target_yaw": targets[0], "target_pitch": targets[1]},
            batch_size=self.batch_size,
            sample_weight=[weights, weights],
            **kwargs
        )

    def predict(self, inputs, spotted_cap=15, **kwargs):
        """
        inputs should be a list of lists of shape
        [tick, self_x, self,y, self_z, self_yaw, self_pitch, spotted, hold, p1_x, p1_y, p1_z, p1_tick, p2_x, ...]
        It will cap out at 15 values for the other spotted players
        """
        rem_len = len(inputs)-8
        zeroes = [0.0]*len(inputs[0])
        if rem_len < spotted_cap*4:
            inputs.append([zeroes]*(spotted_cap*4-rem_len))
        inputs = inputs[:8] + inputs[-spotted_cap*4:]
        predictions = self.model.predict(
            {title: inputs[i] for i, title in enumerate(INPUT_COLS)},
            batch_size=self.batch_size,
            **kwargs
        )
        return transpose(predictions)[0][0]

    def summary(self):
        self.model.summary()

    def save(self):
        filename = "./saved_models/{}-{}layers-v{}.h5".format(self.name, self.nlayers, self.version)
        self.model.save(filename)

    def load(self, filename):
        if filename[-3:] == ".h5":
            self.model = tf.keras.models.load_model(filename)
        if filename[-5:] == ".ckpt":
            self.model.load_weights(filename)

class KerasCNN(KerasModel):
    def __init__(self, name="CNN", kernel_size=1, **kwargs):
        self.kernel_size = kernel_size
        super().__init__(name, **kwargs)

    def create_model(self):
        prev_layer = self.preprocess
        for _ in range(self.nlayers):
            conv_layer = tf.keras.layers.Conv1D(
                self.units,
                self.kernel_size,
                activation=self.activation
            )(prev_layer)
            drop_layer = tf.keras.layers.Dropout(self.dropout)(conv_layer)
            prev_layer = drop_layer
        return prev_layer

class KerasLSTM(KerasModel):
    def __init__(self, name="LSTM", activation="tanh", **kwargs):
        super().__init__(name, activation=activation, **kwargs)

    def create_model(self):
        prev_layer = self.preprocess
        for _ in range(self.nlayers):
            lstm_layer = tf.keras.layers.LSTM(
                self.units,
                dropout=self.dropout,
                activation=self.activation,
                return_sequences=True
            )(prev_layer)
            prev_layer = lstm_layer
        return prev_layer

class KerasGRU(KerasModel):
    def __init__(self, name="GRU", activation="tanh", **kwargs):
        super().__init__(name, activation=activation, **kwargs)

    def create_model(self):
        prev_layer = self.preprocess
        for _ in range(self.nlayers):
            gru_layer = tf.keras.layers.GRU(
                self.units,
                dropout=self.dropout,
                activation=self.activation,
                return_sequences=True
            )(prev_layer)
            prev_layer = gru_layer
        return prev_layer

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
        KerasModel(version=version, nlayers=nlayers)
    model.load(filename)
    return model

if __name__ == "__main__":
    from load_data import load_demo
    from filenames import TEST_FILES
    model = load_model("./saved_models/BaseModel-5layers.h5")
    demofiles = TEST_FILES[:1]
    inputs, _, _ = load_demo(demofiles)
    print(model.predict([col[:3] for col in inputs]))
