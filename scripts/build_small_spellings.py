from os.path import join
import pickle
from collections import Counter

DATA_PATH = "../data/"
SPELLINGS_FILE = 'books_spellings_v2.pickle'

SMALL_SPELLINGS_FILE = 'books_spellings_v2_small.pickle'

print("loading spelling data")


spellings_lower = Counter()
spellings_lower_extract = Counter()

with open(join(DATA_PATH,SPELLINGS_FILE), 'rb') as pickle_file:
    spellings_lower = pickle.load(pickle_file)

words = """acasa
romania este o tara europeana
Ambasadorul SUA la Natiunile Unite, Nikky Haley, a declarat miercuri ca Statele Unite considera ca Rusia este responsabila pentru atacul chimic din Marea Britanie asupra fostului spion rus si a fiicei sale. De asemenea, Consiliul de Securitate al ONU ar trebui sa ia masuri, mai spune aceasta, potrivit reuters.com.Premierul britaqnic Theresa May a anuntat, intr-un discurs tinut in parlament, ca va expulza 23 de diplomati rusi. May a adaugat ca este cel mai masiv val de expulzari din ultimii peste 30 de ani. Ambasadorul Moscovei la Londra a avertizat ca vor exista masuri reciproce daca Regatul Unit expulzeaza diplomati rusi.
"""
for x in words.lower().split():
    spellings_lower_extract[x] =  spellings_lower[x]

print(spellings_lower_extract)

with open(join(DATA_PATH, SMALL_SPELLINGS_FILE), 'wb') as pickle_file:
    pickle.dump(spellings_lower_extract, pickle_file)
