
import time
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from pywebio.output import put_text, put_markdown, put_html
from pywebio.input import input, radio

# data_path = '../data/Proceedings_Processed.csv'
data_path = '../data/Proceedings_1989_2020_Processed.csv'

def similarities(A, B):
    A = A.lower()
    B = B.lower()
    list1 = A.split(" ")
    list2 = B.split(" ")
    return len(list(set(list1) & set(list2)))

def main(data_path):
    df = pd.read_csv(data_path)
    number_of_rows = df.shape[0]

    put_markdown = ('# **Επιλέξτε το διάστημα ετών που θέλετε να δείτε την μεταβολή των σημαντικότερων θεματικών.**')
    start_year = int(input('Από: '))
    end_year = int(input('Μέχρι: '))

    lsi = []

    speeches = []         

    start = time.time()
    for year in range(start_year, end_year + 1):
        
        for i in range(number_of_rows):

            if str(year) in str(df['sitting_date'][i]):
                speeches.append(str(df['speech'][i]))

        if speeches:
            vect = TfidfVectorizer()
            tfidf_matrix = vect.fit_transform(speeches)

            lsa_model = TruncatedSVD(n_components=1, n_iter=7)

            lsa_top = lsa_model.fit_transform(tfidf_matrix)
            l = lsa_top[0]

            terms = vect.get_feature_names_out()

            for i, component in enumerate(lsa_model.components_):
                zipped = zip(terms, component)
                terms_key = sorted(zipped, key = lambda t: t[1], reverse=True)[:10]
                terms_list = list(dict(terms_key).keys())
                lsi.append(terms_list)
                put_text(year)
                put_text(terms_list)

                # for i, topic in enumerate(l):
                #     put_text("Θεματική Περιοχή ", i ," : ", topic * 100)
                #     put_text(lsa_model.components_)
                #     put_text("\n")

        speeches.clear()

    
    # put_text(lsi)

main(data_path)