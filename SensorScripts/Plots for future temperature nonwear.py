import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# # Create Scatter plots for future temp changes

df_1min = pd.read_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_1MIN_TEMP_CHANGES.csv")
df_3min = pd.read_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_3MIN_TEMP_CHANGES.csv")
df_5min = pd.read_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_5MIN_TEMP_CHANGES.csv")
df_10min = pd.read_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_10MIN_TEMP_CHANGES.csv")

plt.figure()
fig, ((ax,ax1)) = plt.subplots(2, 2,sharey=True)#, gridspec_kw={'height_ratios': [3, 3]})
fig.suptitle("Temperature N Minutes After Start")
ax[0].scatter(df_1min["STARTING TEMP"], df_1min["TEMP 1 MINS AFTER START"]-df_1min["STARTING TEMP"],10)
ax[0].hlines(np.average( df_1min["TEMP 1 MINS AFTER START"]-df_1min["STARTING TEMP"]),np.min(df_1min["STARTING TEMP"]),np.max(df_1min["STARTING TEMP"]),linestyles="dashed")
ax[0].set_title("1 MIN")
ax[1].scatter(df_3min["STARTING TEMP"], df_3min["TEMP 3 MINS AFTER START"]-df_3min["STARTING TEMP"],10)
ax[1].hlines(np.average( df_3min["TEMP 3 MINS AFTER START"]-df_3min["STARTING TEMP"]),np.min(df_3min["STARTING TEMP"]),np.max(df_3min["STARTING TEMP"]),linestyles="dashed")
ax[1].set_title("3 MINS")
ax1[0].scatter(df_5min["STARTING TEMP"], df_5min["TEMP 5 MINS AFTER START"]-df_5min["STARTING TEMP"],10)
ax1[0].hlines(np.average( df_5min["TEMP 5 MINS AFTER START"]-df_5min["STARTING TEMP"]),np.min(df_5min["STARTING TEMP"]),np.max(df_5min["STARTING TEMP"]),linestyles="dashed")
ax1[0].set_title("5 MINS")
ax1[1].scatter(df_10min["STARTING TEMP"], df_10min["TEMP 10 MINS AFTER START"]-df_10min["STARTING TEMP"],10)
ax1[1].hlines(np.average( df_10min["TEMP 10 MINS AFTER START"]-df_10min["STARTING TEMP"]),np.min(df_10min["STARTING TEMP"]),np.max(df_10min["STARTING TEMP"]),linestyles="dashed")
ax1[1].set_title("10 MINS")

ax1[0].set_xlabel("STARTING Temperature")
ax1[1].set_xlabel("STARTING Temperature")
ax[0].set_ylabel("Temperature Change")
ax1[0].set_ylabel("Temperature Change")



## Create Individual Plots for each


# 1 min
plt.figure()
plt.scatter(df_1min["STARTING TEMP"], df_1min["TEMP 1 MINS AFTER START"]-df_1min["STARTING TEMP"],10)
average = np.average( df_1min["TEMP 1 MINS AFTER START"]-df_1min["STARTING TEMP"])
plt.hlines(average,np.min(df_1min["STARTING TEMP"]),np.max(df_1min["STARTING TEMP"]),linestyles="dashed")
plt.title("Temperature 1 Minutes after Start")
plt.xlabel("Starting Temperature")
plt.ylabel("Temperature Change")


# 3 Min
plt.figure()
plt.scatter(df_3min["STARTING TEMP"], df_3min["TEMP 3 MINS AFTER START"]-df_3min["STARTING TEMP"],10)
average = np.average( df_3min["TEMP 3 MINS AFTER START"]-df_3min["STARTING TEMP"])
plt.hlines(average,np.min(df_3min["STARTING TEMP"]),np.max(df_3min["STARTING TEMP"]),linestyles="dashed")
plt.title("Temperature 3 Minutes after Start")
plt.xlabel("Starting Temperature")
plt.ylabel("Temperature Change")


# 5 Min
plt.figure()
plt.scatter(df_5min["STARTING TEMP"], df_5min["TEMP 5 MINS AFTER START"]-df_5min["STARTING TEMP"],10)
average = np.average( df_5min["TEMP 5 MINS AFTER START"]-df_5min["STARTING TEMP"])
plt.hlines(average,np.min(df_5min["STARTING TEMP"]),np.max(df_5min["STARTING TEMP"]),linestyles="dashed")
plt.title("Starting 5 Minutes after Start")
plt.xlabel("Starting Temperature")
plt.ylabel("Temperature Change")


# 10 Min
plt.figure()
plt.scatter(df_10min["STARTING TEMP"], df_10min["TEMP 10 MINS AFTER START"]-df_10min["STARTING TEMP"],10)
average = np.average( df_10min["TEMP 10 MINS AFTER START"]-df_10min["STARTING TEMP"])
plt.hlines(average,np.min(df_10min["STARTING TEMP"]),np.max(df_10min["STARTING TEMP"]),linestyles="dashed")
plt.title("Temperature 10 Minutes after Start")
plt.xlabel("Starting Temperature")
plt.ylabel("Temperature Change")
plt.show()

