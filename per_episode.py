import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns



# Keep track of how long things take
e = datetime.datetime.now()
print ("Beginning at %s:%s:%s" % (e.hour, e.minute, e.second))



# read in the table of VAD and PDS values
vad_pds = pd.read_csv('data/ousiometry_data_augmented.tsv', sep='\t')




# takes in a list, returns the average of the values in the list
# ignores any None values in the calculation
def list_avg(l):
    return sum(filter(None, l)) / len(list(filter(None, l)))


# Looks through cleaned 1-grams and returns the values of interest across a sliding window
# Parameters: values_of_interest = list of all values we want to check; set to VAD & PDS by default
#             z = window size, 10^z; set to 2 for a window size of 100 by default
# Returns x list with midpoints used for plotting, as well as the average values across entire corpus
def full_avg_score(values_of_interest = ['power', 'danger']):
    
    # set window size using z
    window_size = len(data)
    
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




season_folders = ['season1','season2','season3','season4']
episodes = ['e1','e2','e3','e4','e5','e6','e7','e8','e9']

episode_avgs = {}

for season in season_folders:
    episode_avgs[season] = {'power':[], 'danger':[]}
    for episode in episodes:
        file_location = 'data/episodes/' + season + '/'
        filename = file_location + 'one_grams_clean_' + episode + '.txt'
        
        # error handling to account for seasons of different lengths
        try:
            with open(filename) as f:
                data = f.readlines()
                
            x, results = full_avg_score()
            episode_avgs[season]['power'].append(results['power']['values'][0])
            episode_avgs[season]['danger'].append(results['danger']['values'][0])
            
        except FileNotFoundError:
            # pass
            episode_avgs[season]['power'].append(None)
            episode_avgs[season]['danger'].append(None)

e = datetime.datetime.now()
print ("Completed at %s:%s:%s" % (e.hour, e.minute, e.second))




# build dataframes
power_df = pd.DataFrame([episode_avgs['season1']['power'], episode_avgs['season2']['power'],
                          episode_avgs['season3']['power'], episode_avgs['season4']['power']], 
                        dtype="float").transpose()
power_df.columns = [1,2,3,4]
power_df.index = [1,2,3,4,5,6,7,8,9]


danger_df = pd.DataFrame([episode_avgs['season1']['danger'], episode_avgs['season2']['danger'],
                          episode_avgs['season3']['danger'], episode_avgs['season4']['danger']], 
                        dtype="float").transpose()
danger_df.columns = [1,2,3,4]
danger_df.index = [1,2,3,4,5,6,7,8,9]



### Build heatmap from results ###

fig, ax = plt.subplots(figsize=(10,15))
sns.heatmap(power_df, cmap="magma")
ax.set_xlabel("Season", size=16)
ax.xaxis.set_label_position('top')
ax.set_ylabel("Episode\n", size=16)
plt.title("Stranger Things Power by Episode\n", size=24)
ax.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, 
               top = False, labeltop=True)
plt.savefig("figures/power_per_episode.png",bbox_inches='tight')



fig, ax = plt.subplots(figsize=(10,15))
sns.heatmap(danger_df, cmap="magma")
ax.set_xlabel("Season", size=16)
ax.xaxis.set_label_position('top')
ax.set_ylabel("Episode\n", size=16)
plt.title("Stranger Things Danger by Episode\n", size=24)
ax.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, 
               top = False, labeltop=True)
plt.savefig("figures/danger_per_episode.png",bbox_inches='tight')





