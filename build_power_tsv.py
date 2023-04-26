import pandas as pd

# build tsv of power
vad_pds = pd.read_csv('data/ousiometry_data_augmented.tsv', sep='\t')



# power_df = vad_pds[['word','power']]
power_df = vad_pds[['word','danger']]



# path = '~sarahgrobe/opt/anaconda3/lib/python3.8/site-packages/shifterator/lexicons/Custom/custom_power.tsv'
path = '~sarahgrobe/opt/anaconda3/lib/python3.8/site-packages/shifterator/lexicons/Custom/custom_danger.tsv'


power_df.to_csv(path, sep='\t', index=False, header=False)

