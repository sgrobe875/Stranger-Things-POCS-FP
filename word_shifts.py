import shifterator as sh
from collections import Counter
import pandas as pd
from labMTsimple.storyLab import emotionFileReader, emotion, stopper, emotionV



def prep_corpus(corpus1, corpus2):  
    lefthandcounter = Counter(corpus1)  
    righthandcounter = Counter(corpus2)  
    for key in lefthandcounter.keys():    
        if key not in righthandcounter.keys():      
            righthandcounter[key] = 0  
    for key in righthandcounter.keys():    
        if key not in lefthandcounter.keys():      
            lefthandcounter[key] = 0  
    
    return(dict(lefthandcounter), dict(righthandcounter))


def build_raw_text(corpus_list):
    raw = ""
    for word in corpus_list:
        raw += word + ' '
    return raw


# takes in a list, returns the average of the values in the list
# ignores any None values in the calculation
def list_avg(l):
    return sum(filter(None, l)) / len(list(filter(None, l)))

# only looks at danger by default
def full_season_score(data, values_of_interest = ['danger']):
    
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


# read in the table of VAD and PDS values
vad_pds = pd.read_csv('data/ousiometry_data_augmented.tsv', sep='\t')


# read in one-grams and use cutoff values (find_season_end.py) to build corpora
with open('data/one_grams_clean_full.txt') as f:
    full_text = f.readlines()


# first goal: s3 vs. all others
s3_words = full_text[72010:113105]
for i in range(len(s3_words)):
    s3_words[i] = s3_words[i].lower().rstrip('\n')
        
while '' in s3_words:
    s3_words.remove('')

s124_words = full_text[:72010] + full_text[113105:]
for i in range(len(s124_words)):
    s124_words[i] = s124_words[i].lower().rstrip('\n')

while '' in s124_words:
    s124_words.remove('')


s3freqs, s124freqs = prep_corpus(s3_words, s124_words)

x, results = full_season_score(s124_words)  
avg = results['danger']['values'][0]
print(avg)




sentiment_shift = sh.WeightedAvgShift(type2freq_1=s124freqs,
                                      type2freq_2=s3freqs,
                                      reference_value = avg,
                                      type2score_1='custom_danger')


sentiment_shift.get_shift_graph(system_names = ['Seasons 1, 2, & 4', 'Season 3'],
                                filename='figures/wordshift_s124_s3_danger.png')





# repeat, but ignore "will" since that is a name, but seems to have a big effect
# first goal: s3 vs. all others
# s3_words = full_text[72010:113105]
# for i in range(len(s3_words)):
#     s3_words[i] = s3_words[i].lower().rstrip('\n')
        
# if '' in s3_words:
#     s3_words.remove('')

# s124_words = full_text[:72010] + full_text[113105:]
# for i in range(len(s124_words)):
#     s124_words[i] = s124_words[i].lower().rstrip('\n')

# if '' in s124_words:
#     s124_words.remove('')

# remove will
remove = 'will'
while remove in s3_words:
    s3_words.remove(remove)
    
while remove in s124_words:
    s124_words.remove(remove)
    
    
    
    
# remove eleven
remove = 'eleven'
while remove in s3_words:
    s3_words.remove(remove)
    
while remove in s124_words:
    s124_words.remove(remove)

s3freqs, s124freqs = prep_corpus(s3_words, s124_words)


# x, results = full_season_score(s124_words)  
x, results = full_season_score(s3_words)  
avg = results['danger']['values'][0]
print(avg)


sentiment_shift = sh.WeightedAvgShift(type2freq_1=s124freqs,
                                      type2freq_2=s3freqs,
                                      reference_value = avg,
                                      type2score_1='custom_danger')


sentiment_shift.get_shift_graph(system_names = ['Seasons 1, 2, & 4', 'Season 3'],
                                filename='figures/wordshift_s124_s3_danger_nonames.png')




### Sentiment ###

corp124 = build_raw_text(s124_words)
corp3 = build_raw_text(s3_words)


labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,lang='english', returnVector=True)

fulltextValence, fulltextFvec = emotion(corp124, labMT, shift=True, happsList=labMTvector)
temp = stopper(fulltextFvec, labMTvector, labMTwordList, stopVal=1.0)
avg = emotionV(temp, labMTvector)
print(avg)


# hardcode for the moment to save time
# avg = 5.720768099602948




sentiment_shift = sh.WeightedAvgShift(type2freq_1=s124freqs,
                                      type2freq_2=s3freqs,
                                      reference_value = avg,
                                      type2score_1='labMT_English',
                                      stop_lens=[(4,6)])


sentiment_shift.get_shift_graph(system_names = ['Seasons 1, 2, & 4', 'Season 3'],
                                filename='figures/wordshift_s124_s3_sentiment.png')

# based on plot, looks like S3 has a higher volume of kind of negative words, and lower volume
# of really positive words --> more positive overall sentiment than other seasons

