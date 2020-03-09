import os

import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# Prints entire dataframe
def printlist(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None,
                           'display.max_colwidth', -1):
        print(df)
    # hotellist.to_csv(csvfile)


# def duplicates(df):
# sample = df.sample(10000, random_state= 100).sort_index(axis=0)
# df.sort_values('Price', ascending=False , inplace = True, na_position='last' )
# print("shape of data {}".format(df.shape))
# df.drop_duplicates(['City','Hotel name'], 'first', inplace=True)
# df['duplicate']= df.duplicated(['Hotel name', 'Price', 'Rating'], False)
# duplicate = df[df['duplicate']== True].sort_values('Hotel name')
# df.dropna(inplace=True)

def plotvalsites(df, comb, figcount):
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
    if bestfit == y:
        sns.regplot(df['Price'], df['Rating'])
    else:
        df.plot('Price', 'Rating', kind='scatter', ax=ax)
    if label == y:
        # Creates plot with labels of hotels
        for k, v in pt.iterrows():
            ax.annotate(k, v)
    try:
        if len(df) > int(highlight) >= 0:
            search = df.iloc[[highlight]]
            hotelname = search.iloc[0]['Hotel name']
            price = search.iloc[0]['Price']
            rating = search.iloc[0]['Rating']
            search.set_index('Hotel name', inplace=True)
            plt.plot(price, rating, 'ro')
            for i, row in search.iterrows():
                ax.annotate(i, row, xytext=(price + 1, rating + 1), arrowprops=dict(facecolor='black', shrink=0.05))
    except:
        pass
    axes = plt.gca()
    axes.set_ylim([None, 10.5])
    pathname = 'static/images/' + comb + '.png'
    fig.savefig(pathname)
    return fig


def plotvalcities(csv):
    label = input("Label points y/n \n")
    bestfit = input("Best fit line y/n \n")
    highlight = input("Highlight point of interest point y/n \n")
    y = "y"
    # Creates dataframe with the parameters, calculates mean price, rating per city
    pt = df.pivot_table(index='City', values=['Rating', 'Price'], aggfunc='mean').sort_values('Price')
    rmdups = df.City.drop_duplicates('first')
    fig, ax = plt.subplots()
    if bestfit == y:
        sns.regplot(pt['Price'], pt['Rating'])
    else:
        pt.plot('Price', 'Rating', kind='scatter', ax=ax)
    if label == y:
        # Creates plot with labels of cities
        for k, v in pt.iterrows():
            ax.annotate(k, v)
    if highlight.capitalize() in df['City'].tolist():
        search = pt.loc[highlight.capitalize()]
        plt.plot(search.values[0], search.values[1], 'ro')
        ax.annotate(highlight.capitalize(), search, xytext=(3, 4), arrowprops=dict(facecolor='black', shrink=0.05))
    plt.show()


def comparefun(hotel_name, largest, closestmatch):
    if fuzz.ratio(hotel_name.lower(), closestmatch.lower()) > largest:
        largest = fuzz.ratio(hotel_name.lower(), closestmatch.lower())
    return largest



def fuzzy_merge(df1, closestmatch):
    pd.options.mode.chained_assignment = None
    # list1 = [s.replace("Fuengirola", "") for s in list1]
    # list1 = [s.replace("Hotel", "") for s in list1]
    # list1 = [s.replace("Hostal", "") for s in list1]
    printlist(df1['Hotel name'])
    largest = 0
    valuelist = df1['Hotel name'].apply(lambda x: comparefun(x, largest, closestmatch))
    print(valuelist)
    matchlist = df1.index[df1['Hotel name']].tolist()
    return matchlist[0]


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


# csv1 = 'hotellistfuengirolatripadvisor.csv'
# csv2 = 'hotellistfuengirolabooking.csv'
# comparesites(csv1, csv2)
def initialize(csvfile, site, comb, figcount):
    # Read the .csv file to create a dataframe
    df = pd.read_csv(csvfile)
    df = df.dropna()
    df.reset_index(drop=True, inplace=True)
    df.index.name = "rank"
    df.drop_duplicates(['Hotel name'], 'first', inplace=True)
    # Create bool list with dups
    # duplicate = hotellist.duplicated()
    # Create new column with dup bools
    # hotellist['duplicate'] = duplicate
    # Find and print max val in price column
    # max_value = hotellist['Price'].idxmax()
    # print(hotellist.loc[max_value,:])
    # sort dataframe by price and prints it
    # hotellist.sort_values('Rating', inplace=True, ignore_index=True)

    # print(df.describe())
    # out = input("Do you want to print results for {} y/n \n".format(site))
    # if out == "y":
    #    printlist(df)
    # plot = input("Do you want to plot results for {} y/n \n".format(site))
    if "y" == "y":
        fig = plotvalsites(df, comb, figcount)
    return fig


def loopthrough():
    dfull = pd.DataFrame()
    for filename in os.listdir("/home/juan/Documents/python/cities2/"):
        df = pd.read_csv('/home/juan/Documents/python/cities2/{0}'.format(filename))
        name = filename.replace("hotellist", "").replace(".csv", "")
        citylist = pd.Series([name] * len(df))
        df.insert(0, "City", citylist)
        dfull = dfull.append(df, ignore_index=True)
    dfull.to_csv("fullcities.csv")
    return dfull


if __name__ == '__main__':
    initialize('csvfiles/carcabueytripadvisor.csv', "tripadvisor", "carcabueytripadvisor", 1)
    initialize('csvfiles/carcabueybooking.csv', "booking", "carcabueybooking", 2)
