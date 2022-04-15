import os
import pandas as pd

data_dir = os.path.join(os.path.abspath(os.curdir), 'data')
assets_dir = os.path.join(os.path.abspath(os.curdir), 'assets')

# main data
df1 = pd.read_csv(os.path.join(data_dir, 'fire_final.csv'), low_memory=False)
df1.drop('Unnamed: 0', axis=1, inplace=True)
# add other binary category
df1['other'] = 0
df1.iloc[df1[(df1['rekindling'] == 0) & (df1['negligent'] == 0) & (df1['intentional'] == 0)].index, -1] = 1
# convert binary categories into main_cat
df1['main_cat'] = 'nan'
df1.iloc[df1[df1['rekindling'] == 1].index, -1] = 'Rekindling'
df1.iloc[df1[df1['negligent'] == 1].index, -1] = 'Negligent'
df1.iloc[df1[df1['intentional'] == 1].index, -1] = 'Intentional'
df1.iloc[df1[df1['other'] == 1].index, -1] = 'Other'
df1['category'] = df1['category'].map(lambda x: str(x).title())
# export to csv
df1.to_csv(os.path.join(data_dir, 'main_data.csv'))

# fire brigade expenditure data
df2 = pd.read_csv(os.path.join(data_dir, 'fire_brigade.csv'), low_memory=False)
df2.rename(columns={'Years': 'year', 'Fire Brigade expenditure': 'expenditure'}, inplace=True)
df3 = df1.groupby('year').agg({'total_ba': 'sum'})
df3 = df3.merge(df2, left_on=df3.index, right_on='year')
df3.set_index('year', inplace=True)
df3['ratio'] = df3['expenditure'] / df3['total_ba']
# export to csv
df3.to_csv(os.path.join(data_dir, 'expenditure.csv'))
