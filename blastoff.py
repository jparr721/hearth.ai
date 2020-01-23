from engine.spiders.corpus.indexer import Indexer
from franca.tf.models.word2vec import Word2Vec

if __name__ == "__main__":
    w = Word2Vec()

    indexer = Indexer({}, "./freq.json")

    indexer.deserialize_index_file()

    w.make_datasets_from_frequency_vector(indexer.local_index)

    # Init our model and train
    w.word2vec()
