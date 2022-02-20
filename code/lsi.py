import time

import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

dataPath = '../data/Proceedings_1989_2020_Processed.csv'
# dataPath = '../data/Proceedings_Processed.csv'

def main(dataPath):
    df = pd.read_csv(dataPath)
    number_of_rows = df.shape[0]
    
    start = time.time()

    processed_list = []
    for s in range(number_of_rows):
        processed_list.append(str(df['speech'][s]))

    vect = TfidfVectorizer()
    tfidf_matrix = vect.fit_transform(processed_list)

    lsa_model = TruncatedSVD(n_components=10, n_iter=10)

    lsa_top = lsa_model.fit_transform(tfidf_matrix)
    l = lsa_top[0]

    terms = vect.get_feature_names()

    for i, component in enumerate(lsa_model.components_):
        zipped = zip(terms, component)
        terms_key = sorted(zipped, key = lambda t: t[1], reverse=True)[:10]
        terms_list = list(dict(terms_key).keys())
        print("Θεματική Περιοχή " + str(i)+": ", terms_list)
        print("\n")

    # for i, topic in enumerate(l):
    #     print("Θεματική Περιοχή ", i ," : ", topic * 100)

    #     print(lsa_model.components_.shape) # (no_of_topics * no_of_words)
    #     print(lsa_model.components_)


    end = time.time()

    print(end-start)

main(dataPath)
