import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import time
import datetime



df = pd.read_csv("bitcoinmay.csv")
#df = pd.read_csv("bc1w.csv")

df.dropna(how="any", inplace=True) #drop any rows with NaN values

bc_mean = df.Close.mean() #get the Average Price of Bitcoin w/in the period
bc_mean_arr = np.repeat(bc_mean, df.Date.size)

dt_arr = []

month_map = {"01": "January",
			 "02": "February",
			 "03": "March",
			 "04": "April",
			 "05": "May",
			 "06": "June",
			 "07": "July",
			 "08": "August",
			 "09": "September",
			 "10": "October",
			 "11": "November",
			 "12": "December"}

for i in range(df.Date.size): #make Date entries as datetime objects
														   #"%m/%d/%Y"
	 dt_arr.append(datetime.datetime.strptime(df.Date[i], "%m/%d/%Y"))


df["Date"] = dt_arr #put it back in the dataframe
df.Date = pd.to_datetime(df.Date, format="%m/%d/%Y")


fig = plt.figure()

ax1 = plt.subplot2grid((2,1), (0,0), rowspan=1, colspan=1)

fr = month_map[dt_arr[0].strftime("%m/%d")[0:2]] + " " + dt_arr[0].strftime("%m/%d")[3:5]
till = month_map[dt_arr[-1].strftime("%m/%d")[0:2]] + " " + dt_arr[-1].strftime("%m/%d/%Y")[3:5] + ", " + dt_arr[-1].strftime("%m/%d/%Y")[6:]
plt.title("Bitcoin Prices from "+ fr + " - " + till, color="#232323", fontsize=16)
plt.ylabel("Prices($, USD)", color="#232323", fontsize=14)

ax2 = plt.subplot2grid((2,1), (1,0), rowspan=1, colspan=1)
plt.xlabel("Dates", color="#232323", fontsize=14)
plt.ylabel("Prices($, USD)", color="#232323", fontsize=14)



ax1.plot(df.Date, df.Close, color="#232323")
ax1.scatter(df.Date.values[:], df.Close.values[:], color="#232323", s=20)


ax1.fill_between(df.Date.values[:], df.Close.values[:], bc_mean_arr, where=(df.Close.values[:] > bc_mean_arr), facecolor="#32bd12", edgecolor="#32bd12", alpha=0.3)
ax1.fill_between(df.Date.values[:], df.Close.values[:], bc_mean_arr, where=(df.Close.values[:] < bc_mean_arr), facecolor="red", edgecolor="red", alpha=0.3)


ax1.text(0.025, 2.1, "Average Price: $" + str(round(bc_mean, 2)), transform=plt.gca().transAxes, fontdict=dict(color="#5f717b", size=12))
ax1.annotate("Dates with Prices < Avg. Price", (df.Date.values[10], bc_mean + 100), xytext=(df.Date.values[6], bc_mean + 350), arrowprops=dict(facecolor="red", edgecolor="red", alpha=0.3), color="red")
ax1.annotate("Dates with Prices > Avg. Price", (df.Date.values[23], bc_mean - 75), xytext=(df.Date.values[20], bc_mean - 350), arrowprops=dict(facecolor="#32bd12", edgecolor="#32bd12", alpha=0.3), color="green")

plt.setp(ax1.xaxis.get_ticklabels(), visible=False)

ax2.plot(df.Date, df.Close, color="#232323")
ax2.scatter(df.Date.values[:], df.Close.values[:], color="#232323", s=20)
ax2.fill_between(df.Date.values[:], df.Close.values[:], df.Close[0], where=(df.Close.values[:] >= df.Close[0]), facecolor="#32bd12", edgecolor="#32bd12", alpha=0.3)
ax2.fill_between(df.Date.values[:], df.Close.values[:], df.Close[0], where=(df.Close.values[:] <= df.Close[0]), facecolor="red", edgecolor="red", alpha=0.3)

for tck in ax2.xaxis.get_ticklabels():
	tck.set_rotation(45)
	tck.set_size(9)