########### SAME THING BUT FOR THE END ############
# Create Scatter plots for future temp changes

df_1min = pd.read_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_1MIN_TEMP_CHANGES.csv")
df_3min = pd.read_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_3MIN_TEMP_CHANGES.csv")
df_5min = pd.read_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_5MIN_TEMP_CHANGES.csv")
df_10min = pd.read_csv(r"D:\Adam PC\PycharmProjects\owcurate\Outputs\OND06_10MIN_TEMP_CHANGES.csv")

plt.figure()
fig, ((ax,ax1)) = plt.subplots(2, 2,sharey=True)#, gridspec_kw={'height_ratios': [3, 3]})
fig.suptitle("Temperature N Minutes After End")
ax[0].scatter(df_1min["ENDING TEMP"], df_1min["TEMP 1 MINS AFTER END"]-df_1min["ENDING TEMP"],10)
ax[0].hlines(np.average( df_1min["TEMP 1 MINS AFTER END"]-df_1min["ENDING TEMP"]),np.min(df_1min["ENDING TEMP"]),np.max(df_1min["ENDING TEMP"]),linestyles="dashed")
ax[0].set_title("1 MIN")
ax[1].scatter(df_3min["ENDING TEMP"], df_3min["TEMP 3 MINS AFTER END"]-df_3min["ENDING TEMP"],10)
ax[1].hlines(np.average( df_3min["TEMP 3 MINS AFTER END"]-df_3min["ENDING TEMP"]),np.min(df_3min["ENDING TEMP"]),np.max(df_3min["ENDING TEMP"]),linestyles="dashed")
ax[1].set_title("3 MINS")
ax1[0].scatter(df_5min["ENDING TEMP"], df_5min["TEMP 5 MINS AFTER END"]-df_5min["ENDING TEMP"],10)
ax1[0].hlines(np.average( df_5min["TEMP 5 MINS AFTER END"]-df_5min["ENDING TEMP"]),np.min(df_5min["ENDING TEMP"]),np.max(df_5min["ENDING TEMP"]),linestyles="dashed")
ax1[0].set_title("5 MINS")
ax1[1].scatter(df_10min["ENDING TEMP"], df_10min["TEMP 10 MINS AFTER END"]-df_10min["ENDING TEMP"],10)
ax1[1].hlines(np.average( df_10min["TEMP 10 MINS AFTER END"]-df_10min["ENDING TEMP"]),np.min(df_10min["ENDING TEMP"]),np.max(df_10min["ENDING TEMP"]),linestyles="dashed")
ax1[1].set_title("10 MINS")

ax1[0].set_xlabel("Ending Temperature")
ax1[1].set_xlabel("Ending Temperature")
ax[0].set_ylabel("Temperature Change")
ax1[0].set_ylabel("Temperature Change")



## Create Individual Plots for each


# 1 min
plt.figure()
plt.scatter(df_1min["ENDING TEMP"], df_1min["TEMP 1 MINS AFTER END"]-df_1min["ENDING TEMP"],10)
average = np.average( df_1min["TEMP 1 MINS AFTER END"]-df_1min["ENDING TEMP"])
plt.hlines(average,np.min(df_1min["ENDING TEMP"]),np.max(df_1min["ENDING TEMP"]),linestyles="dashed")
plt.title("Temperature 1 Minutes after End")
plt.xlabel("Ending Temperature")
plt.ylabel("Temperature Change")


# 3 Min
plt.figure()
plt.scatter(df_3min["ENDING TEMP"], df_3min["TEMP 3 MINS AFTER END"]-df_3min["ENDING TEMP"],10)
average = np.average( df_3min["TEMP 3 MINS AFTER END"]-df_3min["ENDING TEMP"])
plt.hlines(average,np.min(df_3min["ENDING TEMP"]),np.max(df_3min["ENDING TEMP"]),linestyles="dashed")
plt.title("Temperature 3 Minutes after End")
plt.xlabel("Ending Temperature")
plt.ylabel("Temperature Change")


# 5 Min
plt.figure()
plt.scatter(df_5min["ENDING TEMP"], df_5min["TEMP 5 MINS AFTER END"]-df_5min["ENDING TEMP"],10)
average = np.average( df_5min["TEMP 5 MINS AFTER END"]-df_5min["ENDING TEMP"])
plt.hlines(average,np.min(df_5min["ENDING TEMP"]),np.max(df_5min["ENDING TEMP"]),linestyles="dashed")
plt.title("Ending 5 Minutes after End")
plt.xlabel("Starting Temperature")
plt.ylabel("Temperature Change")


# 10 Min
plt.figure()
plt.scatter(df_10min["ENDING TEMP"], df_10min["TEMP 10 MINS AFTER END"]-df_10min["ENDING TEMP"],10)
average = np.average( df_10min["TEMP 10 MINS AFTER END"]-df_10min["ENDING TEMP"])
plt.hlines(average,np.min(df_10min["ENDING TEMP"]),np.max(df_10min["ENDING TEMP"]),linestyles="dashed")
plt.title("Temperature 10 Minutes after End")
plt.xlabel("Ending Temperature")
plt.ylabel("Temperature Change")
plt.show()

