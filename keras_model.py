import tensorflow as tf
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

    def build_preprocess(self):
         columns = [tf.keras.layers.Input(shape=1, name=title) for title in INPUT_COLS]
         return columns, tf.keras.layers.concatenate(columns)

    def create_model(self, nlayers):
        prev_layer = self.preprocess
        for _ in range(nlayers):
            new_layer = tf.keras.layers.Dense(128, activation="sigmoid")(prev_layer)
            prev_layer = new_layer
        return new_layer

    def train(self, data, batch_size=3, epochs=1):
        inputs, targets, weights = data
        history = self.model.fit(
            {title: inputs[i] for i, title in enumerate(INPUT_COLS)},
            {"target_yaw": targets[0], "target_pitch": targets[1]},
            batch_size=batch_size,
            epochs=epochs,
            sample_weight=[weights, weights]
        )
        print("\nHistory: ", history.history)

    def test(self):
        pass

    def save(self):
        pass
