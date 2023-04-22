from SVD import svd, svd_visualizations
from LSAEmbedding import lsa
from JSONCharacterEncoding import extract_possible_char_names as ext
import json
import pandas as pd
import numpy as np


# read in text
text = ext._open_book_text_file('data/stranger_things.txt')

text = text.lower()


char_dict = {"michael":"mike",
             "jane":"eleven",
             "papa":"brenner",
             "harrington":"steve",
             "henderson":"dustin",
             "nance":"nancy",
             "barbara":"barb",
             "sinclair":"lucas",
             "henry":"vecna",
             "one":"vecna",
             "maxine":"max",
             "jim":"hopper"}


if "michael" in text:
    print("True")
else:
    print("False")


for key in char_dict.keys():
    text = text.replace(key, char_dict[key])


if "michael" in text:
    print("True")
else:
    print("False")
    
    
file = open('data/stranger_things_prepro.txt','w')
file.write(text)
file.close()