# Create Histograms
plt.figure()
fig, ((ax,ax1)) = plt.subplots(2, 2)#, gridspec_kw={'height_ratios': [3, 3]})
fig.suptitle("Temperature N Minutes After Start")
counts, bins, patches = ax[0].hist(df_1min["TEMP 1 MINS AFTER START"],range(int(np.min(df_1min["TEMP 1 MINS AFTER START"])),int(np.max(df_1min["TEMP 1 MINS AFTER START"]))),edgecolor = "black", linewidth = 1.2)
ax[0].set_xticks(bins)
ax[0].vlines(np.average(df_1min["TEMP 1 MINS AFTER START"]), 0, np.max(counts), linestyles = "dashed", colors = "orange")
ax[0].set_title("1 MIN")
counts, bins, patches = ax[1].hist(df_3min["TEMP 3 MINS AFTER START"],range(int(np.min(df_3min["TEMP 3 MINS AFTER START"])),int(np.max(df_3min["TEMP 3 MINS AFTER START"]))),edgecolor = "black", linewidth = 1.2)
ax[1].set_xticks(bins)
ax[1].vlines(np.average(df_3min["TEMP 3 MINS AFTER START"]), 0, np.max(counts), linestyles = "dashed", colors = "orange")
ax[1].set_title("3 MINS")
counts, bins, patches = ax1[0].hist(df_5min["TEMP 5 MINS AFTER START"],range(int(np.min(df_5min["TEMP 5 MINS AFTER START"])),int(np.max(df_5min["TEMP 5 MINS AFTER START"]))),edgecolor = "black", linewidth = 1.2)
ax1[0].set_xticks(bins)
ax1[0].vlines(np.average(df_5min["TEMP 5 MINS AFTER START"]), 0, np.max(counts), linestyles = "dashed", colors = "orange")
ax1[0].set_title("5 MINS")
counts, bins, patches = ax1[1].hist(df_10min["TEMP 10 MINS AFTER START"],range(int(np.min(df_10min["TEMP 10 MINS AFTER START"])),int(np.max(df_10min["TEMP 10 MINS AFTER START"]))),edgecolor = "black", linewidth = 1.2)
ax1[1].set_xticks(bins)
ax1[1].vlines(np.average(df_10min["TEMP 10 MINS AFTER START"]), 0, np.max(counts), linestyles = "dashed", colors = "orange")
ax1[1].set_title("10 MINS")

ax1[0].set_xlabel("Temperature")
ax1[1].set_xlabel("Temperature")


## Create Individual Plots for each

# 1 min
plt.figure()
counts, bins, patches = plt.hist(df_1min["TEMP 1 MINS AFTER START"],range(int(np.min(df_1min["TEMP 1 MINS AFTER START"])),int(np.max(df_1min["TEMP 1 MINS AFTER START"]))),edgecolor = "black", linewidth = 1.2)
plt.xticks(bins)
plt.vlines(np.average(df_1min["TEMP 1 MINS AFTER START"]), 0, np.max(counts), linestyles = "dashed", colors = "orange")
plt.title("Temperature 1 Minutes after Start")
plt.xlabel("Temperature")


# 3 Min
plt.figure()
counts, bins, patches = plt.hist(df_3min["TEMP 3 MINS AFTER START"],range(int(np.min(df_3min["TEMP 3 MINS AFTER START"])),int(np.max(df_3min["TEMP 3 MINS AFTER START"]))),edgecolor = "black", linewidth = 1.2)
plt.xticks(bins)
plt.vlines(np.average(df_3min["TEMP 3 MINS AFTER START"]), 0, np.max(counts), linestyles = "dashed", colors = "orange")
plt.title("Temperature 3 Minutes after Start")
plt.xlabel("Temperature")


# 5 Min
plt.figure()
counts, bins, patches = plt.hist(df_5min["TEMP 5 MINS AFTER START"],range(int(np.min(df_5min["TEMP 5 MINS AFTER START"])),int(np.max(df_5min["TEMP 5 MINS AFTER START"]))),edgecolor = "black", linewidth = 1.2)
plt.xticks(bins)
plt.vlines(np.average(df_5min["TEMP 5 MINS AFTER START"]), 0, np.max(counts), linestyles = "dashed", colors = "orange")
plt.title("Temperature 5 Minutes after Start")
plt.xlabel("Temperature")


# 10 Min
plt.figure()
counts, bins, patches = plt.hist(df_10min["TEMP 10 MINS AFTER START"],range(int(np.min(df_10min["TEMP 10 MINS AFTER START"])),int(np.max(df_10min["TEMP 10 MINS AFTER START"]))),edgecolor = "black", linewidth = 1.2)
plt.xticks(bins)
plt.vlines(np.average(df_10min["TEMP 10 MINS AFTER START"]), 0, np.max(counts), linestyles = "dashed", colors = "orange")
plt.title("Temperature 10 Minutes after Start")
plt.xlabel("Temperature")