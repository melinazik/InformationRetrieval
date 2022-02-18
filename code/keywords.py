# -*- coding: UTF-8 -*-
import time
import pandas as pd
from collections import Counter
import unicodedata as ud
import re
import heapq
from pywebio.input import input
from pywebio.output import put_text, put_html, put_markdown

# TODO πως αλλάζουν οι λέξεις κλειδιά στον χρόνο

# dataPath = '../data/Proceedings_1989_2020_Processed.csv'
dataPath = '../data/Proceedings_100000_Processed.csv'


# start = time.time()
# df = pd.read_csv(dataPath)
# print(df.shape)
# df = df[-10000:]
# df.to_csv(dataPath, encoding='utf-8', index=False)
# end = time.time()
# print("Read csv without chunks: ",(end-start),"sec")
# df = pd.read_csv(dataPath)
# print(df)


# def remove_stopwords(df, stop_words):
#    """ Removes stopwords and punctuation
#    from all the speeches in the csv file
#    given.
#    Stores the new format of the speeches
#    in a new csv file called "Proceedings_Processed.csv".
#    Arguments:
#        df : the csv object
#        stop_words : list of stopwords
#    """
#
#    number_of_rows = df.shape[0]
#
#    # set header of new csv file
#    header = ['member_name', 'sitting_date', 'parliamentary_period', 'parliamentary_session', 'political_party',
#              'government', 'roles', 'member_gender', 'speech']
#
#    data = []
#
#    for s in range(number_of_rows):
#
#        # create a list with all the elements in
#        # column of a row of the csv file
#        data_row = []
#
#        data_row.append(df['member_name'][s])
#        data_row.append(df['sitting_date'][s])
#        data_row.append(df['parliamentary_period'][s])
#        data_row.append(df['parliamentary_session'][s])
#        data_row.append(df['political_party'][s])
#        data_row.append(df['government'][s])
#        data_row.append(df['roles'][s])
#        data_row.append(df['member_gender'][s])
#
#        #  replace punctuation with space
#        new_speech = df['speech'][s].translate(str.maketrans(' ', ' ', string.punctuation))
#
#        # replace stopwords with space
#        for word in new_speech.split(' '):
#            if word in stop_words:
#                new_speech = new_speech.replace(" " + word + " ", " ")
#
#        data_row.append(new_speech)
#        data.append(data_row)
#
#    # store the new data in a new csv file
#    with open('../data/Proceedings_Processed.csv', 'w', encoding="utf-8", newline='') as f:
#        writer = csv.writer(f)
#        writer.writerow(header)
#        writer.writerows(data)


def top_k_keywords(speeches, k):
    """
    Args:
        speeches: a list that contains speeches
        nlp: spaCy's greek tokenizer
        k: the number of most important keywords that should be returned

    Returns: top-k keywords from specific speeches.
    """
    total_keywords = Counter({})
    for speech in speeches:
        keywords = extract_keywords(speech)
        total_keywords.update(keywords)
    total_keywords = heapq.nlargest(k, total_keywords, key=total_keywords.get)  # keep top- k keywords using a max heap
    return total_keywords


def extract_keywords(speech):
    """
     Args:
        speech: a speech

    Returns: keywords from a specific speech and how many times each word appears.
    """
    if str(speech) == 'nan':
        return Counter({})

    result = re.sub("[^\w]", " ", speech).split()
    dict_counter = Counter(list(result))
    return dict_counter


def main():
    df = pd.read_csv(dataPath)
    number_of_rows = df.shape[0]
    speeches = []

    start = time.time()
    put_markdown("# **Εύρεση keywords**")
    choice = input('Θέλεις να βρεις λέξεις-κλειδιά: α)ανα ομιλία, β)ανά βουλευτή ή γ)ανα κόμμα. (Δώσε ως είσοδο το αντίστοιχο γράμμα.)', type='text')
    if choice == 'α':
        number_of_speech = int(input('Δώσε αριθμό ομιλίας, μπορεί να είναι απο το 0-' + str(number_of_rows - 1) + ' ', type='text'))
        if 0 <= number_of_speech < number_of_rows:
            speeches.append(df['speech'][number_of_speech])

    elif choice == 'β':
        member_name = input('Δώσε όνομα βουλευτή ', type='text')
        member_name = member_name.lower()
        d = {ord('\N{COMBINING ACUTE ACCENT}'): None}  # remove τόνους
        name = ud.normalize('NFD', member_name).translate(d)
        for i in range(number_of_rows):
            if df['member_name'][i] == name:
                speeches.append(df['speech'][i])
    elif choice == 'γ':
        member_name = input('Δώσε όνομα κόμματος ', type='text')
        member_name = member_name.lower()
        d = {ord('\N{COMBINING ACUTE ACCENT}'): None}  # remove τόνους
        name = ud.normalize('NFD', member_name).translate(d)
        for i in range(number_of_rows):
            if df['political_party'][i] == name:
                speeches.append(str(df['speech'][i]))

    put_markdown('# **Αποτελέσματα**')
    put_text("Βρέθηκαν", len(speeches), "ομιλίες")
    if len(speeches) == 0:
        put_text("Δεν βρέθηκαν ομιλίες")
        return

    k = int(input('Πόσες λέξεις-κλειδιά θες να σου επιστραφούν;', type='text'))
    keywords = top_k_keywords(speeches, k)
    put_html("<b>Λέξεις-κλειδιά: </b>")
    text = keywords[0]
    for i in range(1, k):
        text += ", " + keywords[i]
    put_text(text+".")
    end = time.time()
    put_text("Χρόνος εκτέλεσης: " + f"{round(end - start, 2)} sec.\n")


