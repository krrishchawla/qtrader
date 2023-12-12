import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_name = 'MACY_test.csv'  # Replace with your actual file name
df = pd.read_csv(file_name)

# Convert 'time' to datetime and sort the data
df['time'] = pd.to_datetime(df['time'])
df.sort_values('time', inplace=True)

# Sample list for color coding
# Replace with your actual list of values
# color_list = [2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1]
# Mcdonalds
# Sentiment
# Optimal
# color_list = [1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1]
# Random
# color_list = [1, 0, 2, 1, 2, 1, 1, 2, 0, 1, 2, 0, 1, 1, 2, 2, 2, 0, 0, 1, 0, 2, 0, 0, 0, 1]
# All hold
# color_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# No Sentiment
# color_list = [1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1]
# color_list = [1, 2, 0, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 1, 2, 1, 2, 0, 0, 0, 2, 2, 0, 1, 1]
# color_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Google
# color_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1]
# color_list = [2, 1, 0, 2, 0, 0, 0, 1, 1, 1, 2, 0, 2, 1, 2, 2, 2, 0, 0, 0, 0, 1, 0, 2, 1, 1]
# color_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# color_list = [2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1]
# color_list = [0, 0, 1, 1, 1, 0, 1, 0, 2, 1, 0, 2, 0, 1, 0, 2, 2, 2, 0, 2, 2, 0, 1, 1, 1, 1]
# color_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Macy's
# color_list = [2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
# color_list = [0, 0, 1, 0, 0, 2, 1, 0, 2, 0, 2, 2, 1, 0, 0, 1, 0, 0, 2, 0, 0, 1, 1, 1, 0, 1]
# color_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# color_list = [2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1]
# color_list = [1, 0, 0, 1, 0, 2, 1, 0, 2, 2, 0, 0, 1, 2, 0, 1, 1, 0, 0, 0, 2, 1, 0, 2, 0, 1]
# color_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['close'], marker='o', color='black', label='Closing Price')  # Black line

# Adding colored dots based on the list values
for i in range(len(df)):
    if color_list[i] == 1:
        plt.plot(df['time'].iloc[i], df['close'].iloc[i], 'go', label='Policy 1' if i == 0 else "")
    elif color_list[i] == 2:
        plt.plot(df['time'].iloc[i], df['close'].iloc[i], 'ro', label='Policy 2' if i == 0 else "")

plt.title('Time vs Price with Policy Indication')
plt.xlabel('Time (Weeks)')
plt.ylabel('Price')
plt.grid(True)
plt.xticks(rotation=45)

# Adding the legend
# plt.legend()
plt.show()
