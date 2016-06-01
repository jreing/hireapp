# -*- coding: utf-8 -*-
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
class ValidateCompany(webapp2.RequestHandler):
	def post(self):
		id = self.request.cookies.get('id')
		logging.info(id)
		if (checkComapnyLoginExists(id)==True):
			self.response.write(id+"#accepted")
		else :
			self.response.write(errorPage("זמן החיבור פג"))

class ValidateStudent(webapp2.RequestHandler):
	def post(self):
		id = self.request.cookies.get('id')
		logging.info(id)
		if (checkStudentLoginExists(id)==True):
			self.response.write(id+"#accepted")
		else :
			self.response.write(errorPage("זמן החיבור פג"))
			
class CompanyHandler(webapp2.RequestHandler):
	def get(self):
		id = self.request.cookies.get('id')
		logging.info(id)
		if (Company.query(id==Company.user_id).get()==None):
			self.response.write(errorPage("session timeout"))
		else:
			course_query = Course.query()
			page = buildCompanyQuery(course_query)
			self.response.write(page)			

class tokenSignIn(webapp2.RequestHandler):
	def post(self):
		#logging.info("enter token sign in")
		
		google_id=self.request.get('user_id')

		email=self.request.get('email')
		#TODO: make isStudent server-side
		isStudent = self.request.get('isStudent')
		
		if (isStudent == 'true'):
			user_query = Student.query(Student.google_id==google_id).get()
			#if student is logging up for the first time
			if (user_query == None):
				s = []
				user_id=str(hashlib.sha512(google_id + str(time())).hexdigest())
				logging.info("writing student")
				logging.info(user_id)
				st= Student(allow_emails=False, email=email, student_courses=s,google_id=google_id, name="", city="",avg=-1, user_id=user_id, year=0, availability=0, git="", residence=0, needs_job=True)
				st.put()
			else:
				user_id=user_query.user_id

		elif(isStudent == 'false'):
			user_query = Company.query(Company.google_id==google_id).get()
			#if company is logging up for the first time
			if (user_query == None):
				#allow company user to be created only if the email
				#is on the allowedCompany list
				if allowedCompany.query(allowedCompany.email==email).get()!=None:
					user_id=str(hashlib.sha512(google_id + str(time())).hexdigest())
					logging.info("writing company")
					logging.info(user_id)
					cmp= Company(email=email, google_id=google_id, user_id=user_id, name="", city="")
					cmp.put()
				else:
					self.response.write(errorPage("אין כניסה, משתמש לא חוקי"))
					return
			else:
				user_id=user_query.user_id
		#logging.info("writing cookie")
		#logging.info(user_id)
		self.response.set_cookie("id", user_id)
	
	#use this function to add an AllowedCompany
	def addAllowedCompany(email):
		ac = allowedCompany(email=email)
		ac.put()
		
class StudentInputHandler(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		#logging.info("reading cookie")
		#logging.info(user_id)
		st = Student.query(Student.user_id==user_id).get()
		if (st==None):
			self.response.write (errorPage("גישה לא חוקית לדף"))
		else:
			course_query = Course.query()
			page = buildStudentInputPage(course_query)
			self.response.write(page)

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
		
class UnauthorizedPage(webapp2.RequestHandler):
	def get(self):
		f = open("unauthorized.html") 
		self.response.write(f.read())
		f.close()

class StudentHandler(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		#logging.info("reading cookie")
		#logging.info(user_id)
		st = Student.query(Student.user_id==user_id).get()
		if (st==None):
			self.response.write (errorPage("אירעה שגיאה, נא לטעון מחדש את האתר"))
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
		if (student_query==None): 
			self.response.write(errorPage("גישה לא חוקית לדף"))
		else:
			course_query = Course.query()
			page = buildStudentEditPage(student_query, course_query)
			self.response.write(page)

class companyAdHandler(webapp2.RequestHandler):
	def get(self):
		course_query = Course.query()
		page = buildAdPage(course_query )
		self.response.write(page)

class Logout(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		student_query = Student.query(Student.user_id==user_id).get()
		if (student_query==None): 
			self.response.write(errorPage("גישה לא חוקית לדף"))
		else:
			logging.info("SIGN OUT FUNC")
			self.response.delete_cookie("id")
			self.response.write("Logged out")
			import Cookie
			cookie = Cookie.SimpleCookie()
			cookie['ACSID'] = ''
			cookie['ACSID']['expires'] = -86400  # In the past, a day ago.
			self.response.headers.add_header(*cookie.output().split(': ', 1))
			cookie = Cookie.SimpleCookie()
			cookie['SACSID'] = ''
			cookie['SACSID']['expires'] = -86400
			self.response.headers.add_header(*cookie.output().split(': ', 1))
			self.redirect("/") 

class doubleLogin(webapp2.RequestHandler):
	def get(self):
		logging.info('LogInForBarak START')
		f = open("doublelogin.html")
		self.response.write(f.read())
		f.close()



app = webapp2.WSGIApplication([
	('/unauthorized', UnauthorizedPage),
	('/validateStudent', ValidateStudent),
	('/deleteStudent', deleteStudent),
	('/validateCompany', ValidateCompany),
	#('/dbDelete', dbDelete),
	('/dbUserIdScramble', dbUserIdScramble),
	#('/dbBuild', dbBuild),
	('/studentInputPage', StudentInputHandler),
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
	('/createAd', companyAdHandler),
	('/', LogInForBarak),
	#('/doubleLogin', doubleLogin)
	], debug=True)


