import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec





with open('data/char_results_z3.json') as f:
  char_results = json.load(f)
  
  
with open('data/values_dict_z3.5.json') as f:
  values_dict_z3_5 = json.load(f)
  
  
with open('data/values_dict_z4.json') as f:
  values_dict_z4 = json.load(f)


# read in the preprocessed text
with open('data/one_grams_clean_full_prepro.txt') as f:
    prepro = f.readlines()

    
# read in the preprocessed text
with open('data/one_grams_clean_full.txt') as f:
    raw_text = f.readlines()
    
    
# determined in find_season_lengths.py
season_ends = [32747, 72010, 113105]


def make_x_list(z, text = prepro):
    
    window_size = 10**z
    
    # starting x value = midpoint of the window
    start_x = int(window_size/2)
    
    # set up x values running from midpoint of first window to midpoint of last window
    x = list(range(start_x, len(text)-start_x+1))

    return x





##### plot time series (unstacked) ################################################################3
 

### z = 3.5 ### 

x = make_x_list(3.5, raw_text)

# no vertical lines
fig = plt.figure(figsize=(15, 10))
plt.rcParams.update({'font.size': 22})   # set all font sizes to 22 unless otherwise overwritten
plt.plot(x, values_dict_z3_5['power']['values'], alpha=0.8, color='lightblue')
plt.plot(x, values_dict_z3_5['danger']['values'], alpha=0.8, color='orange')
plt.title('Power and Danger Across "Stranger Things"', fontsize=32, pad=20)
plt.legend(['Power','Danger'], prop={'size': 20}, loc='center right')
plt.xlabel('Word number i')
plt.ylabel('Score')
plt.show()

# now add in the vertical lines at season ends
fig = plt.figure(figsize=(15, 10))
plt.rcParams.update({'font.size': 22})   # set all font sizes to 22 unless otherwise overwritten
plt.plot(x, values_dict_z3_5['power']['values'], alpha=0.8, color='lightblue')
plt.plot(x, values_dict_z3_5['danger']['values'], alpha=0.8, color='orange')
plt.title('Power and Danger Across "Stranger Things"', fontsize=32, pad=20)
plt.vlines(season_ends, ymin=-0.15, ymax=0.05, linestyles='dashed',color='red')
plt.legend(['Power','Danger','Season End'], prop={'size': 20}, loc='center right')
plt.xlabel('Word number i')
plt.ylabel('Score')
plt.show()



### z = 4 ###

x = make_x_list(4, raw_text)

# no vertical lines
fig = plt.figure(figsize=(15, 10))
plt.rcParams.update({'font.size': 22})   # set all font sizes to 22 unless otherwise overwritten
plt.plot(x, values_dict_z4['power']['values'], alpha=0.8, color='lightblue')
plt.plot(x, values_dict_z4['danger']['values'], alpha=0.8, color='orange')
plt.title('Power and Danger Across "Stranger Things"', fontsize=32, pad=20)
plt.legend(['Power','Danger'], prop={'size': 20}, loc='center right')
plt.xlabel('Word number i')
plt.ylabel('Score')
plt.show()

# now add in the vertical lines at season ends
fig = plt.figure(figsize=(15, 10))
plt.rcParams.update({'font.size': 22})   # set all font sizes to 22 unless otherwise overwritten
plt.plot(x, values_dict_z4['power']['values'], alpha=0.8, color='lightblue')
plt.plot(x, values_dict_z4['danger']['values'], alpha=0.8, color='orange')
plt.title('Power and Danger Across "Stranger Things"', fontsize=32, pad=20)
plt.vlines(season_ends, ymin=-0.15, ymax=0.05, linestyles='dashed',color='red')
plt.legend(['Power','Danger','Season End'], prop={'size': 20}, loc='center right')
plt.xlabel('Word number i')
plt.ylabel('Score')
plt.show()






##### stacked plot of 5 main characters ###########################################################

x = make_x_list(3)

# build the figure of 5 plots of main characters
gs = gridspec.GridSpec(5,1)
fig = plt.figure(figsize=(14, 28))

xlab = 'Word number i'
ylab = 'Score'

fig.suptitle("Power and Danger for Specific Characters\n", fontsize=36)

plt.rcParams.update({'font.size': 18}) 

