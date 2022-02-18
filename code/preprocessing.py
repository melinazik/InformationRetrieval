# -*- coding: UTF-8 -*-
import spacy
import string
import csv
import pandas as pd


def remove_stopwords(df, nlp, s):
    """ Removes stopwords and punctuation
    from all the speeches in the csv file
    given.

    Stores the new format of the speeches
    in a new csv file called "Proceedings_Processed.csv".

    Arguments:
        df : the csv object
        nlp : spaCy's greek tokenizer
        s: number of speech in df

    """

    stop_words = nlp.Defaults.stop_words
    stop_words.update({'κ.', 'κύριος', 'κυρία', 'λόγο', 'συνάδελφος', 'επιτροπή', 'βουλευτής', 'υπουργός',
                       'δικαιοσύνη', 'διαδικασία', 'κυβέρνηση', 'βουλή', 'πρόεδρος', 'υπουργείο', 'πολιτικός'})
    #  replace punctuation with space
    new_speech = df['speech'][s].translate(str.maketrans(' ', ' ', string.punctuation))

    # replace stopwords with space
    for word in new_speech.split(' '):
        if word in stop_words:
            if (" " + word + " ") in new_speech:
                new_speech = new_speech.replace(" " + word + " ", " ")
            elif (word + " ") in new_speech:
                new_speech = new_speech.replace(word + " ", " ")
            elif (" " + word) in new_speech:
                new_speech = new_speech.replace(" " + word, " ")
    return new_speech


def keep_noun_propn_adj(nlp, speech):
    """

    Args:
        nlp : spaCy's greek tokenizer
        speech: a speech stored in a string

    Returns: the nouns, proper nouns and
    adjectives of a speech

    """

    pos_tag = ['PROPN', 'NOUN', 'ADJ']
    result = []
    doc = nlp(speech)

    for token in doc:
        if token.pos_ in pos_tag:
            result.append(token.lemma_)
    new_speech = ' '.join(result)
    return new_speech


def preprocessing():  # TODO steaming!
    """ Removes stopwords and punctuation,
   lower case every word, keeps only
   nouns, proper nouns and adjectives
   from all the speeches in the csv file
   given.

   Stores the new format of the speeches
   in a new csv file called "Proceedings_Processed.csv".


   """

    dataPath = '../data/Proceedings_10000.csv'
    nlp = spacy.load("el_core_news_sm")

    df = pd.read_csv(dataPath)
    number_of_rows = df.shape[0]
    print(number_of_rows)

    # set header of new csv file
    header = ['member_name', 'sitting_date', 'parliamentary_period', 'parliamentary_session', 'political_party',
              'government', 'roles', 'member_gender', 'speech']

    data = []

    for s in range(number_of_rows):
        # create a list with all the elements in
        # column of a row of the csv file
        data_row = []

        # remove records that have NaN on basic attributes (member_name, politician_party, speech)
        if str(df['member_name'][s]) == 'nan' or str(df['political_party'][s]) == 'nan' or str(df['speech'][s]) == 'nan':
            break

        data_row.append(df['member_name'][s])
        data_row.append(df['sitting_date'][s])
        data_row.append(df['parliamentary_period'][s])
        data_row.append(df['parliamentary_session'][s])
        data_row.append(df['political_party'][s])
        data_row.append(df['government'][s])
        data_row.append(df['roles'][s])
        data_row.append(df['member_gender'][s])

        # remove stopwords
        new_speech = remove_stopwords(df, nlp, s)

        # lower
        new_speech = new_speech.lower()

        # keep only nouns, adjectives, proper nouns
        new_speech = keep_noun_propn_adj(nlp, new_speech)

        data_row.append(new_speech)
        data.append(data_row)

    # store the new data in a new csv file
    with open('../data/Proceedings_100000_Processed.csv', 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


preprocessing()
