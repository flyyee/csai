import tensorflow as tf
from numpy import transpose
from load_data import INPUT_COLS

class KerasModel():
    def __init__(self, nlayers=1):
        self.inputs, self.preprocess = self.build_preprocess()
        self.core_layers = self.create_model(nlayers)
        self.yaw_output = tf.keras.layers.Dense(1, name="target_yaw")(self.core_layers)
        self.pitch_output = tf.keras.layers.Dense(1, name="target_pitch")(self.core_layers)
        self.model = tf.keras.Model(inputs=self.inputs, outputs=[self.yaw_output, self.pitch_output])

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True)
        )
        self.type = "BaseModel"

    def build_preprocess(self):
         columns = [tf.keras.layers.Input(shape=1, name=title) for title in INPUT_COLS]
         return columns, tf.keras.layers.concatenate(columns)

    def create_model(self, nlayers):
        prev_layer = self.preprocess
        for _ in range(nlayers):
            new_layer = tf.keras.layers.Dense(128, activation="sigmoid")(prev_layer)
            prev_layer = new_layer
        return prev_layer

    def train(self, data, batch_size=3, epochs=1, **kwargs):
        inputs, targets, weights = data
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath="./checkpoints/{}.ckpt".format(self.type),
            save_weights_only=True
        )
        self.model.fit(
            {title: inputs[i] for i, title in enumerate(INPUT_COLS)},
            {"target_yaw": targets[0], "target_pitch": targets[1]},
            batch_size=batch_size,
            epochs=epochs,
            sample_weight=[weights, weights],
            callbacks=[checkpoint],
            **kwargs
        )

    def test(self, data, batch_size=3, **kwargs):
        inputs, targets, weights = data
        self.model.evaluate(
            {title: inputs[i] for i, title in enumerate(INPUT_COLS)},
            {"target_yaw": targets[0], "target_pitch": targets[1]},
            batch_size=batch_size,
            sample_weight=[weights, weights],
            **kwargs
        )

    def predict(self, inputs, batch_size=3, **kwargs):
        predictions = self.model.predict(
            {title: inputs[i] for i, title in enumerate(INPUT_COLS)},
            batch_size=batch_size,
            **kwargs
        )
        return transpose(predictions)[0]

    def summary(self):
        self.model.summary()

    def save(self):
        filename = "./saved_models/{}.h5".format(self.type)
        self.model.save(filename)

    def load(self, filename):
        if filename[:-3] == ".h5":
            self.model = tf.keras.models.load_model(filename)
        if filename[:-5] == ".ckpt":
            self.model.load_weights(filename)

class KerasCNN(KerasModel):
    def __init__(self, nlayers=1):
        super().__init__(nlayers)
        self.type = "CNN"

    def create_model(self, nlayers):
        prev_layer = self.preprocess
        for _ in range(nlayers):
            conv_layer = tf.keras.layers.Conv2D(128, (3,3), activation="sigmoid")(prev_layer)
            drop_layer = tf.keras.layers.Dropout(0.2)(conv_layer)
            pool_layer = tf.keras.layers.MaxPool2D()(drop_layer)
            prev_layer = pool_layer
        return prev_layer

class KerasLSTM(KerasModel):
    def __init__(self, nlayers=1):
        super().__init__(nlayers)
        self.type = "LSTM"

    def create_model(self, nlayers):
        prev_layer = self.preprocess
        for _ in range(nlayers):
            lstm_layer = tf.keras.layers.LSTM(128, dropout=0.2)(prev_layer)
            prev_layer = lstm_layer
        return prev_layer

class KerasGRU(KerasModel):
    def __init__(self, nlayers=1):
        super().__init__(nlayers)
        self.type = "GRU"

    def create_model(self, nlayers):
        prev_layer = self.preprocess
        for _ in range(nlayers):
            gru_layer = tf.keras.layers.GRU(128, dropout=0.2)(prev_layer)
            prev_layer = gru_layer
        return prev_layer
