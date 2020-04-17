import tensorflow as tf
from load_data import INPUT_COLS

models = {
    "BaseModel": BaseModel,
    "CNN": CNN,
    "LSTM": LSTM,
    "GRU": GRU
}

class BaseModel(tf.keras.Sequential):
    def __init__(self, nlayers=1):
        tf.keras.Sequential.__init__(self)
        self.build_preprocess()
        self.create_model(nlayers=nlayers)
        self.add(tf.keras.layers.Dense(1)) # TODO: change number of outputs based on output classes

        # Loss and optimiser functions – can be changed if needed
        self.loss_obj = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        self.optimiser = tf.keras.optimizers.Adam()

    def create_model(self, nlayers=1):
        # Can be varied to build different types of models
        for _ in range(nlayers):
            self.add(tf.keras.layers.Dense(128, activation="sigmoid"))

    def build_preprocess(self):
        columns = []
        for title in INPUT_COLS:
            columns.append(tf.feature_column.numeric_column(title, shape=[len(INPUT_COLS)]))
        self.add(tf.keras.layers.DenseFeatures(columns))

    def train(self, data, epochs=1, print_freq=25):
        train_loss = []
        train_acc = []

        for epoch in range(epochs):
            epoch_loss_avg = tf.keras.metrics.Mean()
            epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

            for features, targets, weights in data:
                # Features – model inputs
                # Targets – target outputs
                # Weights – KD ratio

                # Model evaluation
                predictons = self(features, training=True)
                # Loss – scaled based on KD ratio
                # Loss for data with higher KD ratio will be higher, so model will tend more to them
                loss = self.loss_obj(y_true=targets, y_pred=predictions, sample_weights=weights)
                # Optimisation
                gradients = tf.GradientTape().gradient(loss, self.trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, model.trainable_variables))

                # Update loss and accuracy
                epoch_loss_avg.update_state(loss_value, sample_weights=weights)
                epoch_accuracy.update_state(targets, predictions, sample_weights=weights)

            # Update details of epoch
            train_loss.append(epoch_loss_avg.result())
            train_acc.append(epoch_accuracy.result())

            # Save after every epoch
            model.save_weights("./checkpoints/{}.ckpt".format(self.__name__))

            # Print status at specific intervals
            if epoch % print_freq == 0:
                print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch, epoch_loss_avg.result(), epoch_accuracy.result()))

    def test(self, data):
        test_accuracy = tf.keras.metrics.Accuracy()
        for features, targets, weights in data:
            prediction = tf.argmax(self(features, training=False))
            test_accuracy.update_state(targets, predictions, sample_weights=weights)
        print("Test accuracy: {:.3%}".format(test_accuracy.result()))

class CNN(BaseModel):
    def create_model(self, nlayers=1):
        for _ in range(nlayers):
            self.add(tf.keras.layers.Conv2D(128, (3,3), activation="sigmoid"))
            self.add(tf.keras.layers.Dropout(0.2))
            self.add(tf.keras.layers.MaxPool2D())

class LSTM(BaseModel):
    def create_model(self, nlayers=1):
        for _ in range(nlayers):
            self.add(tf.keras.layers.LSTM(128, dropout=0.2)) # default activation is tanh

class GRU(BaseModel):
    def create_model(self, nlayers=1):
        for _ in range(nlayers):
            self.add(tf.keras.layers.GRU(128, dropout=0.2)) # default activation is tanh
