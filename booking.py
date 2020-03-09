#from bookingscrape import booking
from tripadvisorscrape import tripadvisor
from bookingscrape import booking
def mainfunc(location="carcabuey", datesin= "2020-05-26", datesout="2020-05-29"):
    #tic = time.perf_counter()
    notCorrect = True
    sites=["booking","tripadvisor","trivago"]
    option = "all"
#location = input("What location or hotel do you want \n")
#datesin = input("For what check in date eg. 2020-03-26 \n")
#datesout = input("For what check out date eg. 2020-03-29\n")
    location.capitalize().replace(" ", "_")
    while notCorrect:
        if (option in "booking"):
            print("Ok...")
            bookinggraph = booking(location, datesin, datesout)
            notCorrect=False
            pathname = "static/images/"+location+"booking"+".png"
            bookinggraph.savefig(pathname)
            return pathname.replace("static", "")
        elif (option in "tripadvisor"):
            tripadvisorgraph= tripadvisor(location, datesin, datesout)
            notCorrect=False
            pathname = "static/images/"+location+"tripadvisor"+".png"
            tripadvisorgraph.savefig(pathname)
            return pathname.replace("static", "")
        elif (option=="all"):
            print("Ok....")
            bookinggraph = booking(location, datesin, datesout)

            tripadvisorgraph = tripadvisor(location, datesin, datesout)
            bookingpathname = "static/images/"+location+"booking"+".png"
            bookinggraph.savefig(bookingpathname)
            tripadvisorpathname = "static/images/"+location+"tripadvisor"+".png"
            tripadvisorgraph.savefig(tripadvisorpathname)
            notCorrect = False
            return bookingpathname.replace("static", ""), tripadvisorpathname.replace("static", "")
        else:
            #option=input("Incorrect site name, try again: ")
            #toc = time.perf_counter()
            filler = True
    #print(f"Time taken for operation: {toc - tic:0.4f} seconds")
if __name__=='__main__':
    mainfunc()
