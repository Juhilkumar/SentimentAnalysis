from csv import DictWriter

import tweepy as tw
from pymongo import MongoClient

auth = tw.OAuthHandler("0C1hB0aVqax6OYRBl4P75TdPI", "keANh5Q6K6F10Ng9MWeSlNrk4NPiXXaFP2tkM8iGFoZYrQtWcJ")
auth.set_access_token("1358635825265741824-DQxcJCheNpfB4JhTsg3tI8ESL5JTFL",
                      "a8NJg5pRq7hUbZbuFIvlpemgVFUqzflwdEGuEH1VQUaCO")
api = tw.API(auth)

client = MongoClient("mongodb+srv://root:juhil7734@cluster0.hnmxh.mongodb.net/test")
db = client["cleaned"]
collection = db["Tweet_cleaned - 1"]

field_names = ['Cold Word Appearance in every Document', 'Total Words (m)', 'Frequency (f)']

searchKeywords = ['canada']
tweetList = collection.find()

articleNumber = 0
for tweet_row in tweetList:
    articleNumber += 1
    strFromDic = str(tweet_row)
    words = strFromDic.split()
    bow = {}
    bowCount = 0
    coldCount = 0
    for word in words:
        bowCount += 1
        word = word.lower()
        if word in bow:
            bow[word] = bow[word] + 1
        else:
            bow[word] = 1
    print(bow)

    for coldWord in bow:
        if coldWord == 'cold':
            coldCount = bow[coldWord]

    with open("./WordSementicAnalysis-b/semanticAnalysisB.csv", 'a') as csv_object:
        writerObject = DictWriter(csv_object, fieldnames=field_names)
        row1 = {'Cold Word Appearance in every Document': "Article #" + str(articleNumber),
                'Total Words (m)': str(bowCount),
                'Frequency (f)': str(coldCount)
                }

        writerObject.writerow(row1)



