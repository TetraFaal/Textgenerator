import cherrypy
import os.path

media = os.path.join(os.path.abspath("."), u'GUI')

class HtmlText(object):

    def index(self):
        return open(os.path.join(media, u'HtmlTextgenerator.html'))
    index.exposed = True

    def start(self, textFromHtml=None, length=None):
        print(textFromHtml)
        return
    start.exposed = True

class AnalyseText(object):


configfile = os.path.join(os.path.dirname(__file__),'serv.conf')
cherrypy.quickstart(HtmlText(),config=configfile)