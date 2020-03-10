import os
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


#prints full list from dataframe 
def printlist(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None,
                           'display.max_colwidth', -1):
        print(df)
    # hotellist.to_csv(csvfile)





#compares an input string to the list of hotel names to find the closest match
def fuzzy_merge(df1, closestmatch):
    pd.options.mode.chained_assignment = None
    largest = 0
    hotelnamelist = df1['Hotel name'].tolist()
    newmatch = None
    for name in hotelnamelist:
        if  fuzz.partial_ratio(name.lower(), closestmatch.lower())> largest and fuzz.partial_ratio(name.lower(), closestmatch.lower())> 90:
            largest = fuzz.partial_ratio(name.lower(), closestmatch.lower())
            newmatch = name
    resultindex = df1.loc[df1['Hotel name']==newmatch].index.values[0]
    return newmatch, resultindex



#uses dataframe to create price vs rating plot with a labelled point given an index
def plotvalsites(df, comb, figcount, closestmatch):
    plt.figure()
    y = "y"
    # label = input("Label points y/n \n")
    label = "n"
    # bestfit = input("Best fit line y/n \n")
    bestfit = y
    # highlight = input("Enter rank to highlight specific hotel \n")
    highlight = 2
    pt = df.pivot_table(index='Hotel name', values=['Rating', 'Price'], aggfunc='mean')

    fig, ax = plt.subplots()
    #Creates plot with axis price and rating, and bestfit line
    if bestfit == y:
        sns.regplot(df['Price'], df['Rating'])
    else:
        df.plot('Price', 'Rating', kind='scatter', ax=ax)
    # annotates points with hotel name, disabled by default
    if label == y:
        for k, v in pt.iterrows():
            ax.annotate(k, v)
    rank = ""
    try:
        #takes in an index and highlights the given index
        index, rank =  fuzzy_merge(df, closestmatch)
        search = pt.loc[[index], ['Price', 'Rating']]
        hotelname = index #search.iloc[0]['Hotel name']
        price = search.iloc[0]['Price']
        rating = search.iloc[0]['Rating']
        plt.plot(price, rating, 'ro')
        for i, row in search.iterrows():
            ax.annotate(i, row, xytext=(price + 1, rating + 1), arrowprops=dict(facecolor='black', shrink=0.05))
    except Exception as e:
        print(e)
        pass
    axes = plt.gca()
    axes.set_ylim([None, 10.5])
    pathname = 'static/images/' + comb + '.png'
    fig.savefig(pathname)
    return fig


#Creates a plot with cities, hotels, price and rating
#def plotvalcities(csv):
#    label = input("Label points y/n \n")
#    bestfit = input("Best fit line y/n \n")
#    highlight = input("Highlight point of interest point y/n \n")
#    y = "y"
#    pt = df.pivot_table(index='City', values=['Rating', 'Price'], aggfunc='mean').sort_values('Price')
#    rmdups = df.City.drop_duplicates('first')
#    fig, ax = plt.subplots()
#    if bestfit == y:
#        sns.regplot(pt['Price'], pt['Rating'])
#    else:
#        pt.plot('Price', 'Rating', kind='scatter', ax=ax)
#    if label == y:
#        for k, v in pt.iterrows():
#            ax.annotate(k, v)
#    if highlight.capitalize() in df['City'].tolist():
#        search = pt.loc[highlight.capitalize()]
#        plt.plot(search.values[0], search.values[1], 'ro')
#        ax.annotate(highlight.capitalize(), search, xytext=(3, 4), arrowprops=dict(facecolor='black', shrink=0.05))
#    plt.show()


#Compares hotelnames from both sites and does fuzzy merge to try and find nearest match for hotel name
def comparesites(*args):
    dfull = pd.DataFrame()
    for csv in args:
        if 'tripadvisor' in csv:
            name = 'tripadvisor'
        if 'booking' in csv:
            name = 'booking'
        df = pd.read_csv(csv)
        site = pd.Series([name] * len(df))
        df['Site'] = site
        dfull = dfull.append(df)
    dfull['Rank'] = dfull.index
    dfull.set_index('Site', inplace=True)
    # printlist(dfull)
    tripadvisor = dfull.loc['tripadvisor']
    booking = dfull.loc['booking']
    fuzzy_merge(booking, tripadvisor)

#creates png file from a csv, takes in a site name a site name and city name and a figure count used to create seperate plots
def initialize(csvfile, comb, figcount, closestmatch):
    # Read the .csv file to create a dataframe
    df = pd.read_csv(csvfile)
    soldout = {'Price': 'Sold out'}
    df2 = df.fillna(value=soldout)
    df = df.dropna()
    df2 = df2.dropna()
    dfsoldout = df2.loc[df2['Price'] == 'Sold out']
    print(dfsoldout)
    df.index.name = "Rank"
    df.drop_duplicates(['Hotel name'], 'first', inplace=True)
    fig = plotvalsites(df, comb, figcount, closestmatch)
    return fig


if __name__ == '__main__':
    initialize('csvfiles/carcabueytripadvisor.csv', "tripadvisor", "carcabueytripadvisor", 1)
    initialize('csvfiles/carcabueybooking.csv', "booking", "carcabueybooking", 2)
