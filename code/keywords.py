# -*- coding: UTF-8 -*-
import time
import pandas as pd
from collections import Counter
import unicodedata as ud
import re
import heapq
from pywebio.input import input, radio
from pywebio.output import put_text, put_html, put_markdown


def top_k_keywords(speeches, k):
    """
    Args:
        speeches: a dictionary that contains speeches per year
        k: the number of most important keywords that should be returned

    Returns: top-k keywords from each year, and top-k keywords through all years.
    """
    total_keywords = Counter({})
    keywords_per_year = {}
    for year in speeches:
        yearly_speeches = speeches[year]
        keywords_per_year[year] = Counter({})
        for speech in yearly_speeches:
            keywords = extract_keywords(speech)
            keywords_per_year[year].update(keywords)
        total_keywords.update(keywords_per_year[year])
        keywords_per_year[year] = heapq.nlargest(k, keywords_per_year[year], key=keywords_per_year[
            year].get)  # keep top- k keywords using a max heap
    total_keywords = heapq.nlargest(k, total_keywords, key=total_keywords.get)  # keep top- k keywords using a max heap
    return keywords_per_year, total_keywords


def extract_keywords(speech):
    """
     Args:
        speech: a speech

    Returns: keywords from a specific speech and how many times each word appears.
    """
    result = re.sub("[^\w]", " ", speech).split()
    dict_counter = Counter(list(result))
    return dict_counter


def find_speech(number_of_speech, number_of_rows, df):
    """

    Args:
        number_of_speech: number of speech they are searching
        df: the records of greek parliament
        number_of_rows: member of rows that df has

    Returns: a specific speech

    """

    speech = {}
    number_of_speeches = 0
    if 0 <= number_of_speech < number_of_rows:
        year = df['sitting_date'][number_of_speech][-4:]
        speech[year] = [df['speech'][number_of_speech]]
        number_of_speeches = 1
    return speech, number_of_speeches


def find_speeches(df, name, category, number_of_rows):
    """

    Args:
        df: the records of greek parliament
        number_of_rows: member of rows that df has
        name: member's name or politician's party name for whom they searching speeches
        category: politician_party or member_name (depends of what they are searching for)

    Returns: all speeches of a specific category and how many they are

    """
    name = name.lower()
    d = {ord('\N{COMBINING ACUTE ACCENT}'): None}  # remove τόνους
    name = ud.normalize('NFD', name).translate(d)
    speeches = {}
    number_of_speeches = 0
    last_year = '0'
    for i in range(number_of_rows):
        if df[category][i] == name:
            year = df['sitting_date'][i][-4:]  # speech's year
            if last_year < year:
                speeches[year] = []
                last_year = year
            speeches[year].append(df['speech'][i])  # save speech in a dictionary according speech's year
            number_of_speeches += 1
    return speeches, number_of_speeches


def main(dataPath):
    df = pd.read_csv(dataPath)
    number_of_rows = df.shape[0]
    start = time.time()
    put_markdown("# **Εύρεση keywords**")
    choice = radio("Θέλεις να βρεις λέξεις-κλειδιά: ", options=['ανά ομιλία', 'ανά βουλευτή', 'ανά κόμμα'])
    if choice == 'ανά ομιλία':  # find keywords from a specific speech
        number_of_speech = int(
            input('Δώσε αριθμό ομιλίας, μπορεί να είναι απο το 0-' + str(number_of_rows - 1) + ' ', type='text'))
        speeches, number_of_speeches = find_speech(number_of_speech, number_of_rows, df)
    elif choice == 'ανά βουλευτή':  # find keywords from all the speeches of a politician
        member_name = input('Δώσε όνομα βουλευτή ', type='text')
        speeches, number_of_speeches = find_speeches(df, member_name, 'member_name', number_of_rows)
    else:  # find keywords from all the speeches of a politician party
        party_name = input('Δώσε όνομα κόμματος ', type='text')
        speeches, number_of_speeches = find_speeches(df, party_name, 'political_party', number_of_rows)

    put_markdown('# **Αποτελέσματα**')  # print results
    put_text("Βρέθηκαν", number_of_speeches, "ομιλίες")
    put_html("<br>")
    if number_of_speeches == 0:
        put_text("Δεν βρέθηκαν ομιλίες")
        return

    k = int(input('Πόσες λέξεις-κλειδιά θες να σου επιστραφούν;', type='text'))
    keywords_per_year, keywords = top_k_keywords(speeches, k)
    end = time.time()

    put_html("<b>Λέξεις-κλειδιά: </b>")
    text = keywords[0]
    for i in range(1, len(keywords)):
        text += ", " + keywords[i]
    put_text(text + ".")
    put_html("<br>")

    if number_of_speeches > 1:
        put_html("<b>Λέξεις-κλειδιά ανά έτος: </b> <br> ")
        for year in keywords_per_year:
            put_html("<b>" + year + "</b>")
            text = keywords_per_year[year][0]
            for i in range(1, len(keywords_per_year[year])):
                text += ", " + keywords_per_year[year][i]
            put_text(text + ".")
            put_html("<br>")
    put_text("Χρόνος εκτέλεσης: " + f"{round(end - start, 2)} sec.\n")
