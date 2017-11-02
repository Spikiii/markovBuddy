# -*- coding: cp1252 -*-
import random
import os
import discord as ds
from discord.ext.commands import Bot

# Declarations
filepath = 'Markov Chain Documents\danielEssay.txt' #Default file
replacementText = "FILE NOT FOUND FILE NOT FOUND FILE NOT FOUND"
rawFile = []
cache = {}
words = []
startwords = []
boi = Bot(command_prefix = "!")

# Settings
leng = 100
randStart = False

#Opens the file specified by filepath
try:
    text = open(filepath, 'r')
except:
    text = replacementText

def getWords():
    #Adds everything to words
    global rawFile
    for i in text:
        rawFile.append(i.split())
    for i in rawFile:
        for j in i:
            words.append(j.lower())

def triples():
    """Creates Markov triples from words"""
    global words

    for i in range(len(words) - 2):
        yield(words[i], words[i + 1], words[i + 2])


def databaseTriples():
    """Adds the words to cache, to attempt to make keys"""
    global cache

    for a, b, c in triples():
        key = (a, b)
        if key in cache:
            cache[key].append(c)
        else:
            cache[key] = [c]

def getStartWords():
    """Gets all of the possible starting places"""
    global words

    startwords.append(words[0])
    for i in range(1, len(words)):
        prev_word = words[i - 1]
        if(prev_word[len(prev_word) - 1] == "."):
            startwords.append(words[i])

def genText(size):
    #print("genText")
    """Generates a chain of Markov triples"""
    global words
    if(not randStart):
        seed = random.randint(0, len(words) - 3)
        seed_word, next_word = words[seed], words[seed + 1]
        a, b = seed_word, next_word
    else:
        seed = random.randint(0, len(startwords) - 3)
        seed_word, next_word = startwords[seed], words[index(startwords[seed]) + 1]
        a, b = seed_word, next_word

    gen_words = []
    endPunc = [".", "!", "?", '."', ".'"]
    leng = 0
    while (not b[len(b) - 1] in endPunc or leng <= size):
        gen_words.append(a)
        try:
            a, b = b, random.choice(cache[(a, b)])
        except:
            a, b = b, cache[(a, b)][0]
        leng = len(gen_words)
    gen_words.append(b)
    for i in range(len(gen_words)):  # Makes the text look better
        if ("." in gen_words[i] and i < len(gen_words) - 1):
            gen_words[i + 1] = gen_words[i + 1][0].upper() + gen_words[i + 1][1:]
    gen_words[0] = gen_words[0][0].upper() + gen_words[0][1:]

    return " ".join(gen_words)

getWords()
#print("getWords")
getStartWords()
#print("getStartWords")
databaseTriples()
#print("triples")

@boi.event
async def on_read():
    print("Client logged in")

@boi.command()
async def markov(leng):
    """Generates a markov chain of length [leng]."""
    print("!markov " + leng)
    try:
        return await boi.say("From " + filepath[23:] + ", \n\n" + genText(int(leng)))
    except:
        return await boi.say("Either " + leng + " is not an integer, or it's too big... you dingus")

@boi.command()
async def list():
    """Lists all of the source files to switch to."""
    print("!list")
    return await boi.say(os.listdir("Markov Chain Documents"))

@boi.command()
async def changefile(file):
    """Changes the file to [file]. Use the full name, including the .txt"""
    print("!changefile " + file)
    global rawFile, cache, words, startwords, text, filepath
    try:
        filepath = os.path.normpath("Markov Chain Documents/" + file)
        text = open(filepath, 'r')

        rawFile = []
        cache = {}
        words = []
        startwords = []

        getWords()
        getStartWords()
        databaseTriples()
        return await boi.say("File changed to " + file)

    except:
        return await boi.say(file + " is not a file, you dingus")

print("Running")
boi.run("MzE0MTgzNDg2NjUzMzMzNTA0.C_0i_Q.EVXG24j8xRJ6g0Tjzut0n9PnDb8")