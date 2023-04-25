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



x, values_dict = sliding_window(z=3.5)


# plot each of the values of interest separately over the entire series
for key in values_dict.keys():    
    plt.plot(x, values_dict[key]['values'])
    plt.title(key)
    plt.show()
    

# scatterplot of danger and power values for a give window of 10^z words    
plt.scatter(values_dict['power']['values'], values_dict['danger']['values'])
plt.title('Danger by Power')
plt.show()


# power and danger on the same plot over the entire series
plt.plot(x, values_dict['power']['values'], alpha=0.8, color='lightblue')
plt.plot(x, values_dict['danger']['values'], alpha=0.8, color='orange')
plt.title('Power and Danger Across the Series')
plt.legend(['Power','Danger'])
plt.show()





# Keep track of how long things take
e = datetime.datetime.now()
print ("Completed at %s:%s:%s" % (e.hour, e.minute, e.second))


# to save time, write the results to a json file so they can be easily accessed later
with open("data/values_dict_z3.5.json", "w") as f:
    json.dump(values_dict,f)





#### Notes ####


# Overall, z = 3.5 appears best for getting episodic ebbs and flows while z = 4
# seems to do better at capture the flow of the series as a whole  




### Next step: make windows centered on a character
### e.g., every time "steve" or a derivative thereof appears, start 10^z before it (so the name
### in questions is the last word of the window) and continue moving the window until 10^z beyond
### it (until it's the first word in the window)
### Then:
### Plot VAD and/or PDS within these windows for major characters
###    Maybe start with the 4 boys (mike, will, lucas, dustin) and eleven
###    Do another one with just secondary characters (hopper, steve, nancy, joyce, jonathan)
###        Note that many important characters didn't join until later seasons (robin, murray, etc.)



# Make one figure with 4 plots: one for each season to be able to compare the progressions



# with z = 4, there are 4 distinct humps in the plot of danger over the course of the
# series; work on adding vertical lines to separate the seasons and see how/if these 
# spikes in danger correspond with the beginnings/ends of the seasons




# Per #5 in assignment 23 instructions: look at at least one of these metrics (maybe
# danger?) on a per-episode basis and try to make a similar graphic as the Buffy example





