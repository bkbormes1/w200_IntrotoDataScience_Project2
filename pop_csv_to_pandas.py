import pandas as pd

pop_data = pd.read_csv('pop_by_state_by_year.csv')

#Display data
print(pop_data)
print(pop_data.describe())