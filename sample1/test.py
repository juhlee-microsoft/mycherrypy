import os, os.path
import random
import string

import cherrypy

@cherrypy.expose
class StringGeneratorWebService(object):
    
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']
    
    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string
    
    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string
        
    def DELETE(self):
        cherrypy.session.pop('mystring', None)

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
            <head>
                <link href="/static/css/style.css" rel="stylesheet">            
            </head>
            <body>
                <form method="get" action="generate">
                    <input type="text" value="8" name="length" />
                    <button type="submit">Give it now!</button>
                </form>
            </body>
        </html>"""
    
    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string
    
    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']
    
if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plan')],
#             'tools.staticdir.root': os.path.abspath(os.getcwd())
#             },
#         '/static': {
#             'tools.staticdir.on': True,
#             'tools.staticdir.dir': '.public'
            }
        }
    cherrypy.quickstart(StringGeneratorWebService(),'/', conf)
    