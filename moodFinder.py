# Imports the Google Cloud client library
from google.cloud import language_v1
import os
import pickle
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/jennyromero/Desktop/code/STOCKS/moodFinder-2d03c34a57da.json"

# Instantiates a client
client = language_v1.LanguageServiceClient()

titles = []
tickers = []
time = []
upvotes = []
magnitude = []
sent = []

FullList = open("wallStreetBets_hot.txt","r")
entries = FullList.read().split("|")

remainder = 0
for i in range(len(entries)):
    if i%2 == remainder: 
        TUN = entries[i].split("\t")
        if len(TUN) == 4:
            time.append(TUN[0])
            tickers.append(TUN[1])
            upvotes.append(int(TUN[2]))
            titles.append(TUN[3])
        else:
            if remainder == 0:
                remainder = 1
            else:
                remainder = 0

for i in range(len(titles)):
    # The text to analyze
    text = titles[i]
    up = upvotes[i]

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    sc = sentiment.score
    mag = sentiment.magnitude

    sent.append(sc)
    magnitude.append(mag)

    print("Text: {}".format(text))
    print("Sentiment: {}, {}".format(sc, mag))

# titles = []
# tickers = []
# time = []
# upvotes = []
# magnitude = []
# sent = []

pickle.dump( titles , open( "titles.p", "wb" ) )
pickle.dump( tickers , open( "tickers.p", "wb" ) )
pickle.dump( time, open( "time.p", "wb" ) )
pickle.dump( upvotes, open( "upvotes.p", "wb" ) )
pickle.dump( magnitude, open( "magnitude.p", "wb" ) )
pickle.dump( sent, open( "sent.p", "wb" ) )
