import math
import numpy as np
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential, load_model
from gensim.models.keyedvectors import KeyedVectors
import nltk

nltk.download("stopwords")
nltk.download("punkt")


def sent2word(x):
    stop_words = set(stopwords.words("english"))
    x = re.sub("[^A-Za-z]", " ", x)
    x.lower()
    filtered_sentence = []
    words = x.split()
    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence


def essay2word(essay):
    essay = essay.strip()
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    raw = tokenizer.tokenize(essay)
    final_words = []
    for i in raw:
        if len(i) > 0:
            final_words.append(sent2word(i))
    return final_words


def makeVec(words, model, num_features):
    vec = np.zeros((num_features,), dtype="float32")
    noOfWords = 0.0
    index2word_set = set(model.index_to_key)
    for i in words:
        if i in index2word_set:
            noOfWords += 1
            vec = np.add(vec, model[i])
    vec = np.divide(vec, noOfWords)
    return vec


def getVecs(essays, model, num_features):
    c = 0
    essay_vecs = np.zeros((len(essays), num_features), dtype="float32")
    for i in essays:
        essay_vecs[c] = makeVec(i, model, num_features)
        c += 1
    return essay_vecs


def get_model():
    model = Sequential()
    model.add(
        LSTM(
            300,
            dropout=0.4,
            recurrent_dropout=0.4,
            input_shape=[1, 300],
            return_sequences=True,
        )
    )
    model.add(LSTM(64, recurrent_dropout=0.4))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation="relu"))
    model.compile(loss="mean_squared_error", optimizer="rmsprop", metrics=["mae"])
    model.summary()
    return model


def predictMarks(text):
    content = text
    if len(content) > 20:
        num_features = 300
        model = KeyedVectors.load_word2vec_format(
            "../../Saved_Models/word2vecmodel.bin", binary=True
        )
        clean_test_essays = []
        clean_test_essays.append(sent2word(content))
        testDataVecs = getVecs(clean_test_essays, model, num_features)
        testDataVecs = np.array(testDataVecs)
        testDataVecs = np.reshape(
            testDataVecs, (testDataVecs.shape[0], 1, testDataVecs.shape[1])
        )

        lstm_model = load_model("../../Saved_Models/final_lstm.h5")
        preds = lstm_model.predict(testDataVecs)
        return str(math.floor(preds[0][0] * 10))


# essay = """ Dear The computer blinked to life and an image of a blonde haired girl filled the screen. It was easy to find out how life was in thanks to the actual girl explaining it. Going to the library wouldn't have filled one with this priceless information and human interection. Computers are a nessessity of life if soceity wishes to grow and expand. They should be supported because they teach hand eye coordination, give people the ability to learn about faraway places, and allow people to talk to others online. Firstly, computers help teach hand eye coordination. Hand-eye coordination is a useful ability that is usod to excel in sports. In a recent survey, of kids felt their hand eye coordination improves after computer use. Even a simple thing like tying can build up this skill. Famous neurologist stated in an article last week that, "@CAPS3 and computer strength the When on the computer, you automatically process what the eyes see into a command for your hands." hand eye coordination can improve people in sports such as baseball and basketball. If someone wan't to become better in these sports, all they'd need to do was turn on the computer. Once people become better at sports, they're more likely to play them and become more healthy. In reality, computers can help with exercising instead of decreasing it. Additionaly, computers allow people to access information about faraway places and people. If someone wanted to reasearch all they'd need to do was type in a search would be presented to them in it would link forever to search through countless things. Also, having the ability to learn about cultures can make peole peole and their cultures, they understand others something. Increase tolerance people are. Computers are a resourceful tool that they can help people in every different aspect of life. Lastly, computer and in technology can allow people to chat. Computer chat and video chat can help the all different nations. Bring on good terms places other than can help us understand story comes out about something that happend in people can just go on their computer and ask an actual citizen their take on the matter. Also, video chat and online conversation can cut down on expensive phone bills. No one wants to pay more than they have to in this economy. Another good point is that you can acess family members you scaresly visit. It can help you connect within your own family more. Oviously, computers are a useful aid in todays era. their advancements push the world foreward to a better place. Computers can help people because they help teach handeye coordination, give people the bility to learn about faraway places and people, and allow people to talk online with others. Think of a world with no computers or technologicall advancements. The world would be sectored and unified, contact between people scare, and information even. The internet is like thousands or librarys put together. Nobody would know much about other nations and news would travel slower. Is that the kind of palce you want people to live in? """

# score = predictMarks(essay)
# print('The score is ', score)
