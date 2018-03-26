from os.path import join
import pickle
from collections import Counter

import redis
import json

DATA_PATH = "../data/"
SPELLINGS_FILE = 'books_spellings_v2.pickle'

SMALL_SPELLINGS_FILE = 'books_spellings_v2_small.pickle'

print("loading spelling data")


spellings_lower = Counter()
spellings_lower_extract = Counter()

print("loading spelling gata from pickle file")

with open(join(DATA_PATH,SPELLINGS_FILE), 'rb') as pickle_file:
    spellings_lower = pickle.load(pickle_file)
print("done")


r = redis.StrictRedis(host='localhost', port=6379, db=0)

r.set('xalex','este cel mai tare')
print(r.get('xalex'))
#exit()

print("building kv pairs")
i=0
for k,v  in spellings_lower.items():
    i+=1
    r.set(k,json.dumps(v))

print("done ", i)

with open(join(DATA_PATH, SMALL_SPELLINGS_FILE), 'wb') as pickle_file:
    pickle.dump(spellings_lower_extract, pickle_file)
