#### Slightly modified from Assignment 20: ####

# Question 1 A
# deconstructing text into file w/ vector of 1-grams
    
    
    
    
def deconstruct(filepath_old, filepath_new):
    
    # start by reading in the raw data
    with open(filepath_old) as f:
        data = f.readlines()

    # check all of the nonletters
    not_letters = set()
    for item in data:
        for char in item:
            if not char.isalpha():
                not_letters.add(char)
                
    # convert to a list so we can access indices
    not_letters = list(not_letters)
    
    # lists to hold the one-grams
    one_grams = []    # final list
    step1 = []        # intermediary list 
    
    # loop through each line in the raw data
    for line in data:
        # ignore the newline
        line = line[:-1]
        # split at each space
        line_sp = line.split(' ')
        # add each to step1 list
        for item in line_sp:
            step1.append(item)
            
            
            
    # at this point, step1 holds list of all one-grams with the punctuation attached
            
    clean_only = []
        
    # loop through again to separate the punctuation/non-letters
    for one_gram in step1:
        # if the 1-gram contains a non-alphabetic character
        if not one_gram.isalpha():
            # find the non-alphabetic character in not_letters and add to the list separately
            
            # also clean up the words to remove the punctuation, numbers, etc. from them
            cleaned = ""
            
            # loop through each character in the item
            for char in one_gram:
                # if the character in question is not a letter
                if char in not_letters:
                    # find its location in not_letters and add that item to the one-grams list
                    index = not_letters.index(char)
                    one_grams.append(not_letters[index])
                    
                # if it is a letter, append to the cleaned version of the word
                else:
                    cleaned += char
                    
            # also add the cleaned up word itself
            one_grams.append(cleaned)
            clean_only.append(cleaned)
            
        # if no non-alpha characters, then we just add the item as is
        else:
            one_grams.append(one_gram)
            clean_only.append(one_gram)
    
    
    # alternatively, a data file which ignores the punctuation
    f = open(filepath_new, "w")
    for item in clean_only:
        f.write(item + '\n')
    f.close()
    
    
    
# deconstruct("data/stranger_things_prepro.txt","data/one_grams_clean_full_prepro.txt")



# deconstruct and save results for every individual episode
season_folders = ['season1','season2','season3','season4']
episodes = ['e1','e2','e3','e4','e5','e6','e7','e8','e9']

for season in season_folders:
    for episode in episodes:
        file_location = 'data/episodes/' + season + '/'
        old_file = file_location + episode + '.txt'
        new_file = file_location + 'one_grams_clean_' + episode + '.txt'
        
        # error handling to account for seasons of different lengths
        try:
            deconstruct(old_file, new_file)
        except FileNotFoundError:
            pass














