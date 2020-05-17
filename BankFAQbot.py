import pandas as pd
import numpy as np
import pickle
import operator
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.metrics.pairwise import cosine_similarity
import random
import nltk
from nltk.stem.lancaster import LancasterStemmer


stemmer = LancasterStemmer()
def cleanup(sentence):
    word_tok = nltk.word_tokenize(sentence)
    stemmed_words = [stemmer.stem(w) for w in word_tok]

    return ' '.join(stemmed_words)


le = LE()

tfv = TfidfVectorizer(min_df=1, stop_words='english')

data = pd.read_csv('BankFAQs.csv')
questions = data['Question'].values

X = []
for question in questions:
    X.append(cleanup(question))

tfv.fit(X)
le.fit(data['Class'])

X = tfv.transform(X)
y = le.transform(data['Class'])


trainx, testx, trainy, testy = tts(X, y, test_size=.25, random_state=42)

model = SVC(kernel='linear')
model.fit(trainx, trainy)
print("SVC:", model.score(testx, testy))


def get_max5(arr):
    ixarr = []
    for ix, el in enumerate(arr):
        ixarr.append((el, ix))
    ixarr.sort()

    ixs = []
    for i in ixarr[-5:]:
        ixs.append(i[1])

    return ixs[::-1]



def chat(msg):
    cnt = 0
    # print("PRESS Q to QUIT")
    # print("TYPE \"DEBUG\" to Display Debugging statements.")
    # print("TYPE \"STOP\" to Stop Debugging statements.")
    # print("TYPE \"TOP5\" to Display 5 most relevent results")
    # print("TYPE \"CONF\" to Display the most confident result")
    # print()
    # print()
    DEBUG = False
    TOP5 = False

    # print("Bot: Hi, Welcome to our bank!")
    #  while True:
    usr = msg

    result = []

    if usr.lower() == 'yes':
        print("81")
        result.append("Bot: Yes!")
        # return "Bot: Yes!"
        # continue

    if usr.lower() == 'no':
        print("87")
        result.append("Bot: No?")
        # return "Bot: No?"
        # continue

    if usr == 'DEBUG':
        DEBUG = True
        print("94")
        result.append("Bot: Debugging mode on")
        # return "Debugging mode on"
        # continue

    if usr == 'STOP':
        print("100")
        DEBUG = False
        result.append("Bot: Debugging mode off")
        # return "Debugging mode off"
        # continue

    if usr == 'Q':
        print("107")
        result.append("Bot: It was good to be of help.")
        # return "Bot: It was good to be of help."
        # break

    if usr == 'TOP5':
        TOP5 = True
        print("114")
        result.append("Will display 5 most relevent results now")
        # return "Will display 5 most relevent results now"
        # continue

    if usr == 'CONF':
        TOP5 = False
        print("121")
        result.append("Only the most relevent result will be displayed")
        # return "Only the most relevent result will be displayed"
        # continue

    t_usr = tfv.transform([cleanup(usr.strip().lower())])
    class_ = le.inverse_transform(model.predict(t_usr))
    questionset = data[data['Class']==class_[0]]

    if DEBUG:
        print("131, 132")
        result.append("Question classified under category : " + class_)
        result.append(str(len(questionset)) + " Questions belong to this class")

    cos_sims = []
    for question in questionset['Question']:
        sims = cosine_similarity(tfv.transform([question]), t_usr)
        cos_sims.append(sims)
            
    ind = cos_sims.index(max(cos_sims))

    if DEBUG:
        question = questionset["Question"][questionset.index[ind]]
        print("144")
        result.append("Assuming you asked: " + question)

    if not TOP5:
        print("148")
        result.append("Bot:" + data['Answer'][questionset.index[ind]])
    else:
        inds = get_max5(cos_sims)
        for ix in inds:
            print("153, 154")
            result.append("Question: "+data['Question'][questionset.index[ix]])
            result.append("Answer: " + data['Answer'][questionset.index[ix]])
            # result.append('-'*50)
    print(result)
    return result

    # print("\n"*2)
    # outcome = input("Was this answer helpful? Yes/No: ").lower().strip()
    # if outcome == 'yes':
    #     cnt = 0
    # elif outcome == 'no':
    #     inds = get_max5(cos_sims)
    #     sugg_choice = input("Bot: Do you want me to suggest you questions ? Yes/No: ").lower()
    #     if sugg_choice == 'yes':
    #         q_cnt = 1
    #         for ix in inds:
    #             print(q_cnt,"Question: "+data['Question'][questionset.index[ix]])
    #             # print("Answer: "+data['Answer'][questionset.index[ix]])
    #             print('-'*50)
    #             q_cnt += 1
    #         num = int(input("Please enter the question number you find most relevant: "))
    #         print("Bot: ", data['Answer'][questionset.index[inds[num-1]]])