ax2.xaxis.set_major_locator(mticker.MaxNLocator(nbins=21))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))

ax2.annotate("Dates with Prices < " + fr + " Prices", (df.Date.values[0], df.Close.values[0] + 250), xytext=(df.Date.values[1], 1800), arrowprops=dict(facecolor="red", edgecolor="red", alpha=0.3), color="red")
ax2.annotate("Dates with Prices > " + fr + " Prices", (df.Date.values[16], df.Close.values[16] + 250), xytext=(df.Date.values[12], 2300), arrowprops=dict(facecolor="#32bd12", edgecolor="#32bd12", alpha=0.3), color="green")

ax2.text(0.030, 0.9, fr + " Price: $" + str(round(df.Close.values[1], 2)), transform=plt.gca().transAxes, fontdict=dict(color="#5f717b", size=12))

ax1.grid(True)
ax2.grid(True)


fig1 = plt.figure()
ax3 = plt.subplot2grid((3,2), (0,0), rowspan=2, colspan=2)

mod_dates = []
xlabs = []

for x in range(0, len(dt_arr)):
	mod_dates.append(dt_arr[x].strftime("%m/%d"))


for y in range(1, len(dt_arr)):
	xlabs.append(mod_dates[y-1] + " - " + mod_dates[y])

df_bar = pd.DataFrame({"xlabels": xlabs})


plt.xticks(np.arange(1, len(xlabs) + 1), xlabs, rotation=45)
plt.title("Daily (%)changes in Bitcoin Prices from " + fr + " - " + till, color="#232323", fontsize=16)

plt.ylabel("Percentage(%)", color="#232323", fontsize=14)
ax4 = plt.subplot2grid((3,2), (2,0), rowspan=1, colspan=1)
ax5 = plt.subplot2grid((3,2), (2,1), rowspan=1, colspan=1)

pct_changes = []

for c in range(1, len(df.Close.values)):
	v = 100 * (df.Close.values[c] - df.Close.values[c-1]) / df.Close.values[c]
	pct_changes.append(v)

changes = pd.Series(pct_changes, name="changes")

df_bar = pd.concat([df_bar, changes], axis=1)

df_bar.set_index(np.arange(1, len(pct_changes) + 1), inplace=True)

ps = df_bar.loc[df_bar.changes > 0, "changes"]
ng = df_bar.loc[df_bar.changes < 0, "changes"]


ax3.bar(ps.index.values, ps.values, edgecolor="#2e933c", color="#2e933c")
ax3.bar(ng.index.values, ng.values, edgecolor="#e84a50", color="#e84a50")

for tck3 in ax3.xaxis.get_ticklabels():
	tck3.set_size(8)


ax4.pie([len(ps), len(ng)], labels=["Increased Days", "Decreased Days"], colors=["#0cb4e8", "#d63333"], startangle=0, shadow=True, explode=(0.0, 0.1), autopct="%1.2f%%", textprops=dict(color="#232323", fontsize=10))
ax4.text(-1.12, -0.3,"No. of increased days vs No. of decreased days", transform=plt.gca().transAxes, color="#232323", fontdict=dict(color="#232323", size=13))

ax5.pie([sum(df.Close.values[:] > bc_mean_arr), sum(df.Close.values[:] < bc_mean_arr)], labels=["Days above Avg.", "Days below Avg."], colors=["#4fd851", "#ff651d"], startangle=0, shadow=True, explode=(0.0, 0.1), autopct="%1.2f%%", textprops=dict(color="#232323", fontsize=10))
ax5.text(-0.075, -0.3,"No. of days above avg. price vs No. of days below avg. price", transform=plt.gca().transAxes, color="#232323", fontdict=dict(color="#232323", size=13))

fig1.subplots_adjust(hspace=0.7)

fwrite = open("bitcoin_stats(" + fr + " - " + till+ ").txt", "w")

def round_up(val):
	return str(round(val, 2))

