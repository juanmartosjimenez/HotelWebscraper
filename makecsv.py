import csv
from processhotellist import initialize


def createcsv(hotellist, location, site, figcount):
    comb = location + site
    with open('csvfiles/%s.csv' % comb, 'w') as result:
        print(hotellist)
        writer = csv.writer(result)
        writer.writerow(('Hotel name', 'Price', 'Rating'))
        writer.writerows(hotellist)
    fig = initialize('csvfiles/%s.csv' % comb, site, comb, figcount)
    return fig


def comparefiles(location):
    out = input("do you want to compare different sites y/n \n")
    graph = input("do you want to graph the values y/n \n")
