from flask import Flask
from flask import jsonify, request
#from flask_cors import cross_origin
from flask_cors import CORS
from os.path import join
import pickle
from keras.preprocessing.text import text_to_word_sequence


app = Flask("diacritic")
CORS(app)

DATA_PATH = "../data/"
SPELLINGS_FILE = 'books_spellings_v2.pickle'
SPELLINGS_FILE = 'books_spellings_v2_small.pickle'

print("loading spelling data")
with open(join(DATA_PATH,SPELLINGS_FILE), 'rb') as pickle_file:
    spellings_lower = pickle.load(pickle_file)

print("starting")
print(spellings_lower['acasa'])

@app.route('/', methods=['POST'])
def dummy_response():

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

    for input_word in text_to_word_sequence(input_text.lower(),
                                        filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n',
                                        lower=False):
        # print(f"{input_word}: {spellings_lower[input_word.lower()]}")
        found_stats = spellings_lower[input_word.lower()]
        response_stats.append(found_stats)
        w,c  = found_stats.most_common(1)[0]
        print("sugestinon ", w)
        response_text.append(w)

    print(response_stats)
    print(" ".join(response_text))


    dummy_data = {'text': " ".join(response_text)}
    return jsonify(dummy_data)
