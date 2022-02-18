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

dataPath = '../data/Proceedings_1989_2020_Processed.csv'
# dataPath = '../data/Proceedings_100000_Processed.csv'


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
