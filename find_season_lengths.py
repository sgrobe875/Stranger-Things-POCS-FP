### Count number of one-grams in each season; use results to make vertical lines
### in timeseries plots to help distinguish the different seasons

### Also, make stacked timeseries plots for each season! These will be easier
### since they won't require the same x scale





season_folders = ['season1','season2','season3','season4']
episodes = ['e1','e2','e3','e4','e5','e6','e7','e8','e9']

episode_avgs = {}

lengths = []

for season in season_folders:
    
    full_season = []
    
    for episode in episodes:
        file_location = 'data/episodes/' + season + '/'
        filename = file_location + 'one_grams_clean_' + episode + '.txt'
        
        # error handling to account for seasons of different lengths
        try:
            with open(filename) as f:
                curr = f.readlines()
            
            full_season += curr

            
        except FileNotFoundError:
            pass
            

    lengths.append(len(full_season))



cumulative_lengths = []

for i in range(1, len(lengths)):
    cumulative_lengths.append(sum(lengths[:i]))


print(cumulative_lengths)

