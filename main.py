﻿#!/usr/bin/env python
import cgi
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from db import *
from messages import *


#end of DB class definitions
#
#
#classes for actions:


class CompanyHandler(webapp2.RequestHandler):
    def get(self):
        f = open("companyQueryFormPage\index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close()        

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
			self.response.write('Hello, ' + user.nickname())
			self.response.write('<div><a href="/chooseEmployOrStudentPage/index.html">login</a></div>')
			self.response.write('<br><br><div><a href="/studentInputPage/index.html">input page</a></div>')	
			self.response.write('<div><a href="/message">messages</a></div>')
			self.response.write('<div><a href="/companyQueryFormPage/index.html">search students</a></div>')				
		else:
			self.redirect(users.create_login_url(self.request.uri))


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        f = open("chooseEmployOrStudentPage/index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close() 

class MainHandler(webapp2.RequestHandler):
    def get(self):
        f = open('studentInputPage/index.html') 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close()        


class ResultsPage(webapp2.RequestHandler):
	def get(self):
		f = open("companyQueryResultsPage/index.html")		
		self.response.write(f.read())
		f.close()

#list of urls the user enters and functions that handle them
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/dbDelete', dbDelete),
	('/dbBuild', dbBuild),
	('/studentInputPage/index.html', MainHandler),
	('/chooseEmployOrStudentPage/index.html', LoginHandler),
	('/dbHandler', dbHandler),
	('/companyQueryFormPage/index.html', CompanyHandler),
	('/companyQueryResultsPage' , minGradeQuery),
	('/message', MessageHandler),
	('/messageSend', MessageSend),
	('/messageReply', MessageReply)	
	], debug=True)


	
