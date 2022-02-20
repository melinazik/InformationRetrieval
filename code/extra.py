
import time
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from pywebio.output import put_text, put_markdown, put_html
from pywebio.input import input, radio
import matplotlib.pyplot as plt
import plotly.express as px

# data_path = '../data/Proceedings_Processed.csv'
data_path = '../data/Proceedings_1989_2020_Processed.csv'

def main(data_path):
    df = pd.read_csv(data_path)
    number_of_rows = df.shape[0]

    put_markdown ('# **Επιλέξτε το διάστημα ετών που θέλετε να δείτε την μεταβολή των σημαντικότερων θεματικών (1989 - 2020).**')
    start_year = int(input('Από (1989 -): '))
    end_year = int(input('Μέχρι (- 2020): '))

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

        speeches.clear()

    end = time.time()
    x_coordinates = []
    y_coordinates = []

    y_coordinates.append(10.0)
    
    for year in range(start_year, end_year + 1):
        x_coordinates.append(year)

    for i in range(end_year - start_year ):
        y_coordinates.append(len(list(set(lsi[0]).intersection(lsi[i])))/2)   

    print(x_coordinates)
    print(y_coordinates)
    fig = px.scatter(x=x_coordinates, y=y_coordinates, title="Ομοιότητες Μεταξύ Σημαντικών Θεματικών")

    html = fig.to_html(include_plotlyjs="require", full_html=False)
    put_html(html)  

    put_text("Χρόνος εκτέλεσης: " + f"{round(end - start, 2)} sec.\n")
