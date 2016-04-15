#!/usr/bin/env python
import cgi
import urllib
import datetime
import logging

from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client, crypt

import webapp2
logging.getLogger().setLevel(logging.INFO)
logging.warning("CHECK")
from db import *
from messages import *


#end of DB class definitions
#
#
#classes for actions:


class CompanyHandler(webapp2.RequestHandler):
	def get(self):
		cours_query = Course.query()
		page = buildCompanyQuery(cours_query)
		self.response.write(page)
		#f = open("companyQueryFormPage\index.html") 
		#self.response.charset="unicode"
		#self.response.write(f.read())
		#f.close()               

class tokenSignIn(webapp2.RequestHandler):
	def post(self):
		userid=self.request.get('user_id')
		email=self.request.get('email')
		user_query = Student.query(Student.id==userid).get()
		if (user_query == None):
			s = []
			st= Student(student_courses=s,id=userid, name="", city="",avg=-1)
			st.put()
			self.response.write('<html><br><br>userId: ' + userid)
		self.response.set_cookie("id", userid)

	
class LoginHandler(webapp2.RequestHandler):
	def get(self):
		f = open("chooseEmployOrStudentPage/index.html") 
		logging.info("LOGIN HANDLER")
		self.response.write(f.read())
		f.close() 

class MainHandler(webapp2.RequestHandler):
	def get(self):
		cours_query = Course.query()
		page = buildStudentInputPage(cours_query)
		self.response.write(page)
		#f = open("studentInputPage/index.html") 
	#self.response.charset="unicode"
	#self.response.write(f.read())
	#f.close()        

class ResultsPage(webapp2.RequestHandler):
	def get(self):
		f = open("companyQueryResultsPage/index.html")		
		self.response.write(f.read())
		f.close()
		
class LogInForBarak(webapp2.RequestHandler):
	def get(self):
		logging.info('LogInForBarak START')
		f = open("LogInForBarak/index.html")		
		self.response.write(f.read())
		f.close()

class FirstPage(webapp2.RequestHandler):
	def get(self):
		self.response.write ("""<html><script>
			window.location="chooseEmployOrStudentPage/index.html";
			</script></html>""")

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		f = open("StudentWelcomePage/index.html") 
		#self.response.charset="unicode"
		self.response.write(f.read())
		f.close()

class StudentHandler(webapp2.RequestHandler):
	def get(self):
		userid = self.request.cookies.get('id')
		st = Student.query(Student.id==userid).get()
		if (st.avg == -1):
			self.response.write ("""<html><script>
				window.location="/studentInputPage";
				</script></html>""")
		else:
			self.response.write ("""<html><script>
				window.location="/StudentOffersPage";
				</script></html>""")

				
app = webapp2.WSGIApplication([
	('/dbDelete', dbDelete),
	('/dbBuild', dbBuild),
	('/studentInputPage', MainHandler),
	('/StudentWelcomePage/index.html', WelcomeHandler),	
	('/studenthandler', StudentHandler),
	('/tokenSignIn', tokenSignIn),
	('/chooseEmployOrStudentPage/index.html', LoginHandler),
	('/dbHandler', dbHandler),
	('/companyQueryFormPage', CompanyHandler),
	('/companyQueryResultsPage' , minGradeQuery),
	('/StudentOffersPage', MessageHandler),
	('/messageSend', MessageSend),
	('/messageReply', MessageReply),
	('/', LogInForBarak)
	], debug=True)


