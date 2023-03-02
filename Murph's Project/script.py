import pandas as pd

playerStats = pd.read_csv(r'player stats.csv')
# print(playerStats)

playerStats["mpg"] = playerStats["MP"] / playerStats["G"]
# playerStats
ps_Tm = playerStats.sort_values(by=['Tm','mpg'], ascending = False)

processed_teams = []
topFive = pd.DataFrame(columns=ps_Tm.columns)
topFive.drop(topFive.index, inplace=True)
for index, row in ps_Tm.iterrows():
    Tm = row['Tm']
    if Tm not in processed_teams and Tm != 'TOT':
        print(Tm)
        processed_teams.append(Tm)
        Tm_df = ps_Tm[ps_Tm['Tm']==Tm].head(5)
        print(Tm_df)
        topFive = pd.concat([topFive,Tm_df])
        print(topFive)

teamStats= topFive.groupby('Tm')['DBPM','OBPM','TS%', 'BPM'].mean()
# teamStats

nbaScores = pd.read_csv(r'updated nba scores.csv')
# nbaScores

merged_df = nbaScores.merge(teamStats, left_on='Visitor', right_on='Tm', how='left')
merged_df = merged_df.merge(teamStats, left_on='Home', right_on='Tm', suffixes=('_1', '_2'), how='left')
# merged_df


nbaScores['PTS'].astype(int)
nbaScores['PTS.1'].astype(int)
# this could possibly work

nbaScores['point_diff'] = nbaScores['PTS'] - nbaScores['PTS.1']
teamStats = teamStats.reset_index()


results = pd.DataFrame(columns=['Tm1', 'Tm2', 'DBPM_diff', 'OBPM_diff', 'TS_diff', 'BPM_diff', 'point_diff'])
for index, row in nbaScores.iterrows():
    Tm1 = row['Visitor']
    Tm2 = row['Home'] 
    tm1_stats = teamStats.loc[teamStats['Tm'] == Tm1].iloc[:, 1:].values[0]
    tm2_stats = teamStats.loc[teamStats['Tm'] == Tm2].iloc[:, 1:].values[0]
    DBPM_diff = tm1_stats[0] - tm2_stats[0]
    OBPM_diff = tm1_stats[1] - tm2_stats[1]
    TS_diff = tm1_stats[2] - tm2_stats[2]
    BPM_diff = tm1_stats[3] - tm2_stats[3]
    point_diff = row['point_diff']
    
    results = results.append({
        'Tm1': Tm1,
        'Tm2': Tm2,
        'DBPM_diff': DBPM_diff,
        'OBPM_diff': OBPM_diff,
        'TS_diff': TS_diff,
        'BPM_diff': BPM_diff,
        'point_diff': point_diff
    }, ignore_index=True)