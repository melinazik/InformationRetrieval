from pywebio import start_server
from pywebio.input import input, radio, select
import keywords
import tf_idf
import lsi
import extra

data_path = '../data/Proceedings_1989_2020_Processed.csv'
# data_path = '../data/Proceedings_100000_Processed.csv'


def webapp_main():
    option_keywords = 'Σημαντικότερες λέξεις κλειδιά'
    option_tf_idf = 'Τop-k ζεύγη με τον υψηλότερο βαθμό ομοιότητας'
    option_lsi = 'Σημαντικότερες θεματικές περιοχές (LSI)'

    mode = radio("Αναζήτηση ", options=[option_keywords, option_tf_idf , option_lsi, '?'])

    if mode == option_keywords:
        keywords.main(data_path)
    elif mode == option_tf_idf:
        tf_idf.main(data_path)
    elif mode == option_lsi:
        lsi.main(data_path)


if __name__ == '__main__':
    start_server(webapp_main, port=8080, debug=True)
