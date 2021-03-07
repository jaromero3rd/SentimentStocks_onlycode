### installing praw: pip3 install praw
import praw
import copy
import time; time.time()
import pickle

def createCounter(mixUps):
    #---- gets the symbols on the stock exchange ----#
    #return counter = {" SYMB1 ": [0,0], "$SYMB1 ": [0,0]....}
    #return listOfSymb = [" SYMB1 ","$SYMB1 "," SYMB2 "...]
    FullList = open("SYMBOLS.txt","r")
    SymbAndNames = FullList.read().split("\n")
    ListOfSymb = []
    for entry in SymbAndNames:
        entrySplit = entry.split("\t")
        symbol1 = f"${entrySplit[0]} "
        symbol2 = f" {entrySplit[0]} "
        ListOfSymb.append(symbol1)
        ListOfSymb.append(symbol2)

    for entry in ListOfSymb:
        if entry in mixUps:
            ListOfSymb.remove(entry)

    #---- makes a counter for each symbol ----#
    counter = {}
    for names in ListOfSymb:
        counter[names] = [0,0]
    return counter, ListOfSymb

def countNew(subred, lim, ListOfSymb, counter, name):
    #We look at the first (lim) new posts we can find their titles#
    #return counter = {" SYMB1 ": [1,1002], "$SYMB1 ": [2,200]....}
    counterCopy = copy.deepcopy(counter)
    FullList = open(f"{name}_new.txt","a")
    for post in subred.new(limit = lim):
        for symb in ListOfSymb:
            if symb in post.title:
                upvotes = post.ups
                FullList.write(f"|{post.created}\t")
                FullList.write(f"{symb}\t{upvotes}\t")
                FullList.write(f"{post.title}|\n")
                post.comments.replace_more(limit=0)
                for top_level_comment in post.comments:
                    FullList.write(f"---\t({top_level_comment.body}) \n")
                counterCopy[symb][0] += 1
                counterCopy[symb][1] += upvotes

    return counterCopy

def countHot(subred, lim, ListOfSymb, counter, name):
    #We look at the first (lim) hot posts we can find their titles
    #return counter = {" SYMB1 ": [1,1002], "$SYMB1 ": [2,200]....}
    counterCopy = copy.deepcopy(counter)
    FullList = open(f"{name}_hot.txt","a")
    for post in subred.hot(limit = lim):
        for symb in ListOfSymb:
            if symb in post.title:
                upvotes = post.ups
                FullList.write(f"|{post.created}\t")
                FullList.write(f"{symb}\t{upvotes}\t")
                FullList.write(f"{post.title}|\n")
                post.comments.replace_more(limit=0)
                for top_level_comment in post.comments:
                    FullList.write(f"---\t({top_level_comment.body}) \n")
                counterCopy[symb][0] += 1
                counterCopy[symb][1] += upvotes
    return counterCopy

def filterTickerOne(counter, listOfSymbs):
    #---gives names of tickers that atleast have 1 mention---#
    #return counter = [[" SYMB1 ",1,1002], ["$SYMB1 ",2,200]....]
    fullTickers = {}
    for names in listOfSymbs:
        if counter[names][0] > 0:
            fullTickers[names] = counter[names]
    return fullTickers

def filterTickerTwo(fullTickers):
    #--- takes all the _GME_ and $GME_ and puts them into one if both exist ---#
    doubleMentions = {}

    for tickers in fullTickers:
        name = tickers.strip(" $")
        if name in doubleMentions:
            doubleMentions[name][0] += fullTickers[tickers][0]
            doubleMentions[name][1] += fullTickers[tickers][1]
        else:
            doubleMentions[name] = fullTickers[tickers]
    return doubleMentions

def merge(fullTickers1,fullTickers2):
    doubleMentions = copy.deepcopy(fullTickers1)

    for names in doubleMentions:
        if names in fullTickers2:
            doubleMentions[names][0] += fullTickers2[names][0]
            doubleMentions[names][1] += fullTickers2[names][1]
    
    for names in fullTickers2:
        if names not in doubleMentions:
            doubleMentions[names] = copy.deepcopy(fullTickers2[names])

    return doubleMentions

def findRelevantTickers(subred,lim,ListOfSymbs,emptyCounter,name):
    noSiftCounterNew = countNew(subred, lim, ListOfSymbs, emptyCounter,name)
    oneSiftCounterNew = filterTickerOne(noSiftCounterNew,ListOfSymbs)
    twoSiftCounterNew = filterTickerTwo(oneSiftCounterNew)

    noSiftCounterHot = countHot(subred, lim, ListOfSymbs, emptyCounter,name)
    oneSiftCounterHot = filterTickerOne(noSiftCounterHot,ListOfSymbs)
    twoSiftCounterHot = filterTickerTwo(oneSiftCounterHot)

    return twoSiftCounterNew, twoSiftCounterHot





""" For the future: create a new file app.py to control the flow of the 
    website and html and what not. Take the info we get here, send it to sql
    and then extract it later into several "posts" that show the number of times
    they have been mentioned. Also find when posts are and be able to time updates.
    I don't know how but it should be possible."""

def run(names):
    mixUp = [" A "," LOW "," FOR "," CEO "," INFO "," NEW "," VS "," DD "
                ," EV "," FLY "," LIVE "," IT "," BIG ", "GAIN"," BY "," AT "
                ," MAN ", " VERY ", " ALL ", " AM "," NEXT "," GAIN "," ON ","$ "
                ," C "]

    #---- gets us into the subreddit ----#
    reddit = praw.Reddit(
        client_id="nh6LZq8z0ppGKg",
        client_secret="duNyO775Jl-7rM-ZTN9dC22V_ZZzFg",
        user_agent="jaromero12345678910",
    )

    for name in names:
        lim = 1000
        stringyThing = f"{name}_red"
        stringyThing = reddit.subreddit(name)
        emptyCounter, ListOfSymbs = createCounter(mixUp)
        newStringyThing = f"new{name}"
        hotStringyThing = f"new{name}"
        newStringyThing, hotStringyThing = findRelevantTickers(stringyThing, 
                                            lim, ListOfSymbs, emptyCounter,name)
        print(f"The most mentioned on New {name}: \n{newStringyThing} \n")
        print(f"\nThe most mentioned on Hot {name}: \n{hotStringyThing} \n")

    return newStringyThing, hotStringyThing


nameOfReddits = ['wallstreetbets','stocks']

pickle.dump( run(nameOfReddits), open("tickersWithUpvotes.p","wb"))