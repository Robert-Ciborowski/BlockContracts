# Name: Binance Pump and Dump Detector
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Detects pump and dumps from Binance crypto data.

# from __future__ import annotations
import json
from typing import List
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from matplotlib import pyplot as plt
import tensorflow.keras.layers
import numpy as nd

from ml.Hyperparameters import Hyperparameters

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class AmbiguityDetector:
    _classificationThreshold: float
    hyperparameters: Hyperparameters
    listOfMetrics: List
    vocabularySize: int
    embeddingDimension: int
    maxInputLength: int
    tokenizer: Tokenizer
    exportPath = "./exports/ambiguitydetector"

    def __init__(self):
        self._buildMetrics()

    def setup(self, classificationThreshold, hyperparameters: Hyperparameters,
              vocabularySize: int, embeddingDimension: int, maxInputLength: int,
              sentencesWithWords):
        self._classificationThreshold = classificationThreshold
        self.hyperparameters = hyperparameters
        self.vocabularySize = vocabularySize
        self.embeddingDimension = embeddingDimension
        self.maxInputLength = maxInputLength
        self.tokenizer = Tokenizer(num_words=vocabularySize, oov_token="<OOV>")
        self.tokenizer.fit_on_texts(sentencesWithWords)

    def setupWithDefaultValues(self, sarcasm_src):
        pd.options.display.max_rows = 10
        pd.options.display.float_format = "{:.1f}".format

        print("Ran the import statements.")

        with open(sarcasm_src, 'r') as f:
            datastore = json.load(f)

        sentences = []
        labels = []
        urls = []

        for item in datastore:
            sentences.append(item['headline'])
            labels.append(item['is_sarcastic'])
            urls.append(item['article_link'])

        # updated hypermater values in the final form
        vocab_size = 1000
        embedding_dim = 16
        max_length = 16
        training_size = 20000
        training_sentences = np.array(sentences[0:training_size])

        self.setup(0.28, Hyperparameters(0.15, 30, 50), vocab_size,
                   embedding_dim, max_length, training_sentences)

    def detect(self, sentences: List[str]) -> bool:
        count = len(sentences)

        if count == 0:
            return False

        input_sequences = self.tokenizer.texts_to_sequences(sentences)
        padding_input = pad_sequences(input_sequences, truncating='post',
                                      padding='post',
                                      maxlen=self.maxInputLength)

        results = self._predict(padding_input)
        total = 0.0

        for i in results:
            total += i

        print(total / count)
        return total / count >= self._classificationThreshold

    """
    Creates a brand new neural network for this model.
    """

    def createModel(self, layerParameters: List):
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Embedding(self.vocabularySize,
                                                 self.embeddingDimension,
                                                 input_length=self.maxInputLength))
        self.model.add(tf.keras.layers.GlobalAveragePooling1D())

        # model = tf.keras.Sequential([
        #     tf.keras.layers.Embedding(vocab_size, embedding_dim,
        #                               input_length=max_length),
        #     tf.keras.layers.GlobalAveragePooling1D(),
        #     tf.keras.layers.Dense(24, activation='relu'),
        #     tf.keras.layers.Dense(1, activation='sigmoid')
        # ])

        count = 0
        for parameter in layerParameters:
            self.model.add(tf.keras.layers.Dense(units=parameter.units,
                                                 activation=parameter.activation,
                                                 name="Hidden_" + str(count)))
            count += 1

        # Define the output layer.
        self.model.add(tf.keras.layers.Dense(units=1, input_shape=(1,),
                                             activation=tf.sigmoid,
                                             name="Output"))

        # model.compile(loss='binary_crossentropy', optimizer='adam',
        #               metrics=['accuracy'])

        # Compiles the model with the appropriate loss function.
        self.model.compile(
            loss='binary_crossentropy', optimizer='adam',
            metrics=self.listOfMetrics)

    def trainModel(self, training_sentences, training_labels, testing_sentences,
                   testing_labels):
        """Train the model by feeding it data."""
        sequences = self.tokenizer.texts_to_sequences(training_sentences)
        padded_training = pad_sequences(sequences, truncating='post',
                                        padding='post',
                                        maxlen=self.maxInputLength)
        testing_sequences = self.tokenizer.texts_to_sequences(testing_sentences)
        padding_testing = pad_sequences(testing_sequences, truncating='post',
                                        padding='post',
                                        maxlen=self.maxInputLength)

        history = self.model.fit(padded_training, training_labels,
                                 batch_size=self.hyperparameters.batchSize,
                                 epochs=self.hyperparameters.epochs,
                                 shuffle=True,
                                 validation_data=(
                                 padding_testing, testing_labels))

        # The list of epochs is stored separately from the rest of history.
        epochs = history.epoch

        # To track the progression of training, gather a snapshot
        # of the model's mean squared error at each epoch.
        hist = pd.DataFrame(history.history)
        return epochs, hist

    """
    Evalutaes the model on features.
    Returns:
        Scalar test loss (if the model has a single output and no metrics)
        or list of scalars (if the model has multiple outputs
        and/or metrics). The attribute `model.metrics_names` will give you
        the display labels for the scalar outputs.
    """

    def _predict(self, features):
        return self.model.predict(features)

    def plotCurve(self, epochs, hist, metrics):
        """Plot a curve of one or more classification metrics vs. epoch."""
        # list_of_metrics should be one of the names shown in:
        # https://www.tensorflow.org/tutorials/structured_data/imbalanced_data#define_the_model_and_metrics

        plt.figure()
        plt.xlabel("Epoch")
        plt.ylabel("Value")

        for m in metrics:
            x = hist[m]
            plt.plot(epochs[1:], x[1:], label=m)

        plt.legend()
        plt.show()

    def _buildMetrics(self):
        self.listOfMetrics = ["accuracy"]

    def export(self):
        self.model.save_weights(self.exportPath)

    def load(self):
        self.model.load_weights(self.exportPath)
