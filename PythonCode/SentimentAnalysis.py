import re
import sys
import tweepy as tw
from csv import DictWriter
from tweepy import StreamListener

auth = tw.OAuthHandler("0C1hB0aVqax6OYRBl4P75TdPI", "keANh5Q6K6F10Ng9MWeSlNrk4NPiXXaFP2tkM8iGFoZYrQtWcJ")
auth.set_access_token("1358635825265741824-DQxcJCheNpfB4JhTsg3tI8ESL5JTFL",
                      "a8NJg5pRq7hUbZbuFIvlpemgVFUqzflwdEGuEH1VQUaCO")
api = tw.API(auth)

WORDS = ["cold", "flu", "snow"]

positiveWordsFile = open("./WordsForSentimentalAnalysis/positive.txt")
positiveWords = []
for word in positiveWordsFile:
    word = word.replace('\n', '')
    positiveWords.append(word)
print(positiveWords)

negativeWordsFile = open("./WordsForSentimentalAnalysis/negative.txt")
negativeWords = []
for word in negativeWordsFile:
    word = word.replace('\n', '')
    negativeWords.append(word)
print(negativeWords)

field_names = ['TWEET', 'MESSAGE', 'MATCH', 'POLARITY']

def clean_data(txt):
    try:
        txt = " ".join(
            re.sub(
                "([\U0001F1E0-\U0001F1FF]) | ([\U0001F300-\U0001F5FF]) |([\U0001F600-\U0001F64F]) |([\U0001F300-\U0001F5FF]) |([^a-zA-Z0-9]+)|(\w+:\/\/\S+)|([RT]+)",
                " ",
                txt).split())
    except:
        pass
    return txt


class StreamListener(tw.StreamListener):
    count = 0
    tweetRow = 0

    def on_status(self, status):
        StreamListener.count += 1
        StreamListener.tweetRow += 1
        bow = {}
        text = clean_data(status.text)
        words = text.split()

        for word in words:
            word = word.lower()
            if word in bow:
                bow[word] = bow[word] + 1
            else:
                bow[word] = 1

        match = []
        pCount = 0
        for pWord in positiveWords:
            if pWord in bow:
                pCount += 1
                match.append(pWord)

        nCount = 0
        for nWord in negativeWords:
            if nWord in bow:
                nCount += 1
                match.append(nWord)

        polarity = ""
        if (pCount<nCount) :
            polarity = "Negative"
        elif (pCount > nCount) :
            polarity = "Positive"
        else:
            polarity = "Neutral"

        with open("./WordsForSentimentalAnalysis/sentimentalAnalysis.csv", 'a') as csv_object:
            writerObject = DictWriter(csv_object, fieldnames=field_names)

            row = {'TWEET': StreamListener.tweetRow, 'MESSAGE': str(text), 'MATCH': match, 'POLARITY': str(polarity)}
            writerObject.writerow(row)
            print("Tweet" + str(StreamListener.count) + " :" + str(text))
            print("bag_of_words" + str(bow))

        if StreamListener.count == 4000:
            sys.exit()

    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tw.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=WORDS)
