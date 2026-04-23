from PyMultiDictionary import MultiDictionary, DICT_MW
dictionary = MultiDictionary()
# meaning = ""/

def look_up(query:str):
    try:
        meaning = dictionary.meaning("en",query, dictionary=DICT_MW).items()
        if meaning:
            meaning = next(iter(meaning))
            meaning_data = {
                'type': meaning[0],
                'meaning': meaning[1][0]
            }
            return meaning_data
        else:
            dict_flag = False
            return dict_flag
    except:
        return "error"

# meaning을 verb, none 등으로 보기 좋게 나중에 표시하기

# meaning = dictionary.meaning("en","query", dictionary=DICT_MW).items()
# meaning = next(iter(meaning))
# print(meaning[0], meaning[1][0])

# print(look_up("fakfldjfs;"))