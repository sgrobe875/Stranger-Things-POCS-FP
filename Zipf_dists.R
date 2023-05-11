library(dplyr)
library(ggplot2)
library(tidyverse)



# set working directory to the location of this file
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))



# inputs: dataframe, the column to be used (as a string), and optionally, an addition to the plot title
calc_and_plot_Zipf <- function(dataframe, columnName, title) {
  # sort largest to smallest and add index column
  columnNo <- which(colnames(dataframe) == columnName)
  data <- dataframe %>% arrange(-dataframe[columnNo])
  data <- tibble::rowid_to_column(data, "index")
  
  # columns shift by 1 since we've now added the index column
  columnNo <- columnNo + 1
  
  # obtain all unique counts (values in V1)
  values <- data %>% distinct(data[columnNo])
  values <- values[ ,1]
  
  # add an empty column to hold the rank
  data <- data %>% mutate(rank = NA)
  
  # fill in the rank column by taking mean of indices for all those with each unique value
  for (i in seq(1, length(values))) {
    val <- values[i]
    data$rank[data[columnName] == val] <- mean(data$index[data[columnName] == val])
  }
  
  
  
  # pretty plot:
  plotTitle <- "Zipf Distribution"
  if (!missing(title)) {
    plotTitle <- paste(plotTitle, title, sep='')
  } 
  
  ggplot(data = data, mapping = aes(x = log10(rank), y = log10(data[,columnNo]))) + 
    geom_point(alpha = 0.5) +
    ggtitle(plotTitle) +
    xlab("Log10(Rank)") + 
    ylab("Log10(Frequency)") +
    theme_bw() +
    theme(plot.title = element_text(hjust = 0.5), axis.text=element_text(size=11))
}


# same as above, but does not plot, and returns the modified dataframe (with rank and index columns)
calc_Zipf <- function(dataframe, columnName) {
  # sort largest to smallest and add index column
  columnNo <- which(colnames(dataframe) == columnName)
  data <- dataframe %>% arrange(-dataframe[columnNo])
  data <- tibble::rowid_to_column(data, "index")
  
  # columns shift by 1 since we've now added the index column
  columnNo <- columnNo + 1
  
  # obtain all unique counts (values in V1)
  values <- data %>% distinct(data[columnNo])
  values <- values[ ,1]
  
  # add an empty column to hold the rank
  data <- data %>% mutate(rank = NA)
  
  # fill in the rank column by taking mean of indices for all those with each unique value
  for (i in seq(1, length(values))) {
    val <- values[i]
    data$rank[data[columnName] == val] <- mean(data$index[data[columnName] == val])
  }
  
  return(data)
}


# just the plotting portion of the calc_and_plot_Zipf function; use with dataframe from the calc_Zipf function
plot_Zipf <- function(dataframe, columnName, title) {
  columnNo <- which(colnames(dataframe) == columnName)

  # pretty plot:
  plotTitle <- "Zipf Distribution"
  if (!missing(title)) {
    plotTitle <- paste(plotTitle, title, sep='')
  } 
  
  ggplot(data = dataframe, mapping = aes(x = log10(rank), y = log10(dataframe[,columnNo]))) + 
    geom_point(alpha = 0.5) +
    ggtitle(plotTitle) +
    xlab("Log10(Rank)") + 
    ylab("Log10(Frequency)") +
    theme_bw() +
    theme(plot.title = element_text(hjust = 0.5), axis.text=element_text(size=11))
}


# same as plot_Zipf function above, but includes the regression line in the plot
plot_Zipf_with_linreg <- function(dataframe, columnName, title) {
  columnNo <- which(colnames(dataframe) == columnName)
  
  # pretty plot:
  plotTitle <- "Zipf Distribution"
  if (!missing(title)) {
    plotTitle <- paste(plotTitle, title, sep='')
  } 
  
  ggplot(data = dataframe, mapping = aes(x = log10(rank), y = log10(dataframe[,columnNo]))) + 
    geom_point(alpha = 0.5) +
    ggtitle(plotTitle) +
    xlab("Log10(Rank)") + 
    ylab("Log10(Frequency)") +
    geom_smooth(method='lm') + 
    theme_bw() +
    theme(plot.title = element_text(hjust = 0.5), axis.text=element_text(size=11))
}


# takes in a dataframe of one-grams, returns a dataframe of words and their corresponding frequencies
build_freq_df <- function(corpus_df) {
  # set all words to lowercase first
  for (i in seq(nrow(corpus_df))) {
    corpus_df[i, 'V1'] <- tolower(corpus_df[i, 'V1'])
  }
  freq_df <- data.frame(table(corpus_df))
  names(freq_df) <- c('word','freq')
  
  return(freq_df)
}


# same as above, but case sensitive
build_freq_df_sensitive <- function(corpus_df) {
  freq_df <- data.frame(table(corpus_df))
  names(freq_df) <- c('word','freq')
  
  return(freq_df)
}






# read in one-grams
st_text <- read.csv('data/one_grams_clean_full.txt', header=FALSE)


### Case insensitive ###

# get frequencies of words
freq_df <- build_freq_df(st_text)
# build plot using the frequencies
calc_and_plot_Zipf(freq_df, 'freq', ' for Stranger Things (Case Insensitive)')

# get the rank data
t1 <- calc_Zipf(freq_df, 'freq')
# build linear model
model <- lm(data = t1, log10(freq) ~ log10(rank))
model$coefficients[2]
# plot with linear model
plot_Zipf_with_linreg(t1, 'freq', ' for Stranger Things (Case Insensitive) with Linear Regression')


# 25 most used words
head(t1, 25)


### Case sensitive ###

# get frequencies of words
freq_df_sensitive <- build_freq_df_sensitive(st_text)
# build plot using the frequencies
calc_and_plot_Zipf(freq_df_sensitive, 'freq', ' for Stranger Things (Case Sensitive)')

# get the rank data
t2 <- calc_Zipf(freq_df_sensitive, 'freq')
# build linear model
model <- lm(data = t2, log10(freq) ~ log10(rank))
model$coefficients[2]
# plot with linear model
plot_Zipf_with_linreg(t2, 'freq', ' for Stranger Things (Case Sensitive) with Linear Regression')


# 25 most used words
head(t2, 25)





# write to files
write.csv(t1, "data/case_insensitive_zipf.csv")
write.csv(t2, "data/case_sensitive_zipf.csv")



t1 <- read.csv("data/case_insensitive_zipf.csv")
t2 <- read.csv("data/case_sensitive_zipf.csv")






# rebuild and write files for building the ousiogram
ousio_data <- data.frame('ngram'=t1$word, 'count'=t1$freq)
write.csv(ousio_data, 'data/corpus_data.csv')

