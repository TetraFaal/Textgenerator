import cherrypy
import os.path
import random

media = os.path.join(os.path.abspath("."), u'GUI') #Chemin au documnets contenant les fichiers html

class TextGenerator:

    stateList = []
    number = 30

    def index(self):
        return open(os.path.join(media, u'HtmlTextgenerator.html')) #Html ouvert dans le navigateur
    index.exposed = True # ??? CherryPy

    def start(self, textFromHtml=None, length=None): #Fonction se lance après avoir cliquer sur Submit dans le navigateur
        analyzer = Analyze(textFromHtml) #Pour pouvoir utiliser dans l'autre class (objets)
        stateList = analyzer.getStructuredData()
        markov = MarkovGenerator()
        finalText = []
        for i in range (0, self.number):
            output = markov.generateSentence(stateList)
            print(output)
            finalText.append(output)
        return finalText
    start.exposed = True # ??? CherryPy


class MarkovGenerator:

    def generateSentence(self, list):

        output = ''
        currentState = None
        counter = 0

        values =[]

        for state in list:
            if state.value == 'SENTENCE_START':
                currentState = state
                break

        nextWord = ''
        while nextWord != 'SENTENCE_END' and counter <= random.randint(10,20):
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
        sentenceList = [w.replace('."', '. ') for w in sentenceList]
        sentenceList = [w.replace('"', '') for w in sentenceList]
        sentenceList = [w.replace(',. ', '. ') for w in sentenceList]
        sentenceList = [w.replace(':. ', ': ') for w in sentenceList]
        stateList = [] #State shit

        for sentence in sentenceList:
            wordList = ['SENTENCE_START']
            words = sentence.split(' ')
            wordList += words
            wordList.append('SENTENCE_END')

            for entry in wordList:
                if entry != 'SENTENCE_END' and entry != ' ':
                    existingState = next((state for state in stateList if state.value == entry), State(entry, []))
                    possibilityToAdd = wordList[wordList.index(entry) + 1]
                    if possibilityToAdd != ' ':
                        existingState.nextPossibilities.append(possibilityToAdd)

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