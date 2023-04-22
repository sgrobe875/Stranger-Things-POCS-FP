import pandas as pd
import matplotlib.pyplot as plt
import datetime
import json



# Keep track of how long things take
e = datetime.datetime.now()
print ("Beginning at %s:%s:%s" % (e.hour, e.minute, e.second))



# read in the table of VAD and PDS values
vad_pds = pd.read_csv('data/ousiometry_data_augmented.tsv', sep='\t')

# read in the text
with open('data/one_grams_clean_full.txt') as f:
    data = f.readlines()
    
    
# read in the preprocessed text
with open('data/one_grams_clean_full_prepro.txt') as f:
    prepro = f.readlines()
    

# prepro = prepro[:10000]

# for debugging purposes, only work with a subset of the data
# data = data[:1000]





#### taken & modified from assignment 20 ####

# takes in a list, returns the average of the values in the list
# ignores any None values in the calculation
def list_avg(l):
    return sum(filter(None, l)) / len(list(filter(None, l)))


# Looks through cleaned 1-grams and returns the values of interest across a sliding window
# Parameters: values_of_interest = list of all values we want to check; set to VAD & PDS by default
#             z = window size, 10^z; set to 2 for a window size of 100 by default
# Returns x list with midpoints used for plotting, as well as dictionary of window values
def sliding_window(values_of_interest = ['valence', 'arousal', 'dominance', 'power', 'danger', 'structure'], 
                   z = 2):
    
    # set window size using z
    window_size = int(10**z)
    
    # initialize variables
    words = data.copy()       # copy of list of 1-grams
    values_dict = {}          # dictionary to hold final results
        
    
    # set up the initial window (the first window_size 1-grams in the data set)
    # build list of all of the words
    window = []
    for i in range(window_size):
        window.append(words[0])
        words.pop(0)    
    
    # loop through each value of interest
    for value in values_of_interest:
        # list to hold value of each word in the window
        values_window = []
        # make a new copy of the words in the window so we can manipulate it
        window_copy = window.copy()
        
        # loop through each word in the window
        for i in range(window_size):
            
            # get its associated value from the vad_pds table
            try:
                values_window.append(float(vad_pds[value][vad_pds['word'] == window_copy[0][:-1].lower()]))
                
            # if the word isn't in the table, append None
            except TypeError:
                values_window.append(None)
            
            # remove the first word to slide the window
            window_copy.pop(0)

        values_dict[value] = {'window': values_window.copy(), 'values': [list_avg(values_window)]}
        # values_dict[value]['values'] = [list_avg(values_window)]
    
    # slide window by one word until we run out of words
    while len(words) > 0:
        # same procedure as above to get sentiment of the word in question
        for value in values_of_interest:
            
            values_window = values_dict[value]['window']
            
            try:
                values_window.append(float(vad_pds[value][vad_pds['word'] == words[0][:-1].lower()]))
                    
            except TypeError:
                values_window.append(None)
                
            values_window.pop(0)
            values_dict[value]['values'].append(list_avg(values_window))
            
        words.pop(0)

            
    # starting x value = midpoint of the window
    start_x = int(window_size/2)
    
        
    # set up x values running from midpoint of first window to midpoint of last window
    x = list(range(start_x, len(data)-start_x+1))
    

    # return x, sentiments
    return x, values_dict



# same as sliding_window, but only builds windows when the inputted character's 
# name is found in the window; works off of the preprocessed text
def sliding_window_character(char_name,
                             values_of_interest=['danger','power'], 
                             z = 2):
    
    # set window size using z
    window_size = int(10**z)
    
    # initialize variables
    words = prepro.copy()       # copy of list of 1-grams
    values_dict = {}            # dictionary to hold final results
        
    
    # set up the initial window (the first window_size 1-grams in the data set)
    # build list of all of the words
    window = []   # the list of all words in the window
    for i in range(window_size):
        window.append(words[0][:-1])
        words.pop(0)    
    
    # loop through each value of interest
    for value in values_of_interest:
        # list to hold value of each word in the window
        values_window = []
        # make a new copy of the words in the window so we can manipulate it
        window_copy = window.copy()
        
        # loop through each word in the window
        for i in range(window_size):
            # get its associated value from the vad_pds table
            try:
                values_window.append(float(vad_pds[value][vad_pds['word'] == window_copy[0][:-1].lower()]))
                
            # if the word isn't in the table, append None
            except TypeError:
                values_window.append(None)
        
            # remove the first word to slide the window
            window_copy.pop(0)
        
        if char_name in window:
            values_dict[value] = {'window': values_window.copy(), 'values': [list_avg(values_window)]}
        else:
            values_dict[value] = {'window': values_window.copy(), 'values': [None]}

    # slide window by one word until we run out of words
    while len(words) > 0:
        
        # slide window by one
        window.append(words[0][:-1])
        window.pop(0)

        
        # same procedure as above to get sentiment of the word in question
        for value in values_of_interest:
            
            values_window = values_dict[value]['window']
            
            try:
                values_window.append(float(vad_pds[value][vad_pds['word'] == words[0][:-1].lower()]))
                    
            except TypeError:
                values_window.append(None)
                
            values_window.pop(0)
            
            if char_name in window:
                values_dict[value]['values'].append(list_avg(values_window))
            else:
                values_dict[value]['values'].append(None)
            
        words.pop(0)
        
            
    # starting x value = midpoint of the window
    start_x = int(window_size/2)
    
        
    # set up x values running from midpoint of first window to midpoint of last window
    x = list(range(start_x, len(prepro)-start_x+1))
    

    # return x, sentiments
    return x, values_dict




