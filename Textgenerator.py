import cherrypy
import os.path

media = os.path.join(os.path.abspath("."), u'GUI')

class HelloWorld(object):

    def index(self):
        return open(os.path.join(media, u'HtmlTextgenerator.html'))
    index.exposed = True

    def start(self, text=None, length=None):
        print(text)
        return
    start.exposed = True

class Markov(object):

    def getText(self):


configfile = os.path.join(os.path.dirname(__file__),'serv.conf')
cherrypy.quickstart(HelloWorld(),config=configfile)