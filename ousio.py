from SVD import svd, svd_visualizations
from LSAEmbedding import lsa
from JSONCharacterEncoding import extract_possible_char_names as ext
import json
import pandas as pd
import numpy as np



# copy/pasted from lsa.py
prefixes = ["mr.", "mrs.", "ms.", "dr.", "mme.", "rev.", "lt.", "col.",
            "hon.", "st."]



# read in the raw text
text = ext._open_book_text_file('data/stranger_things_prepro.txt')


# # make character name dict (only do this once!)
# # ext._make_char_name_dict(text, 'data', 'characters')


# # once character name dict exists, just read it in to save time
# chars_string = open("data/charac.json", "r")
# chars_dict = json.load(chars_string)


# char_names = ['mike','will','lucas','dustin','el','vecna','steve','nancy','robin','erica',
#               'max','jonathan','hopper','joyce','argyle','yuri','demogorgon','karen','lonnie',
#               'billy','eddie','jason','patrick','chrissy','barb','vickie','alexei','murray',
#               'victor','fred','jane','terry','keith','dmitri','ted', 'holly', 'harrington',
#               'michael','bob', 'suzie','byers','henderson','sinclair','jim','eleven','owens',
#               'maxine','munson','creel','henry','one','six','newby','mind flayer','eight',
#               'scott', 'barbara','brenner','papa']



char_names = ['mike','will','lucas','dustin','eleven','vecna','steve','nancy','robin','erica',
              'max','jonathan','hopper','joyce','argyle','yuri','demogorgon','karen','lonnie',
              'billy','eddie','jason','patrick','chrissy','barb','vickie','alexei','murray',
              'victor','fred','terry','keith','dmitri','ted', 'holly', 
              'bob', 'suzie',
              'one','six','mind flayer','eight',
              'scott','brenner']


# try out lsa
# enc_matrix_list = lsa.run_LSA(text, chars_dict['char_names'], prefixes)
# output_df = lsa.use_LSA_words_in_matrix(enc_matrix_list, chars_dict['char_names'])

enc_matrix_list = lsa.run_LSA(text, char_names, prefixes)
output_df = lsa.use_LSA_words_in_matrix(enc_matrix_list, char_names)

output_df.to_json("lsa.json")


path_to_df_of_data = "lsa.json"
data_df = pd.read_json(path_to_df_of_data)

data_df = svd.subtract_mean(data_df)
df, U, D, V, Sig, X, remakeX = svd.run_SVD(data_df)
svd.write_array_to_npy(U, "U.npy")
svd.write_array_to_npy(D, "D.npy")
svd.write_array_to_npy(V, "V.npy")



V = np.load("V.npy")
data_df = pd.read_json("lsa.json")
vectordf, plotguy = svd_visualizations.vector_barchart(data_df.columns, V[0, :], 12)
# svd_visualizations.vector_barchart(data_df.columns, V[1, :], 15)



# vectordf, plotguy = svd_visualizations.vector_barchart(trait_columns_relabeled,V[2,:],10)
print(vectordf.columns)

print(vectordf['Trait'])



# prefixes = ["mr.", "mrs.", "ms.", "dr.", "mme.", "rev.", "lt.", "col.",
#             "hon.", "st."]


# # read in the two corpora
# # with open('data/one_grams_clean_full.txt') as f:
# #     words1 = f.readlines()

# #open text file in read mode
# text_file = open("data/stranger_things.txt", "r")
 
# #read whole file to a string
# data = text_file.read()
 
# #close file
# text_file.close()
    
# L = lsa.run_LSA(data, ['mike','steve'], prefixes)
    
# # words_df = pd.DataFrame(words1)


# # s = svd.run_SVD(words_df)
    









