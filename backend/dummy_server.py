from flask import Flask
from flask import jsonify, request
#from flask_cors import cross_origin
from flask_cors import CORS
from os.path import join
import pickle
from keras.preprocessing.text import text_to_word_sequence
import json
import operator

import redis

r=redis.StrictRedis(host='localhost', port=6379, db=0)

app = Flask("diacritic")
CORS(app)

# DATA_PATH = "../data/"
# SPELLINGS_FILE = 'books_spellings_v2.pickle'
# SPELLINGS_FILE = 'books_spellings_v2_small.pickle'
#
# print("loading spelling data")
# with open(join(DATA_PATH,SPELLINGS_FILE), 'rb') as pickle_file:
#     spellings_lower = pickle.load(pickle_file)
#
# print("starting")
# print(spellings_lower['acasa'])


@app.route('/', methods=['POST'])
def dummy_response():

    def json_p(json_thing, sort=True, indents=4):
        """
        return pretty json of json_thing
        """
        if type(json_thing) is str:
            return json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)

        return json.dumps(json_thing, sort_keys=sort, indent=indents)

    def choose_best_alternative( input_word ):
        """
        return:
        - the key with the highest value associated
        - a dict with curated spellings as keys and relative freq as values
        - sum of all sum_occurences
        """

        alt_d = {}
        curated_alternatives = {}
        most_frequent = False
        sum_occurences = 0


        found_record = r.get(input_word.lower())
        if not found_record:
            return most_frequent, curated_alternatives, sum_occurences

        alt_d = json.loads(found_record)

        sum_occurences = sum(alt_d.values())
        if sum_occurences < 100:
            return most_frequent, curated_alternatives, sum_occurences

        most_frequent = max(alt_d.keys(), key=lambda x: alt_d[x])
        for w,c in alt_d.items():
            relative_freq = c/sum_occurences*100
            if relative_freq>5:
                curated_alternatives[w]=relative_freq

        return most_frequent, curated_alternatives, sum_occurences



    request_data = request.get_json()
    type(request_data)
    print("data", request_data)
    print("values", request.values)
    for k, v in request_data.items():
        print(k,v)

    try:
        input_text =  request_data['text']
    except KeyError:
        input_text = ""

    response_stats = []
    response_text = []

    output_text = input_text
    for input_word in text_to_word_sequence(input_text,
                                        filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n',
                                        lower=False):
        # print(f"{input_word}: {spellings_lower[input_word.lower()]}")
        # found_stats = spellings_lower[input_word.lower()]

        suggested_word, dict_alternatives, count_occurencies = choose_best_alternative(input_word)

        input_word_start_with_capital = input_word[0].isupper()
        response_stats.append({
            'word': input_word,
            'alternatives': dict_alternatives,
            'counts': count_occurencies,
            'suggested': suggested_word,
            'starts_capital': input_word_start_with_capital
        })

        print("sugestion ", suggested_word)
        # response_text.append(suggested_word or input_word)
        if suggested_word:
            suggestion = suggested_word
            if input_word_start_with_capital:
                suggestion = suggested_word[0].upper() + suggested_word[1:]
            output_text = output_text.replace(input_word, suggestion, 1)

    #print(response_stats)
    print(" ".join(output_text))
    print(json_p(response_stats))


    # dummy_data = {'text': " ".join(response_text)}
    response_data = {
        'text': output_text,
        'word_info': response_stats
        }
    return jsonify(response_data)
