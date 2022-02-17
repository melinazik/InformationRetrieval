# -*- coding: UTF-8 -*-
import time
import pandas as pd
import spacy
import string
import csv
from string import punctuation
from collections import Counter
import unicodedata as ud

dataPath = '../data/Proceedings_500.csv'


# start = time.time()
# df = pd.read_csv(dataPath)
# print(df.shape)
# df = df[-10000:]
# df.to_csv(dataPath, encoding='utf-8', index=False)
# end = time.time()
# print("Read csv without chunks: ",(end-start),"sec")
# df = pd.read_csv(dataPath)
# print(df)

def remove_stopwords(df, stop_words):
    """ Removes stopwords and punctuation
    from all the speeches in the csv file
    given.

    Stores the new format of the speeches
    in a new csv file called "Proceedings_Processed.csv".

    Arguments:
        df : the csv object
        stop_words : list of stopwords

    """

    number_of_rows = df.shape[0]

    # set header of new csv file
    header = ['member_name', 'sitting_date', 'parliamentary_period', 'parliamentary_session', 'political_party',
              'government', 'roles', 'member_gender', 'speech']

    data = []

    for s in range(number_of_rows):

        # create a list with all the elements in
        # column of a row of the csv file
        data_row = []

        data_row.append(df['member_name'][s])
        data_row.append(df['sitting_date'][s])
        data_row.append(df['parliamentary_period'][s])
        data_row.append(df['parliamentary_session'][s])
        data_row.append(df['political_party'][s])
        data_row.append(df['government'][s])
        data_row.append(df['roles'][s])
        data_row.append(df['member_gender'][s])

        #  replace punctuation with space
        new_speech = df['speech'][s].translate(str.maketrans(' ', ' ', string.punctuation))

        # replace stopwords with space
        for word in new_speech.split(' '):
            if word in stop_words:
                new_speech = new_speech.replace(" " + word + " ", " ")

        data_row.append(new_speech)
        data.append(data_row)

    # store the new data in a new csv file
    with open('../data/Proceedings_Processed.csv', 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def top_k_keywords(speeches, nlp, k):
    """
    Args:
        speeches: a list that contains speeches
        nlp: spaCy's greek tokenizer
        k: the number of most important keywords that should be returned

    Returns: top-k keywords from specific speeches.
    """

    total_keywords = {}
    for speech in speeches:
        keywords = extract_keywords(nlp, speech)
        for key in total_keywords:
            if key in keywords:
                total_keywords[key] = total_keywords[key] + keywords[key]
        total_keywords = {**keywords, **total_keywords}

    total_keywords = sorted(total_keywords, key=total_keywords.get, reverse=True)[:k]
    return total_keywords


def extract_keywords(nlp, speech):
    """
     Args:
        speech: a speech
        nlp: spaCy's greek tokenizer

    Returns: keywords from a specific speech and how many times each word appears.
    """

    pos_tag = ['PROPN', 'NOUN', 'ADJ']
    result = []
    doc = nlp(speech.lower())

    for token in doc:
        if token.pos_ in pos_tag:
            result.append(token.lemma_)
    dict_counter = dict(Counter(list(result)))

    return dict_counter


def main():
    start = time.time()
    nlp = spacy.load("el_core_news_sm")
    speeches = []

    df = pd.read_csv('../data/Proceedings_Processed.csv')
    number_of_rows = df.shape[0]

    choice = input('Εύρεση keywords, α)Ανα ομιλία, β)Ανά βουλευτή, γ)Ανα κόμμα  ')
    if choice == 'α':
        number_of_speech = int(input('Δώσε αριθμό ομιλίας, μπορεί να είναι απο το 0-' + str(number_of_rows - 1) + ' '))
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

    print("Βρέθηκαν",  len(speeches), "ομιλίες")
    if len(speeches) == 0:
        print("Δεν βρέθηκαν ομιλίες")
        return

    keywords = top_k_keywords(speeches, nlp, 15)
    print(keywords)
    end = time.time()
    print(" Time: " + f"{round(end-start, 2)} sec.\n")


main()