characters = ['mike','will','lucas','dustin','eleven',
              'steve','hopper','joyce','nancy','jonathan',
              'max','robin','brenner','vecna']

results = {}

for char in characters:
    x, values_dict = sliding_window_character(char_name=char, z=3.5)
    results[char] = values_dict
    e = datetime.datetime.now()
    print("Completed", char, "at %s:%s:%s" % (e.hour, e.minute, e.second))
    
    

# Plot all results
for char in characters:
    name = char[0].upper() + char[1:]
    plt.plot(x, results[char]['power']['values'], alpha=0.8, color='lightblue')
    plt.plot(x, results[char]['danger']['values'], alpha=0.8, color='orange')
    title = 'Power and Danger Across the Series for ' + name
    plt.title(title)
    plt.legend(['Power','Danger'])
    plt.show()
    
    
with open("data/char_results_z3.5.json", "w") as f:
    json.dump(results,f)
    
    
    
results = {}

for char in characters:
    x, values_dict = sliding_window_character(char_name=char, z=4)
    results[char] = values_dict
    e = datetime.datetime.now()
    print("Completed", char, "at %s:%s:%s" % (e.hour, e.minute, e.second))
    
    

# Plot all results
for char in characters:
    name = char[0].upper() + char[1:]
    plt.plot(x, results[char]['power']['values'], alpha=0.8, color='lightblue')
    plt.plot(x, results[char]['danger']['values'], alpha=0.8, color='orange')
    title = 'Power and Danger Across the Series for ' + name
    plt.title(title)
    plt.legend(['Power','Danger'])
    plt.show()
    
    
with open("data/char_results_z4.json", "w") as f:
    json.dump(results,f)


    
    
    
    
    
        


# x, values_mike = sliding_window_character(char_name="mike")
# x, values_steve = sliding_window_character(char_name="steve", values_of_interest=['danger','power'])



# x, dict_episodic = sliding_window(values_of_interest=['power','danger'],z=3.5)

    

# # scatterplot of danger and power values for a give window of 10^z words    
# plt.scatter(dict_episodic['power']['values'], dict_episodic['danger']['values'])
# plt.title('Danger by Power')
# plt.show()


# power and danger on the same plot over the entire series
# plt.plot(x, dict_episodic['power']['values'], alpha=0.8, color='lightblue')
# plt.plot(x, dict_episodic['danger']['values'], alpha=0.8, color='orange')
# plt.title('Power and Danger Across the Series')
# plt.legend(['Power','Danger'])
# plt.show()


# # Keep track of how long things take
# e = datetime.datetime.now()
# print ("Completed first part at %s:%s:%s" % (e.hour, e.minute, e.second))





# x, dict_series = sliding_window(values_of_interest=['power','danger'],z=4)

    

# # scatterplot of danger and power values for a give window of 10^z words    
# plt.scatter(dict_series['power']['values'], dict_series['danger']['values'])
# plt.title('Danger by Power')
# plt.show()


# # power and danger on the same plot over the entire series
# plt.plot(x, dict_series['power']['values'], alpha=0.8, color='lightblue')
# plt.plot(x, dict_series['danger']['values'], alpha=0.8, color='orange')
# plt.title('Power and Danger Across the Series')
# plt.legend(['Power','Danger'])
# plt.show()


# # Keep track of how long things take
# e = datetime.datetime.now()
# print ("Completed second part at %s:%s:%s" % (e.hour, e.minute, e.second))







