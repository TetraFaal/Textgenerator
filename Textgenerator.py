import cherrypy
import os.path

media = os.path.join(os.path.abspath("."), u'GUI')

class HtmlText:

    def index(self):
        return open(os.path.join(media, u'HtmlTextgenerator.html'))
    index.exposed = True

    def start(self, textFromHtml=None, length=None):
        analyzer = Analyze(textFromHtml)
        analyzer.analyze()
    start.exposed = True

class Analyze:

    text =''

    def __init__(self, text):
        self.text = text

    def analyze(self):
        sentenceList = self.text.split('. ')
        wordList = []
        for i in range(0, len(sentenceList)):
            print("Sentence " + str(i) + ": " + sentenceList[i])
            l = sentenceList[i].split(' ')
            print(l)
            wordList.append(l)

class State:

    index = 0
    value =''
    nextPossibilities = []

    def __init__(self, i, v, n):
        self.index = i
        self.value = v
        self.nextPossibilities = n


configfile = os.path.join(os.path.dirname(__file__),'serv.conf')
cherrypy.quickstart(HtmlText(),config=configfile)