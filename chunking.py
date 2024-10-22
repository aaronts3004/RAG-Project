'''
    The plain text needs to be processed and specifically chunked into smaller units of text
    to ease the embedding into the vector database and thus influence the quality of the retrieval.
    First, the naive chunking method is implemented:
    - the open-source spaCy module performs the tokenization on a sentence-basis,
        while potentially keeping some context about each specific sentence
'''

from spacy.lang.en import English # see https://spacy.io/usage for install instructions


def naive_sentence_chunking(text):
    nlp = English() # Load a Language object containing all components and data needed to process text

    # Add a sentencizer pipeline, see https://spacy.io/api/sentencizer/ 
    nlp.add_pipe("sentencizer")

    # Calling the nlp object on a string of text will return a processed Doc
    doc = nlp(text)

    print(type(doc))
    
    for token in doc:
        print(token.text, token.pos_, token.dep_)

    # After tokenization, spaCy can parse and tag a given Doc


    


