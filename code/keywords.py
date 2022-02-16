# -*- coding: UTF-8 -*-
import time
import pandas as pd
import spacy
from string import punctuation
from collections import Counter
import unicodedata as ud

dataPath = '../data/Proceedings_500.csv'
dataSize = 500

# start = time.time()
# df = pd.read_csv(dataPath)
# print(df.shape)
# df = df[-10000:]
# df.to_csv(dataPath, encoding='utf-8', index=False)
# end = time.time()
# print("Read csv without chunks: ",(end-start),"sec")
# df = pd.read_csv(dataPath)
# print(df)


def extract_keywords(nlp, sequence, stop_words, special_tags: list = None):
    """ Takes a Spacy core language model,
    string sequence of text and optional
    list of special tags as arguments.

    If any of the words in the string are
    in the list of special tags they are immediately
    added to the result.

    Arguments:
        sequence {str} -- string sequence to have keywords extracted from

    Keyword Arguments:
        tags {list} --  list of tags to be automatically added (default: {None})

    Returns:
        {list} -- list of the unique keywords extracted from a string
    """
    result = []

    # custom list of part of speech tags we are interested in
    # we are interested in proper nouns, nouns, and adjectives
    # edit this list of POS tags according to your needs.
    pos_tag = ['PROPN', 'NOUN', 'ADJ']

    # create a spacy doc object by calling the nlp object on the input sequence
    doc = nlp(sequence.lower())

    # if special tags are given and exist in the input sequence
    # add them to results by default
    if special_tags:
        tags = [tag.lower() for tag in special_tags]
        for token in doc:
            if token.text in tags:
                result.append(token.text)
    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if token.lemma_ in stop_words or token.text in punctuation:  # REMOVE STOPWORDS AND PUNCTUATION SYMBOLS
                continue
            if token.pos_ in pos_tag:
                final_chunk = final_chunk + token.lemma_ + " "
        if final_chunk:
            result.append(final_chunk.strip())

    for token in doc:
        if token.lemma_ in stop_words or token.text in punctuation:  # REMOVE STOPWORDS AND PUNCTUATION SYMBOLS
            continue
        if token.pos_ in pos_tag:
            result.append(token.lemma_)
    dict_counter = dict(Counter(list(result)))
    return dict_counter


def main():
    start = time.time()
    nlp = spacy.load("el_core_news_sm")
    speeches = []
    df = pd.read_csv(dataPath, delimiter=',')
    number_of_rows = df.shape[0]
    stop_words = nlp.Defaults.stop_words
    stop_words.update({"κ.", "κύριος", "κυρία", "λόγο"})

    choice = input('Εύρεση keywords, α)Ανα ομιλία, β)Ανά βουλευτή, γ)Ανα κόμμα  ')
    if choice == 'α':
        number_of_speech = int(input('Δώσε αριθμό ομιλίας, μπορεί να είναι απο το 0-' + str(number_of_rows-1)))
        if 0 <= number_of_speech < number_of_rows:
            speeches.append(df['speech'][number_of_speech])
    elif choice == 'β':
        member_name = input('Δώσε όνομα βουλευτή ')
        member_name = member_name.lower()
        d = {ord('\N{COMBINING ACUTE ACCENT}'): None}  # remove τόνους
        name = ud.normalize('NFD', member_name).translate(d)
        for i in range(number_of_rows):
            if df['member_name'][i] == name:
                speeches.append(df['speech'][i])
    elif choice == 'γ':
        member_name = input('Δώσε όνομα κόμματος ')
        member_name = member_name.lower()
        d = {ord('\N{COMBINING ACUTE ACCENT}'): None}  # remove τόνους
        name = ud.normalize('NFD', member_name).translate(d)
        for i in range(number_of_rows):
            if df['political_party'][i] == name:
                speeches.append(df['speech'][i])

    print(len(speeches))
    total_keywords = {}
    for speech in speeches:
        # nlp.max_length = len(speech) + 100
        keywords = extract_keywords(nlp, speech, stop_words)
        for key in total_keywords:
            if key in keywords:
                total_keywords[key] = total_keywords[key] + keywords[key]
        total_keywords = {**keywords, **total_keywords}
    if len(speeches) == 0:
        print("Δεν βρέθηκαν ομιλίες")
    else:
        total_keywords = sorted(total_keywords, key=total_keywords.get, reverse=True)[:15]
        print(total_keywords)
    end = time.time()
    print("Time", end-start)

main()
