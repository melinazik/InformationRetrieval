from pywebio import start_server
from pywebio.input import input, radio, select
import keywords
import tf_idf

dataPath = '../data/Proceedings_1989_2020_Processed.csv'
# dataPath = '../data/Proceedings_100000_Processed.csv'


def webapp_main():
    option_keywords = 'Σημαντικότερες λέξεις κλειδιά'
    option_tf_idf = 'Τop-k ζεύγη με τον υψηλότερο βαθμό ομοιότητας'
    option_lsi = 'Σημαντικότερες θεματικές περιοχές'
    mode = radio("Αναζήτηση ", options=[option_keywords, option_tf_idf , option_lsi, '?'])
    if mode == option_keywords:
        keywords.main(dataPath)
    if mode == option_tf_idf:
        tf_idf.main(dataPath)
    if mode == option_lsi:
        lsi.main(dataPath)


if __name__ == '__main__':
    start_server(webapp_main, port=8080, debug=True)
