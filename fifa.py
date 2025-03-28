import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

matches = pd.read_csv(r'C:/Namit/Unified Mentor Internship/FIFA World Cup/WorldCupMatches.csv')
players = pd.read_csv(r'C:/Namit/Unified Mentor Internship/FIFA World Cup/WorldCupPlayers.csv')
cups = pd.read_csv(r'C:/Namit/Unified Mentor Internship/FIFA World Cup/WorldCups.csv')

#Checking for null & missing values
matches.info()
matches.describe()
matches.isnull().sum()            #no null values

players.info()
players.describe()
players.isnull().sum()            #null values in Position & Event

cups.info()
cups.describe()
cups.isnull().sum()               #no null values


#Typecasting
matches['Date'] = matches['Datetime'].dt.date
matches['Time'] = matches['Datetime'].dt.time
matches= matches.drop(columns=['Datetime'])

matches.dtypes
matches['Year'] = pd.to_datetime(matches['Year'], format='%Y')
matches['Datetime'] = pd.to_datetime(matches['Datetime'], format='mixed')
matches['Stage'] = matches['Stage'].astype(str)
matches['Stadium'] = matches['Stadium'].astype(str)
matches['City'] = matches['City'].astype(str)
matches['Home Team Name'] = matches['Home Team Name'].astype(str)
matches['Away Team Name'] = matches['Away Team Name'].astype(str)
matches['Win conditions'] = matches['Win conditions'].astype(str)

matches['Attendance'] = matches['Attendance'].fillna(0)
matches['Attendance'] = matches['Attendance'].astype(int)

matches['Referee'] = matches['Referee'].astype(str)
matches['Assistant 1'] = matches['Assistant 1'].astype(str)
matches['Assistant 2'] = matches['Assistant 2'].astype(str)
matches['Home Team Initials'] = matches['Home Team Initials'].astype(str)
matches['Away Team Initials'] = matches['Away Team Initials'].astype(str)

cups.dtypes
cups['Year'] = pd.to_datetime(cups['Year'],  format='%Y')
cups['Country'] = cups['Country'].astype(str)
cups['Winner'] = cups['Winner'].astype(str)
cups['Runners-Up'] = cups['Runners-Up'].astype(str)
cups['Third'] = cups['Third'].astype(str)
cups['Fourth'] = cups['Fourth'].astype(str)

def convert_attendance(value):
    value = value.replace('.', '')
    return int(float(value))
cups['Attendance'] = cups['Attendance'].apply(convert_attendance)



#Home Advantages
#Home wins 488 matches, away wins 174, draw 190 matches.
#Calculate match outcome
matches['Result'] = matches.apply(lambda row: 'Home Win' if row['Home Team Goals'] > row['Away Team Goals'] 
                                  else ('Away Win' if row['Home Team Goals'] < row['Away Team Goals'] else 'Draw'), axis=1)
#Count the number of wins, losses, and draws
outcome_counts = matches['Result'].value_counts()

plt.figure(figsize=(8, 6))
sns.barplot(x=outcome_counts.index, y=outcome_counts.values)
plt.title('Match Outcomes (Home Wins vs Away Wins vs Draws)')
plt.show()


#Goal comparison between stages
#Aggregate total goals per stage
matches['Total Goals'] = matches['Home Team Goals'] + matches['Away Team Goals']
stage_goals = matches.groupby('Stage')['Total Goals'].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(x='Stage', y='Total Goals', data=stage_goals)
plt.title('Average Goals per Stage in World Cups')
plt.show()


#Attendance over the years
#average attendance increased over the years
#Group by year and calculate average attendance
attendance_per_year = matches.groupby('Year')['Attendance'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='Attendance', data=attendance_per_year)
plt.title('Average Attendance Over World Cups')
plt.show()


#Goals analysis: Full time vs Half time
#Second half home > Half time home > Second half away > half time away
#Calculate second-half goals
matches['Second Half Home Goals'] = matches['Home Team Goals'] - matches['Half-time Home Goals']
matches['Second Half Away Goals'] = matches['Away Team Goals'] - matches['Half-time Away Goals']

# Aggregate full-time and half-time goals
half_full_goals = matches[['Half-time Home Goals', 'Half-time Away Goals', 'Second Half Home Goals', 'Second Half Away Goals']].sum()

plt.figure(figsize=(10, 6))
half_full_goals.plot(kind='bar')
plt.title('Comparison of Half-time vs Full-time Goals')
plt.show()


#Top scoring matches
#Identify matches with the highest total goals
high_scoring_matches = matches[['Year', 'Home Team Name', 'Away Team Name', 'Home Team Goals', 'Away Team Goals']].copy()
high_scoring_matches['Total Goals'] = high_scoring_matches['Home Team Goals'] + high_scoring_matches['Away Team Goals']

#Sort and display top 5 highest scoring matches
top_matches = high_scoring_matches.sort_values(by='Total Goals', ascending=False).head(5)
print(top_matches)


#Most successful teams in the World Cup.#BRAZIL is the most successful team
#Count the number of World Cup wins by each country
winners_count = cups['Winner'].value_counts().reset_index()
winners_count.columns = ['Country', 'Wins']

plt.figure(figsize=(10, 6))
sns.barplot(x='Country', y='Wins', data=winners_count)
plt.title('Countries with the Most World Cup Wins')
plt.show()


#Goals scored over the years. Every year goals scored increases.
plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='GoalsScored', data=cups)
plt.title('Total Goals Scored in Each World Cup')
plt.show()


#Attendance trend over the years. Every year attendance increases.
plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='Attendance', data=cups)
plt.title('Attendance Over World Cup Tournaments')
plt.show()


#Host country performance
#Identify instances where the host country finished in the top 4
host_performance = cups[(cups['Country'] == cups['Winner']) | (cups['Country'] == cups['Runners-Up']) |
                        (cups['Country'] == cups['Third']) | (cups['Country'] == cups['Fourth'])]

#Count how often the host country finished in the top 4
host_top4_count = host_performance['Country'].value_counts()

# Plot the host country performance
plt.figure(figsize=(10, 6))
sns.barplot(x=host_top4_count.index, y=host_top4_count.values)
plt.title('Host Country Performance (Top 4 Finishes)')
plt.show()


#Correlation between goals scored and winning
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Year', y='GoalsScored', data=cups, hue='Winner')
plt.title('Goals Scored by Winning Teams Over Time')
plt.show()


#Host country advantage
host_advantage = cups[cups['Country'] == cups['Winner']].shape[0]
print(f'The host country won the World Cup {host_advantage} times.')



