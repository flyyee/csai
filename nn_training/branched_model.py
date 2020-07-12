import tensorflow as tf
from keras_model import KerasModel
from load_data import INPUT_COLS

# see comments for keras_model first, it will be easier to understand this one
class KerasBranched(KerasModel):
    def __init__(self,
        name="BranchedModel",
        activation_dense="sigmoid",
        activation_rnn="tanh",
        spotted_branch="GRU",
        combine_at=3,
        **kwargs
    ):
        self.activation_dense = activation_dense; self.activation_rnn = activation_rnn;
        self.spotted_branch = spotted_branch; self.combine_at = combine_at # layer to concatenate the two branches
        super().__init__(name, **kwargs)
        assert self.combine_at <= self.nlayers

    def build_preprocess(self):
        # initialise input layers for player information and enemy information separately
        player_cols = [tf.keras.layers.Input(shape=1, name=title) for title in INPUT_COLS[:8]]
        spotted_cols = [tf.keras.layers.Input(shape=1, name=title) for title in INPUT_COLS[8:]]
        # pass in 2 different sets of input layers for initialisation and later layers
        return [player_cols, spotted_cols], [
            tf.reshape(tf.keras.layers.concatenate(player_cols), tf.constant([self.batch_size, self.steps, len(player_cols)])),
            tf.reshape(tf.keras.layers.concatenate(spotted_cols), tf.constant([self.batch_size, self.steps, len(spotted_cols)])),
        ]

    def create_model(self):
        player_prev, spotted_prev = self.preprocess
        for _ in range(self.combine_at):
            # processing of player information with Dense layers
            player_layer = tf.keras.layers.Dense(
                self.units,
                activation=self.activation_dense,
            )(player_prev)
            player_prev = tf.keras.layers.Dropout(self.dropout)(player_layer)

            # processing of enemy information with RNN layers (set to GRU by default)
            spotted_layer = \
                tf.keras.layers.GRU(
                    self.units,
                    activation=self.activation_rnn,
                    return_sequences=True
                )(spotted_prev) if self.spotted_branch == "GRU" else \
                tf.keras.layers.LSTM(
                    self.units,
                    activation=self.activation_rnn,
                    return_sequences=True
                )(spotted_prev) if self.spotted_branch == "LSTM" else \
                tf.keras.layers.SimpleRNN(
                    self.units,
                    activation=self.activation_rnn,
                    return_sequences=True
                )(spotted_prev)
            spotted_prev = tf.keras.layers.Dropout(self.dropout)(spotted_layer)

        # combine the evaluation of player information and enemy information
        combined_prev = tf.keras.layers.concatenate([player_prev, spotted_prev])
        for _ in range(self.nlayers-self.combine_at):
            # processing of combined information with Dense layers
            combined_layer = tf.keras.layers.Dense(
                self.units,
                activation=self.activation_dense,
            )(combined_prev)
            combined_prev = tf.keras.layers.Dropout(self.dropout)(combined_layer)
        # return the last layer to be piped into output dense layers
        return combined_prev

    def save(self):
        filename = "./saved_models/{}_{}-{}layers-v{}.h5".format(self.name, self.spotted_branch, self.nlayers, self.version)
        self.model.save(filename)
