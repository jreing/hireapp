#!/usr/bin/env python
import cgi
import urllib
import datetime
from db import *

from google.appengine.api import users
from google.appengine.ext import ndb

#from google.appengine.api import oauth

import webapp2
logging.getLogger().setLevel(logging.INFO)

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
		#logging.info("enter token sign in")

		google_id=self.request.get('user_id')

		email=self.request.get('email')
		
		isStudent = self.request.get('isStudent')
		
		if (isStudent == 'true'):
			user_query = Student.query(Student.google_id==google_id).get()
			#if student is logging up for the first time
			if (user_query == None):
				s = []
				user_id=str(hashlib.sha512(google_id + str(time())).hexdigest())
				logging.info("writing student")
				logging.info(user_id)
				st= Student(email=email, student_courses=s,google_id=google_id, name="", city="",avg=-1, user_id=user_id)
				st.put()
			else:
				user_id=user_query.user_id

		elif(isStudent == 'false'):
			user_query = Company.query(Company.google_id==google_id).get()
			#if company is logging up for the first time
			if (user_query == None):
				user_id=str(hashlib.sha512(google_id + str(time())).hexdigest())
				logging.info("writing company")
				logging.info(user_id)
				cmp= Company(email=email, google_id=google_id, user_id=user_id, name="", city="")
				cmp.put()
			else:
				user_id=user_query.user_id
		#logging.info("writing cookie")
		#logging.info(user_id)
		self.response.set_cookie("id", user_id)
		
		
		
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
		f = open("index.html")
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
		self.response.write(f.read())
		f.close()

class StudentHandler(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		#logging.info("reading cookie")
		#logging.info(user_id)
		st = Student.query(Student.user_id==user_id).get()
		if (st==None):
			self.response.write ("""<html> an error has occured, please reload page""")
		elif (st.avg == -1):
			self.response.write ("""<html><script>
				window.location="/studentInputPage";
				</script></html>""")
		else:
			self.response.write ("""<html><script>
				window.location="/StudentOffersPage";
				</script></html>""")

class StudentEditHandler(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		student_query = Student.query(Student.user_id==user_id).get()
		logging.info(student_query.city)
		course_query = Course.query()
		page = buildStudentEditPage(student_query, course_query )
		self.response.write(page)



class Logout(webapp2.RequestHandler):
	def get(self):
		logging.info("SIGN OUT FUNC")
		user_id = self.request.cookies.get('id')
		self.response.delete_cookie("id")
		self.response.write("Logged out")
		import Cookie
		# On the production instance, we just remove the session cookie, because
		# redirecting users.create_logout_url(...) would log out of all Google
		# (e.g. Gmail, Google Calendar).
		#
		# It seems that AppEngine is setting the ACSID cookie for http:// ,
		# and the SACSID cookie for https:// . We just unset both below.
		cookie = Cookie.SimpleCookie()
		cookie['ACSID'] = ''
		cookie['ACSID']['expires'] = -86400  # In the past, a day ago.
		self.response.headers.add_header(*cookie.output().split(': ', 1))
		cookie = Cookie.SimpleCookie()
		cookie['SACSID'] = ''
		cookie['SACSID']['expires'] = -86400
		self.response.headers.add_header(*cookie.output().split(': ', 1))
		self.redirect("/") 



app = webapp2.WSGIApplication([
	('/dbDelete', dbDelete),
	('/dbUserIdScramble', dbUserIdScramble),
	('/dbBuild', dbBuild),
	('/studentInputPage', MainHandler),
	('/StudentWelcomePage/index.html', WelcomeHandler),	
	('/studenthandler', StudentHandler),
	('/tokenSignIn', tokenSignIn),
	('/StudentLogout', Logout),
	('/dbHandler', dbHandler),
	('/companyQueryFormPage', CompanyHandler),
	('/companyQueryResultsPage' , minGradeQuery),
	('/StudentOffersPage', MessageHandler),
	('/messageSend', MessageSend),
	('/messageReply', MessageReply),
	('/studentEditPage', StudentEditHandler),
	('/getMyCV', getMyCV),
	('/getCV', getCV),
	('/', LogInForBarak)
	], debug=True)


