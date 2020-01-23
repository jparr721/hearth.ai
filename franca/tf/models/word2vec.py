"""
Word2Vec is an embedding model for pre trained embeddings
for text processing purposes
"""

from typing import Dict, Any

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.layers import Input, Dense, Reshape, Dot, Embedding


class Word2Vec:
    class SimilarityCallback:
        def __init__(
            self,
            model: Model,
            sim_iter: int,
            reverse_dictionary: Dict[Any, Any],
            validation_examples: np.array,
            vocab_size: int,
            top_k=8,
        ):
            """
            SimilarityCallback is useful for training embeddings
            by visually showing euclidean relationships between
            words during training

            Parameters
            ----------
            model : tf.keras.Model
                The model we are evaluating
            sim_iter : int
                The number of times to run the sim for and calculate
            reverse_dictionary : Dict[Any, Any]
                The reversed dict of characterized words
            validation_examples : np.array
                Our array of validation examples randomly picked from our
                dataset
            vocab_size : int
                The size of our vocabulary we are working with
            top_k : int
                The number of nearest neighbors to check during training
            """
            self.model = model
            self.sim_iter = sim_iter
            self.reverse_dictionary = reverse_dictionary
            self.validation_examples = validation_examples
            self.vocab_size = vocab_size
            self.top_k = top_k

        def run_sim(self):
            for i in range(self.sim_iter):
                validation_word = self.reverse_dictionary[
                    self.validation_examples[i]
                ]
                sim = self.get_sim(
                    self.validation_examples[i], self.vocab_size, self.model
                )
                nearest = (-sim).argsort()[1 : self.top_k + 1]
                log_str = f"Nearest to {validation_word}"
                for k in range(self.top_k):
                    close_word = self.reverse_dictionary[nearest[k]]
                    log_str = f"{validation_word} {close_word}"
                print(log_str)

        @staticmethod
        def get_sim(validation_word_index: int, vocab_size: int, model: Model):
            sim = np.zeros((vocab_size,))

            # These match our inputs from the model
            in_arr1 = np.zeros((1,))
            in_arr2 = np.zeros((1,))

            in_arr1[0,] = validation_word_index

            for i in range(vocab_size):
                in_arr2[0,] = i
                out = model.predict_on_batch((in_arr1, in_arr2))
                sim[i] = out
            return sim

    def __init__(
        self,
        window_size=3,
        vector_dim=300,
        epochs=int(1e6),
        validation_size=16,
        validation_window=100,
    ):
        # How many words around the word to use for context
        self.window_size = window_size

        # The embedding vector size
        self.vector_dim = vector_dim

        # Our number of training epochs
        self.epochs = epochs

        # Validation params
        self.validation_size = validation_size

        # How many words around the word to use for context
        self.validation_window = validation_window

        # Example picker
        self.validation_examples = np.random.choice(
            self.validation_window, self.validation_size, replace=False
        )

    def make_datasets_from_frequency_vector(
        self, frequency_vector: Dict[str, int]
    ):
        sorted_index = dict(sorted(frequency_vector.items()))

        self.vocab_size = len(frequency_vector)

        token_to_index = {}

        for word, count in frequency_vector.items():
            token_to_index[word] = len(token_to_index)

        self.reversed_word_index = {v: k for k, v in token_to_index.items()}
        self.sorted_index = sorted_index
        self.token_to_index = token_to_index

    def word2vec(self):
        """
        word2vec is our model which implements the word2vec architecture
        """

        # A sampling table allows the skipgrams to be evenly distributed
        # between true context and negative samples
        sampling_table = sequence.make_sampling_table(
            self.vocab_size, sampling_factor=0.01
        )

        # Genrate skip grams for context within a window
        # This will give us couples of words and contexts of the following form
        # [[100, 4], [10, 10]...] where the 0-index is the word and 1-index is
        # the context. We then check if this is correct with the labels of form
        # [1, 0, 1, 0, 1, 1, 0, 1, 0, 0] which inform our embedding during
        # training
        # Legend:
        # 1 - True context
        # 0 - Negative sample
        word_indexes = list(self.token_to_index.values())
        self.couples, self.labels = sequence.skipgrams(
            word_indexes,
            self.vocab_size,
            window_size=self.window_size,
            sampling_table=sampling_table,
        )

        # Take the couples and zip them to get the target and context
        word_target, word_context = zip(*self.couples)

        # Convert them to an np array of ints instead of standard list type
        self.word_target = np.array(word_target, dtype="int32")
        self.word_context = np.array(word_context, dtype="int32")

        # Generate our custom embedding layer
        input_target = Input((1,))
        input_context = Input((1,))

        embedding = Embedding(
            self.vocab_size, self.vector_dim, input_length=1, name="embedding"
        )

        # Transpose our input vectors to take a dot product next

        # Now, map our embedding over the target to fit our vector dim
        target = embedding(input_target)
        target = Reshape((self.vector_dim, 1))(target)

        # Now, map our embedding over the context to fit our vector dim
        context = embedding(input_context)
        context = Reshape((self.vector_dim, 1))(context)

        # Construct the cosine similarity model to use in validation
        # Keras dot does this by default when normalize = True both vectors
        # become l2_normed and then the dot product becomes the cosine
        # proximity since l2 makes comparisons euclidean
        similarity = Dot(axes=0, normalize=True)

        # Dot product layers to get the similarity
        dot_product = Dot(axes=1, normalize=False)([target, context])
        dot_product = Reshape((1,))(dot_product)

        # Create our sigmoid output layer
        output = Dense(1, activation="sigmoid")(dot_product)

        # Now, generate our model
        model = Model(inputs=[input_target, input_context], outputs=output)

        # Binary cross entropy because our embedding labels are binary
        # rmsprop trains quickly by decaying the average of squared gradients
        # link https://ruder.io/optimizing-gradient-descent/index.html#rmsprop
        model.compile(loss="binary_crossentropy", optimizer="rmsprop")

        # Next, calculate our similarity during validation
        similarity = Dot(axes=1, normalize=True)([target, context])
        validation_model = Model(
            inputs=[input_target, input_context], outputs=similarity
        )

        sim_cb = self.SimilarityCallback(
            validation_model,
            self.validation_size,
            self.reversed_word_index,
            self.validation_examples,
            self.vocab_size,
        )

        arr1 = np.zeros((1,))
        arr2 = np.zeros((1,))
        arr3 = np.zeros((1,))

        for count in range(self.epochs):
            idx = np.random.randint(0, len(self.labels) - 1)
            arr1[0,] = self.word_target[idx]
            arr2[0,] = self.word_context[idx]
            arr3[0,] = self.labels[idx]

            loss = model.train_on_batch([arr1, arr2], arr3)

            if count % 100 == 0:
                print(f"Iter: {count}, loss: {loss}")
            if count % 500 == 0:
                sim_cb.run_sim()
