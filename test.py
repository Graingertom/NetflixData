#Import useful packages
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
from pandas.io.parsers import TextParser

#Read the csv file with the dataset we will be using
nf=pd.read_csv(r"C:\Pythonfiles\My Netflix Data - Sheet1.csv")

#Now we will work out whether we watched more Movies or Series, starting by counting the number of Series and Movies in the dataset
from collections import Counter
print(Counter(nf['Movie_Series']))

#Grouping the dataset removes any unnecessary columns from our dataset
title_type = nf.groupby('Movie_Series').agg('count')
print(title_type)

#import the needed packages to create clearer graphs and charts
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.gridspec import GridSpec

#Sort the data to give x and y variables for our chart
type_labels = title_type.Show_Name.sort_values().index
type_counts = title_type.Show_Name.sort_values()

#Define variables and ask to plot a pie chart, we will show the two seperate charts at the end so we can make a comparison
fig, ax1 = plt.subplots(figsize=(6,3), subplot_kw=dict(aspect="equal"))

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d})".format(pct, absolute)

wedges, texts, autotexts = ax1.pie(type_counts, autopct=lambda pct: func(pct, type_counts),
                                    textprops=dict(color='w'))

ax1.legend(wedges, type_labels,
            title='Type of Show',
            loc='center left',
            bbox_to_anchor=(1, 0, 0.5, 1)) 

plt.setp(autotexts, size=8, weight="bold")

ax1.set_title("Netflix Title Type by Number of Shows Watched")

#Pie chart 1 is finished but we want to compare the title types and minutes watched so we create another chart
WatchSplit = nf.groupby(by=['Movie_Series'])["Total_Watched"].sum()
print(WatchSplit)

fig, ax2 = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

TitleType = ['Movie', 'Series']
MinutesWatched = [1835, 10380]

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d} mins)".format(pct, absolute)

wedges, texts, autotexts = ax2.pie(MinutesWatched, autopct=lambda pct: func(pct, MinutesWatched),
                                    textprops=dict(color='w'))

ax2.legend(wedges, TitleType,
            title='Type of Show',
            loc='center left',
            bbox_to_anchor=(1, 0, 0.5, 1)) 

plt.setp(autotexts, size=8, weight="bold")

ax2.set_title("Netflix Title Type by Minutes Watched")

#Now we can show the two charts together and make our comparisons as you can see although the split between titles is almost 50/50 there is clearly a larger amount of minutes watched for Series vs Movies
plt.show()

#Now let us see what we watched the most of by minutes watched, we start with sorting the values by total minutes watched and only showing the top 5
TopWatched = nf.sort_values(by=['Total_Watched'], ascending=False)
Top5Watched = TopWatched.head()
print(Top5Watched)

#We can now create a horizontal bar chart to clearly show these top 5 and the amount of time spent watching them
fig, ax3 = plt.subplots(figsize=(17, 8), dpi=70)
ax3.barh(Top5Watched['Show_Name'], Top5Watched['Total_Watched'], align='center')
ax3.set_yticks(Top5Watched['Show_Name'], labels=Top5Watched['Show_Name'])
ax3.invert_yaxis()
ax3.set_xlabel('Minutes Watched')
ax3.set_title('Top 5 Netflix Shows by Minutes Watched')

plt.show()

#How about we look at the genres watched and see what was most popular, first lets group the data and count each genre
print(Counter(nf['Genre']))

genre_type = nf.groupby('Genre').agg('count')

#Again sort the data to give x and y variables for our graph
genre_labels = genre_type.Show_Name.sort_values().index
genre_counts = genre_type.Show_Name.sort_values()

#Plot a bar chart to see a clear comparison of what genres of title were chosen, we will wait to show the chart so we can compare later on.
fig, ax4 = plt.subplots(figsize=(17, 8), dpi=70)
ax4.bar(genre_labels, genre_counts, align='center')
ax4.set_yticks(genre_counts, lables=genre_counts)
ax4.set_xlabel('Genre of Show Watched')
ax4.set_title('Distribution of genres by number of shows watched')

#Now how does this differ for minutes watched. We can use our TopWatched dataframe from before. However we need to group the genres up with the time watched.

GenresWatched = TopWatched.groupby(["Genre"]).Total_Watched.sum().reset_index()
print(GenresWatched)

#Now we can use this to plot another horizontal bar chart
fig, ax5 = plt.subplots(figsize=(17, 8), dpi=70)
ax5.bar(GenresWatched['Genre'], GenresWatched['Total_Watched'], align='center')
ax5.set_yticks(GenresWatched['Total_Watched'], labels=GenresWatched['Total_Watched'])
ax5.set_xlabel('Genre of Show Watched')
ax5.set_title('Top Genres of Netflix Shows by Minutes Watched')

plt.show()

#Finally let us see how good we've been at finishing what we've started. We will use the Finished column but we must turn our 'Y' and 'N' into True and False.

nf['Finished'] = nf['Finished'].map(
                {'Y':True ,'N':False})

#We are printing the column to check the changes have been made
print(nf['Finished'])

#Now let's plot a pie chart against this Boolean column
print(Counter(nf['Finished']))

#Group the dataset and count so we can use this number for our pie chart
was_finished = nf.groupby('Finished').agg('count')
print(was_finished)

#sort the values so we can input them into our graph
finish_labels = was_finished.Show_Name.sort_values().index
finish_counts = was_finished.Show_Name.sort_values()

#Create a pie chart to visualise the data
fig, ax6 = plt.subplots(figsize=(6,3), subplot_kw=dict(aspect="equal"))

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d})".format(pct, absolute)

wedges, texts, autotexts = ax6.pie(finish_counts, autopct=lambda pct: func(pct, finish_counts),
                                    textprops=dict(color='w'))

ax6.legend(wedges, finish_labels,
            title='True or False',
            loc='center left',
            bbox_to_anchor=(1, 0, 0.5, 1)) 

plt.setp(autotexts, size=8, weight="bold")

ax6.set_title("Did we finish the show?! by Number of Shows Watched")

plt.show()
