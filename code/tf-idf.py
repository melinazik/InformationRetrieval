# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import heapq
import time


dataPath = '../data/Proceedings_100000_Processed.csv'


class Member:
    def __init__(self, name, party, speech):
        self.name = name
        self.party = party
        self.speeches = []
        self.speeches.append(speech)
        self.str_speeches = speech

    def add_speech(self, speech):
        self.speeches.append(speech)
        self.str_speeches += speech

    def print(self):
        print("Name", self.name, "Party", self.party, "Speeches", len(self.speeches))


def main():
    df = pd.read_csv(dataPath)
    number_of_rows = df.shape[0]
    members = []
    members_names = []
    start = time.time()
    for i in range(number_of_rows):
        name = str(df['member_name'][i])
        party = str(df['political_party'][i])
        speech = str(df['speech'][i])
        found = False
        for x in members:
            if x.name == name:
                x.add_speech(speech)
                found = True
        if not found:
            members.append(Member(name, party, speech))
            members_names.append(name)
    end = time.time()
    print("Members found", end-start)
    # here we define our document collection
    # this is an array of strings

    start = time.time()
    documents = []
    for x in members:
        documents.append(x.str_speeches)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # define the doc-doc similarity matrix based on the cosine distance
    print("This is the doc-doc similarity matrix :")
    ddsim_matrix = cosine_similarity(tfidf_matrix[:], tfidf_matrix)
    print(ddsim_matrix)

    heap = []
    k = 5
    # create a max heap that contains top-k tf-idf scores
    for i in range(len(members)):
        for j in range(i+1, len(members)):
            # If we have not yet found k items, or the current item is larger than the smallest item on the heap
            if len(heap) < k or ddsim_matrix[i][j] > heap[0][0]:
                # If the heap is full, remove the smallest element on the heap.
                if len(heap) == k:
                    heapq.heappop(heap)
                # add the current element as the new smallest.
                heapq.heappush(heap, [ddsim_matrix[i][j], i, j])

    print(heap)
    print("top", k)
    for i in range(len(heap)):
        print(members[heap[i][1]].name," - ", members[heap[i][2]].name)
    end = time.time()
    print("", end-start)


main()


