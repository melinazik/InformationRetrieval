# -*- coding: utf-8 -*-
import csv

from pywebio.output import put_text, put_markdown
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import heapq
import time
from pywebio.input import input
import os.path


def main(data_path):

    k = int(input('Πόσα top-k θες να σου επιστραφούν;', type='text'))

    start = time.time()
    data_tf_idf_path = '../data/Proceedings_1989_2020_Processed_tf_idf.csv'
    if not os.path.isfile(data_tf_idf_path):
        preprocessing(data_path)

    df = pd.read_csv(data_tf_idf_path)
    number_of_rows = df.shape[0]

    # here we define our document collection
    # this is an array of strings
    documents = []
    for i in range(number_of_rows):
        documents.append(df['Speeches'][i])

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # define the doc-doc similarity matrix based on the cosine distance
    ddsim_matrix = cosine_similarity(tfidf_matrix[:], tfidf_matrix)

    heap = []
    # create a max heap that contains top-k tf-idf scores
    for i in range(number_of_rows):
        for j in range(i + 1, number_of_rows):
            # If we have not yet found k items, or the current item is larger than the smallest item on the heap
            if len(heap) < k or ddsim_matrix[i][j] > heap[0][0]:
                # If the heap is full, remove the smallest element on the heap.
                if len(heap) == k:
                    heapq.heappop(heap)
                # add the current element as the new smallest.
                heapq.heappush(heap, [ddsim_matrix[i][j], i, j])

    put_markdown('# **Αποτελέσματα**')  # print results
    put_markdown("# **Top-" + str(k) + "** ")
    for i in range(len(heap)):
        put_text(df['Name'][heap[i][1]].upper(), " - ", df['Name'][heap[i][2]].upper())
    end = time.time()
    put_text("Χρόνος εκτέλεσης: " + f"{round(end - start, 2)} sec.\n")


def preprocessing(data_path):
    df = pd.read_csv(data_path)
    number_of_rows = df.shape[0]
    members_speeches = {}
    for i in range(number_of_rows):
        name = str(df['member_name'][i])
        speech = str(df['speech'][i])
        if name in members_speeches:
            members_speeches[name] += " " + speech
        else:
            members_speeches[name] = " "

    header = ['Name', 'Speeches']
    csv_file = '../data/Proceedings_1989_2020_Processed_tf_idf.csv'
    try:
        with open(csv_file, 'w', encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for key, value in members_speeches.items():
                writer.writerow([key, value])
    except IOError:
        print("I/O error")
