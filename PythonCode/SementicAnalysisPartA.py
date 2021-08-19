import math
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

field_names = ['Search Query', 'Document containing term(df)',
               'Total Documents(N)/ number of documents term appeared(df)', 'Log10(N/df)']

searchKeywords = ['flu', 'snow', 'cold']
tweetList = collection.find()

fluCount = 1
snowCount = 1
coldCount = 1
for tweet_row in tweetList:
    strFromDic = str(tweet_row)
    words = strFromDic.split()
    bow = {}
    for word in words:
        word = word.lower()
        if word in bow:
            bow[word] = bow[word] + 1
        else:
            bow[word] = 1
    print(bow)

    for searchWord in bow:
        if searchWord == 'flu':
            fluCount += 1
        elif searchWord == 'snow':
            snowCount += 1
        elif searchWord == 'cold':
            coldCount += 1

with open("./WordSementicAnalysis/semanticAnalysis.csv", 'a') as csv_object:
    writerObject = DictWriter(csv_object, fieldnames=field_names)
    N = 500
    row1 = {'Search Query': str(searchKeywords[0]),
           'Document containing term(df)': str(fluCount),
           'Total Documents(N)/ number of documents term appeared(df)':  str(str(N) + "/" + str(fluCount)),
           'Log10(N/df)': str(math.log10(N / fluCount))}

    row2 = {'Search Query': str(searchKeywords[1]),
            'Document containing term(df)': str(snowCount),
            'Total Documents(N)/ number of documents term appeared(df)': str(str(N) + "/" + str(snowCount)),
            'Log10(N/df)': str(math.log10(N / snowCount))}


    row3 = {'Search Query': str(searchKeywords[2]),
            'Document containing term(df)': str(coldCount),
            'Total Documents(N)/ number of documents term appeared(df)': str(str(N) + "/" + str(coldCount)),
            'Log10(N/df)': str(math.log10(N / coldCount))}

    writerObject.writerow(row1)
    writerObject.writerow(row2)
    writerObject.writerow(row3)