# This is really interesting and not really what we typically see in these word shifts!






# avg danger per season; use this to inform more word shifts
season_ends = [32747, 72010, 113105]

s1_words = full_text[:32747]
for i in range(len(s1_words)):
    s1_words[i] = s1_words[i].lower().rstrip('\n')
        
while '' in s1_words:
    s1_words.remove('')
    
s2_words = full_text[32747:72010]
for i in range(len(s2_words)):
    s2_words[i] = s2_words[i].lower().rstrip('\n')
        
while '' in s2_words:
    s2_words.remove('')

s3_words = full_text[72010:113105]
for i in range(len(s3_words)):
    s3_words[i] = s3_words[i].lower().rstrip('\n')
        
while '' in s3_words:
    s3_words.remove('')
    
s4_words = full_text[113105:]
for i in range(len(s4_words)):
    s4_words[i] = s4_words[i].lower().rstrip('\n')
        
while '' in s4_words:
    s4_words.remove('')




words_list = [s1_words, s2_words, s3_words, s4_words]
avgs = []
for word_list in words_list:
    x, results = full_season_score(word_list)
    avg = results['danger']['values'][0]
    avgs.append(avg)
    
print('Average danger by season:')
for i in range(len(avgs)):
    print('Season ', str(i + 1), ': ', str(avgs[i] + 1), sep='')
    
# least dangerous ---> most dangerous
# S3 --> S1 --> S2 --> S4


# Next, try out: S1 + S3 vs. S2 + S4
# And: S2 vs. S4



s13_words = s1_words + s3_words
s24_words = s2_words + s4_words

s13freqs, s24freqs = prep_corpus(s13_words, s24_words)

x, results = full_season_score(s13_words)  
avg = results['danger']['values'][0]
print(avg)


sentiment_shift = sh.WeightedAvgShift(type2freq_1=s13freqs,
                                      type2freq_2=s24freqs,
                                      reference_value = avg,
                                      type2score_1='custom_danger')


sentiment_shift.get_shift_graph(system_names = ['Seasons 1 & 3', 'Seasons 2 & 4'],
                                                filename='figures/wordshift_s13_s24.png')




###########


s2freqs, s4freqs = prep_corpus(s2_words, s4_words)

avg = avgs[1]
print(avg)


sentiment_shift = sh.WeightedAvgShift(type2freq_1=s2freqs,
                                      type2freq_2=s4freqs,
                                      reference_value = avg,
                                      type2score_1='custom_danger') 


sentiment_shift.get_shift_graph(system_names = ['Season 2', 'Season 4'], 
                                filename="figures/wordshift_s2_s4.png")


# season 4 has really strong words - fight, weapons, war, cursed, demon, die, kill
# season 2 has a lot of noises - screeching, growling, grunts, grunting, screams, screeches, scoffs

# overall they're very similar, season 4 just has harsher language









# Throw in a proportion shift or two because why not:
    
# Season 3 vs. All others

s3_words = full_text[72010:113105]
for i in range(len(s3_words)):
    s3_words[i] = s3_words[i].lower().rstrip('\n')
        
while '' in s3_words:
    s3_words.remove('')

s124_words = full_text[:72010] + full_text[113105:]
for i in range(len(s124_words)):
    s124_words[i] = s124_words[i].lower().rstrip('\n')

while '' in s124_words:
    s124_words.remove('')


s3freqs, s124freqs = prep_corpus(s3_words, s124_words)

proportion_shift = sh.ProportionShift(type2freq_1=s124freqs,
                                      type2freq_2=s3freqs)
proportion_shift.get_shift_graph(system_names = ['Seasons 1, 2, and 4', 'Season 3'],
                                 title='Proportion Shift of Season 3 vs. All Other Seasons')



# try again and remove names
names = ['will','lucas','dustin','nancy','mike','max','eleven','jonathan','mom',
         'joyce','steve','chrissy','billy','angela','papa','hopper','el','robin']

for name in names:
    while name in s3_words:
        s3_words.remove(name)
    
    while name in s124_words:
        s124_words.remove(name)
        

s3freqs, s124freqs = prep_corpus(s3_words, s124_words)

proportion_shift = sh.ProportionShift(type2freq_1=s124freqs,
                                      type2freq_2=s3freqs)
proportion_shift.get_shift_graph(system_names = ['Seasons 1, 2, and 4', 'Season 3'],
                                 title='Proportion Shift of Season 3 vs. All Other Seasons\nIgnoring Names')




# Season 1 + 3 vs. Season 2 + 4

proportion_shift = sh.ProportionShift(type2freq_1=s13freqs,
                                      type2freq_2=s24freqs)
proportion_shift.get_shift_graph(system_names = ['Seasons 1 and 3', 'Seasons 2 and 4'],
                                 title='Proportion Shift of Seasons 1 and 3 vs. Seasons 2 and 4')



# Not much of anything interesting in these








