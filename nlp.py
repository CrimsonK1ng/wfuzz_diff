from gensim.test.utils import get_tmpfile
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import Similarity
from collections import Counter

"""Test Data"""

document_0 = "China has a strong economy that is growing at a rapid pace. However politically it differs greatly from the US Economy."
document_1 = "At last, China seems serious about confronting an endemic problem: domestic violence and corruption."
document_2 = "Japan's prime minister, Shinzo Abe, is working towards healing the economic turmoil in his own country for his view on the future of his people."
document_3 = "Vladimir Putin is working hard to fix the economy in Russia as the Ruble has tumbled."
document_4 = "What's the future of Abenomics? We asked Shinzo Abe for his views"
document_5 = "Obama has eased sanctions on Cuba while accelerating those against the Russian Economy, even as the Ruble's value falls almost daily."
document_6 = "Vladimir Putin is riding a horse while hunting deer. Vladimir Putin always seems so serious about things - even riding horses. Is he crazy?"
 
all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]
 
"""Test Data"""


def tokenize(data):
    """Splits string up into list of words

    Args:
        data (str): Document (URL Content)

    Returns:
        List: Words in document
    """
    return data.lower().split(' ')

def get_tokens(docs):
    """Tokenize documents

    Args:
        docs (List): List of documents
    
    Returns:
        List: List of list tokenized docs
    """
    tokenized_docs = list()
    for doc in docs:
        tokenized_docs.append(tokenize(doc))
    return tokenized_docs

def get_dictionary(tokenized):
    """Get Dictionary from tokenized docs

    Args:
        tokenized (List): List of tokenized docs 

    Returns:
        Dictionary: Dictionary of tokenized docs 
    """
    return Dictionary(tokenized) 

def get_corpus(dic, tokenized):
    """Generate corpus from tokenized documents using dictionary to generate bag of words

    Args:
        dic (Dictionary): Contains index for all tokenized docs
        tokenized (List): List of tokenized documents

    Returns:
        List: List of lists
    """
    return [dic.doc2bow(line) for line in tokenized]

def get_model(corpus):
    """Corpus of tokenized documents

    Args:
        corpus (List): BoW list of documents

    Returns:
        TfIdfModel: model to generate vectors
    """
    return TfidfModel(corpus)

def get_sim(model, corps):
    """get Similarity for corpus and model

    Args:
        model (TfIdfModel): TfIdf model to develop Similarity
        corps (Dictionary): Dictionary of words 

    Returns:
        [type]: [description]
    """
    return Similarity(None, model[corps], num_features=400)

def get_comp(index, model, corp, id):
    """Get comparison {0,1} or id compared to baseline

    Args:
        index (Similarity): Similarity object to query cosine similarity
        model (TfIdfModel): TfIdfModel to get the vector to query cosine similarity
        corp (Dictionary): Corpus to index to get proper list of BoW (Bag of Words) array 
        id (int): Index of string we want to compar 

    Returns:
        Float: {0,1} value comparing baseline 
    """
    return index[model[corp[id]]][0]


def get_comp_to_base(index, model, corp):
    """Return comparison for baseline to all other documents!

    Args:
        index (Similarity): Similarity object to query cosine similarity
        model (TfIdfModel): TfIdfModel to get the vector to query cosine similarity
        corp (Dictionary): Corpus to index to get proper list of BoW (Bag of Words) array 

    Returns:
        List: List of {0,1} value comparing corpus of documents to baseline 
    """
    return index[model[corp[0]]]

if __name__ == "__main__":
    """Example of how to use the above data to calculate similarity
    """
    tokenized = list()
    for doc in all_documents:
        tokenized.append(tokenize(doc))

    dic = Dictionary(tokenized)
    corpus = [dic.doc2bow(line) for line in tokenized]
    model = TfidfModel(corpus)
    print(model[corpus[0]])
    """
    This is specific to gensim and recommended to not overflow memory

    first arg is temp file which it will generate
    second arg is a multidimensional array of our "corpus" but in our case it is the value of the model applied to all strings
    third is the max length to run againstj
    """
    index = Similarity(None, model[corpus], num_features=400)
    print(index[model[corpus[1]]])
    for id, _ in enumerate(all_documents):
        print(index[model[corpus[1]]][id])