def write_dates(fw, dates, isdate):
	tp = ()
	if isdate:
		for t1 in dates:
			tp += (pd.to_datetime(t1).strftime("%m/%d/%Y"), )
		fw.write("Dates " + str(tp) + nl)
	else:
		for t1 in dates:
			tp += (t1, )
		fw.write("Dates " + str(tp) + nl)
	return



nl = "\n"
fwrite.write("Bitcoin Price STATS " + "(" + fr + " - " + till + ")" + "\n\n")
fwrite.write("Average Price: " + "$" + round_up(bc_mean) + nl + "Median Price: " + "$" + round_up(df.Close.median()) + nl)
fwrite.write("%Change " + fr + " - " + till +  "(" + str(len(dt_arr)) + " days" + "): " + round_up(100 * (df.Close[30] / df.Close[0])) + "%" + nl)
fwrite.write("Average increase(Days with increased prices): " + round_up(np.array(ps).mean()) + "%" + nl + "Average decrease(Days with decreased prices): " + round_up(np.array(ng).mean()) + "%" + nl)
fwrite.write("\n")
fwrite.write("Highest Price: " + "$" + round_up(df.Close.max()) + " at " +  pd.to_datetime(df.loc[df.Close == df.Close.values.max(), "Date"].values[0]).strftime("%m/%d/%Y") + nl)
fwrite.write("Lowest Price: " + "$" + round_up(df.Close.min()) + " at " +  pd.to_datetime(df.loc[df.Close == df.Close.values.min(), "Date"].values[0]).strftime("%m/%d/%Y") + nl)
fwrite.write("Highest 1 day Price increase: " + round_up(df_bar.changes.max()) + "%" + " at " + df_bar.loc[df_bar.changes == df_bar.changes.values.max(), "xlabels"].values[0] + nl)

hw = df_bar.loc[df_bar.changes > 0, "changes"].values.min()
h_write = df_bar.loc[df_bar.changes == hw, "xlabels"].values[0] 
fwrite.write("Lowest 1 day Price increase: " + round_up(hw) + "%" + " at " + h_write + nl)

fwrite.write("Highest 1 day Price decrease: " + round_up(df_bar.changes.min()) + "%" + " at " + df_bar.loc[df_bar.changes == df_bar.changes.values.min(), "xlabels"].values[0] + nl)

hw1 = df_bar.loc[df_bar.changes < 0, "changes"].values.max()
h_write1 = df_bar.loc[df_bar.changes == hw1, "xlabels"].values[0]
fwrite.write("Lowest 1 day Price increase: " + round_up(hw1) + "%" + " at " + h_write1 + nl)

fwrite.write("\n")

fwrite.write("No. of Days above Avg. Price: " + str(df.loc[df.Close > bc_mean, "Close"].size) + " | ")
write_dates(fwrite, df.loc[df.Close > bc_mean, "Date"].values, True)
fwrite.write("No. of Days below Avg. Price: " + str(df.loc[df.Close < bc_mean, "Close"].size) + " | ")
write_dates(fwrite, df.loc[df.Close < bc_mean, "Date"].values, True)

fwrite.write("No. of Days above " + fr + " Price: " + str(df.loc[df.Close > df.Close.values[1], "Date"].size) + " | ") #modular
write_dates(fwrite, df.loc[df.Close > df.Close.values[1], "Date"].values, True)
fwrite.write("No. of Days below or equal to" + fr + " Price: " + str(df.loc[df.Close < df.Close.values[1], "Date"].size) + " | ") #modular 
write_dates(fwrite, df.loc[df.Close <= df.Close.values[1], "Date"].values, True)

fwrite.write("No. of days with increased prices(relative to previous): " + str(df_bar.loc[df_bar.changes > 0, "changes"].size) + " | ")
write_dates(fwrite, df_bar.loc[df_bar.changes > 0, "xlabels"].values, False)
fwrite.write("No. of days with decreased prices(relative to previous): " + str(df_bar.loc[df_bar.changes < 0, "changes"].size) + " | ")
write_dates(fwrite, df_bar.loc[df_bar.changes < 0, "xlabels"].values, False)

fwrite.close()

print(df)
print(df_bar)
plt.show()
