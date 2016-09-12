import cherrypy
import os.path
from random import randint


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
        makrov = MakrovGenerator()
        print(makrov.generateSentence(stateList))
    start.exposed = True # ??? CherryPy

    def printStateList(self, list):
        for i in range(0, len(list)):
            print(list[i].value)

class MakrovGenerator:

    def generateSentence(self, list):

        output = ''
        counter = 1
        length = 5

        for i in range(0, length):
            tempList = []
            for entry in list:
                if(entry.index == counter):
                    tempList.append(entry)
            if(len(tempList) > 0):
                output += self.getRandomString(tempList) + " "
            counter += 1

        return output



    def getRandomString(self, l):
        rndNumber = randint(0, len(l))
        return l[rndNumber].value


class Analyze:

    text ='' #première definition de la variable text

    def __init__(self, text): #initialise Analyze
        self.text = text

    def getStructuredData(self): #Fonction qui sépare les phrases et ensuite les mots
        sentenceList = self.text.split('. ') #sépart les phrases
        wordList = []
        returnList = [] #State shit
        for i in range(0, len(sentenceList)):
            l = sentenceList[i].split(' ') #sépare les mots
            for entry in l:
                wordList.append(entry)
        for entry in wordList:
            for e in returnList:
                if(entry == e.value):
                    list = e.nextPossibilities
                    list.append(wordList[wordList.index(entry) + 1])
                    returnList[returnList.index(e)] = State(entry.value, list)
                else:
                    list = []
                    list.append(wordList[wordList.index(entry) + 1])
                    returnList.append(State(entry, list))

            if(len(returnList) == 0):
                list = []
                list.append(wordList[wordList.index(entry) + 1])
                returnList.append(State(entry, list))

        return returnList

class State:

    value =''
    nextPossibilities = []

    def __init__(self, v, n):
        self.value = v
        self.nextPossibilities = n


configfile = os.path.join(os.path.dirname(__file__),'serv.conf') #Lance le serveur
cherrypy.quickstart(TextGenerator(), config=configfile) #Lance cherrypy interface web