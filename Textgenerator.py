import cherrypy
import os.path
import random
from itertools import chain

media = os.path.join(os.path.abspath("."), u'GUI') #Chemin au documnets contenant les fichiers html

class TextGenerator:

    stateList = []

    def index(self):
        return open(os.path.join(media, u'HtmlTextgenerator.html')) #Html ouvert dans le navigateur
    index.exposed = True # ??? CherryPy

    def start(self, textFromHtml=None, length=None): #Fonction se lance après avoir cliquer sur Submit dans le navigateur
        analyzer = Analyze(textFromHtml) #Pour pouvoir utiliser dans l'autre class (objets)
        stateList = analyzer.getStructuredData()
        #self.printStateList(stateList) #Controle qui a foiré
        markov = MarkovGenerator()
        output = markov.generateSentence(stateList)
        print(output)
    start.exposed = True # ??? CherryPy

    def printStateList(self, list):
        for i in range(0, len(list)):
            print(list[i].value)

class MarkovGenerator:

    def generateSentence(self, list):

        output = ''
        currentState = None
        counter = 0

        for state in list:
            if state.value == 'SENTENCE_START':
                currentState = state
                break

        while currentState.value != 'SENTENCE_END' and counter <= 10:
            nextWord = random.choice(currentState.nextPossibilities)
            for state in list:
                if state.value == nextWord:
                    currentState = state
                    output += " " + currentState.value
                    counter += 1
                    break

        return output + '. '

class Analyze:

    textToAnalyze = '' #première definition de la variable textToAnalize

    def __init__(self, text): #initialise Analyze
        self.textToAnalyze = text #définit la variable textToAnalize comme égale à la variable text

    def getStructuredData(self): #Fonction qui sépare les phrases et ensuite les mots
        sentenceList = self.textToAnalyze.split('. ') #sépart les phrases du texte textToAnalize

        stateList = [] #State shit

        for sentence in sentenceList:
            wordList = ['SENTENCE_START']
            words = sentence.split(' ')
            wordList += words
            wordList.append('SENTENCE_END')

            for entry in wordList:
                if entry != 'SENTENCE_END' and entry != ' ':
                    existingState = next((state for state in stateList if state.value == entry), State(entry, []))

                    existingState.nextPossibilities.append(wordList[wordList.index(entry) + 1])

                    if existingState not in stateList:
                        stateList.append(existingState)

        return stateList

class State:

    value = ''
    nextPossibilities = []

    def __init__(self, v, n):
        self.value = v
        self.nextPossibilities = n


configfile = os.path.join(os.path.dirname(__file__),'serv.conf') #Lance le serveur
cherrypy.quickstart(TextGenerator(), config=configfile) #Lance cherrypy interface web