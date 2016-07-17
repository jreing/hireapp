#from oauth2client.client import flow_from_clientsecrets
#from google.appengine.api import oauth
#import logging
#import traceback

#handle login page
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        f = open("chooseEmployOrStudentPage/index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close() 


