from pywebio import start_server
from pywebio.input import input
import keywords


def webapp_main():
    mode = input('1. Λέξεις κλειδιά, 2. tf-idf, 3. lsa ', type='text')
    if mode == '1':
        keywords.main()


if __name__ == '__main__':
    start_server(webapp_main, port=8080, debug=True)
