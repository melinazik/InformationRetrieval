
import pandas as pd
import keywords
from pprint import pprint

# dataPath = '../data/Proceedings_Processed.csv'
# dataPath = '../data/Proceedings_1989_2020_Processed.csv'


def main(dataPath):
    df = pd.read_csv(dataPath)
    number_of_rows = df.shape[0]
    
    members = []
    members_names = []

    member_name = input('Δώσε όνομα βουλευτή ')
    speeches, number_of_speeches = keywords.find_speeches(df, member_name, 'member_name', number_of_rows)

    dates = []


    for s in range(number_of_rows):
        # create a list with all the elements in
        # column of a row of the csv file

        if df['member_name'][s] == member_name:
            dates.append( df['sitting_date'][s])


    earliest = min(dates[0])
    latest = max(dates[0])

    min_index = dates[0].index(earliest)
    max_index = dates[0].index(latest)

    # print(keywords.extract_only_keywords(df['speech'][min_index]))
    min_speech_keywords = keywords.extract_only_keywords(df['speech'][min_index])
    max_speech_keywords = keywords.extract_only_keywords(df['speech'][max_index])

    # print(min_index, max_index)
    # print(min_speech_keywords)

    # res = len(set(min_speech_keywords) & set(max_speech_keywords)) / float(len(set(min_speech_keywords) | set(max_speech_keywords))) * 100
    # TODO correct calculation
    res = 200.0 * len(set(min_speech_keywords) & set(max_speech_keywords)) / (len(min_speech_keywords) + len(max_speech_keywords))
    # print(set(min_speech_keywords) & set(max_speech_keywords))
    # # printing result
    # print(len(set(min_speech_keywords) & set(max_speech_keywords)))

# main(dataPath)