# first plot
ax = fig.add_subplot(gs[0])
ax.plot(x, char_results['mike']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, char_results['mike']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.vlines(season_ends, ymin=-0.17, ymax=0.1, linestyles='dashed',color='red')
ax.set_title('Mike')

# second plot
ax = fig.add_subplot(gs[1])
ax.plot(x, char_results['will']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, char_results['will']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.vlines(season_ends, ymin=-0.17, ymax=0.1, linestyles='dashed',color='red')
ax.set_title('Will')

# third plot
ax = fig.add_subplot(gs[2])
ax.plot(x, char_results['lucas']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, char_results['lucas']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.vlines(season_ends, ymin=-0.17, ymax=0.1, linestyles='dashed',color='red')
ax.set_title('Lucas')

# fourth plot
ax = fig.add_subplot(gs[3])
ax.plot(x, char_results['dustin']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, char_results['dustin']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.vlines(season_ends, ymin=-0.17, ymax=0.1, linestyles='dashed',color='red')
ax.set_title('Dustin')

# fifth plot
ax = fig.add_subplot(gs[4])
ax.plot(x, char_results['eleven']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, char_results['eleven']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.vlines(season_ends, ymin=-0.17, ymax=0.1, linestyles='dashed',color='red')
ax.set_title('Eleven')


fig.legend(['Power','Danger','Season End'], prop={'size': 20}, loc='center left', bbox_to_anchor=(1, 0.5))

    
fig.tight_layout(h_pad=1)
    
plt.show()





##### stacked plot of the four seasons #####################################################

### z = 3.5 ###

x = make_x_list(3.5, raw_text)

# divide x by the four seasons and rescale
x_s1 = [i for i in x if i <= season_ends[0]]

x_s2 = [i for i in x if i > season_ends[0] and i <= season_ends[1]]
x_s2 = [item - x_s2[0] + x[0] for item in x_s2]

x_s3 = [i for i in x if i > season_ends[1] and i <= season_ends[2]]
x_s3 = [item - x_s3[0] + x[0] for item in x_s3]

x_s4 = [i for i in x if i > season_ends[2]]
x_s4 = [item - x_s4[0] + x[0] for item in x_s4]


# get the necessary y values in similar fashion as above
s1 = len(x_s1)
s2 = s1 + len(x_s2)
s3 = s2 + len(x_s3)

y_s1_p = values_dict_z3_5['power']['values'][:s1]
y_s2_p = values_dict_z3_5['power']['values'][s1:s2]
y_s3_p = values_dict_z3_5['power']['values'][s2:s3]
y_s4_p = values_dict_z3_5['power']['values'][s3:]

y_s1_d = values_dict_z3_5['danger']['values'][:s1]
y_s2_d = values_dict_z3_5['danger']['values'][s1:s2]
y_s3_d = values_dict_z3_5['danger']['values'][s2:s3]
y_s4_d = values_dict_z3_5['danger']['values'][s3:]



# build the figure of 4 plots
gs = gridspec.GridSpec(4,1)
fig = plt.figure(figsize=(14, 28))

xlab = 'Word number i'
ylab = 'Score'

fig.suptitle("Power and Danger Across Seasons\n", fontsize=36)

plt.rcParams.update({'font.size': 18}) 


# first plot
ax = fig.add_subplot(gs[0])
ax.plot(x_s1, y_s1_p, alpha=0.8, color='lightblue')
ax.plot(x_s1, y_s1_d, alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Season 1')


# second plot
ax = fig.add_subplot(gs[1])
ax.plot(x_s2, y_s2_p, alpha=0.8, color='lightblue')
ax.plot(x_s2, y_s2_d, alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Season 2')


# third plot
ax = fig.add_subplot(gs[2])
ax.plot(x_s3, y_s3_p, alpha=0.8, color='lightblue')
ax.plot(x_s3, y_s3_d, alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Season 3')


# fourth plot
ax = fig.add_subplot(gs[3])
ax.plot(x_s4, y_s4_p, alpha=0.8, color='lightblue')
ax.plot(x_s4, y_s4_d, alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Season 4')



fig.legend(['Power','Danger'], prop={'size': 20}, loc='center left', bbox_to_anchor=(1, 0.5))

    
fig.tight_layout(h_pad=1)
    
plt.show()













