import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec





with open('data/char_results_z3.json') as f:
  results = json.load(f)


# read in the preprocessed text
with open('data/one_grams_clean_full_prepro.txt') as f:
    prepro = f.readlines()
    


def make_x_list(z):
    
    window_size = 10**z
    
    # starting x value = midpoint of the window
    start_x = int(window_size/2)
    
    # set up x values running from midpoint of first window to midpoint of last window
    x = list(range(start_x, len(prepro)-start_x+1))

    return x


x = make_x_list(3)

# build the figure of 5 plots of main characters
gs = gridspec.GridSpec(5,1)
fig = plt.figure(figsize=(14, 28))

xlab = 'Word number i'
ylab = 'Score'

# first plot
ax = fig.add_subplot(gs[0])
ax.plot(x, results['mike']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, results['mike']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Mike')

# second plot
ax = fig.add_subplot(gs[1])
ax.plot(x, results['will']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, results['will']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Will')

# third plot
ax = fig.add_subplot(gs[2])
ax.plot(x, results['lucas']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, results['lucas']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Lucas')

# fourth plot
ax = fig.add_subplot(gs[3])
ax.plot(x, results['dustin']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, results['dustin']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Dustin')

# fifth plot
ax = fig.add_subplot(gs[4])
ax.plot(x, results['eleven']['power']['values'], alpha=0.8, color='lightblue')
ax.plot(x, results['eleven']['danger']['values'], alpha=0.8, color='orange')
ax.set_xlabel(xlab)
ax.set_ylabel(ylab)
ax.set_title('Eleven')



    
fig.tight_layout(h_pad=1)
    
plt.show()