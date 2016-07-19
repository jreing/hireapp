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

#classes for actions:
class ValidateCompany(webapp2.RequestHandler):
	#this class validates that a request was sent from a valid logged in company
	def post(self):
		id = self.request.cookies.get('id')
		logging.info(id)
		if (checkCompanyLoginExists(id)==True):
			self.response.write(id+"#accepted")
		else :
			self.response.write(errorPage("זמן החיבור פג"))

class ValidateStudent(webapp2.RequestHandler):
	#this class validates that a request was sent from a valid logged in student
	def post(self):
		id = self.request.cookies.get('id')
		logging.info(id)
		if (checkStudentLoginExists(id)==True):
			logging.info ("accepted")
			self.response.write(id+"#accepted")
			
		else :
			self.response.write(errorPage("זמן החיבור פג"))
			

class tokenSignIn(webapp2.RequestHandler):
	#this class performs the server-side user login
	
	
	def post(self):
		#logging.info("enter token sign in")
		
		google_id=self.request.get('user_id')

		email=self.request.get('email')
		
		#server side check if it's a student or a company mail
		isStudent=email.endswith("tau.ac.il")
		
		#isStudent = self.request.get('isStudent')
		
		if (isStudent == True):
			user_query = Student.query(Student.google_id==google_id).get()
			#if student is logging up for the first time
			if (user_query == None):
				s = []
				user_id=str(hashlib.sha512(google_id + str(time())).hexdigest())
				logging.info("writing student")
				logging.info(user_id)
				st= Student(cnt=0, allow_emails=False, email=email, student_courses=s,google_id=google_id, name="", city="",avg=-1, user_id=user_id, year=0, availability=0, git="", residence=0, needs_job=True,gradesheet_view_cnt=0,cv_view_cnt=0)
				st.put()
				user_query=st
				
		elif(isStudent == False):
			user_query = Company.query(Company.google_id==google_id).get()
			#if company is logging up for the first time
			if (user_query == None):
				#allow company user to be created only if the email
				#is on the allowedCompany list
				if (allowedCompany.query(allowedCompany.email==email).get()!=None):
					user_id=str(hashlib.sha512(google_id + str(time())).hexdigest())
					logging.info("writing company")
					logging.info(user_id)
					cmp= Company(cnt=0, email=email, google_id=google_id, user_id=user_id, name="", city="")
					cmp.put()
					t.sleep(1)
					user_query = Company.query(Company.google_id==google_id).get()
				else:
					self.response.write(errorPage("אין כניסה, משתמש לא חוקי"))
					return
				
				
		#logging.info("writing cookie")
		#logging.info(user_id)
		user_id=user_query.user_id
		
		#increment counter of visits
		user_query.cnt=user_query.cnt + 1
		user_query.put()
		
		self.response.set_cookie("id", user_id)
	
	#use this function to add an AllowedCompany
	def addAllowedCompany(email):
		ac = allowedCompany(email=email)
		ac.put()


###Page loading handlers
		
class CompanyHandler(webapp2.RequestHandler):
	def get(self):
		id = self.request.cookies.get('id')
		logging.info(id)
		if (Company.query(id==Company.user_id).get()==None):
			self.response.write(errorPage("זמן החיבור פג"))
		else:
			course_query = Course.query()
			page = buildCompanyQuery(course_query)
			self.response.write(page)		
		
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

#class ResultsPage(webapp2.RequestHandler):
#	def get(self):
#		f = open("companyQueryResultsPage/index.html")
#		self.response.write(f.read())
#		f.close()
				
class HelpHandler(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		isCompany=False
		isStudent=False
		if (user_id==None):
			isStudent=True
			isCompany=True
		elif (Student.query(Student.user_id==user_id).get()!=None):
			isStudent=True
		elif (Company.query(user_id==Company.user_id).get()!=None):
			isCompany=True
		logging.info(user_id)
		self.response.write(buildHelpPage(isStudent,isCompany))
		#f = open('helpPage.html')
		#self.response.write(f.read())
		#f.close()
		
class LogInForBarak(webapp2.RequestHandler):
	def get(self):
		logging.info('LogInForBarak START')
		f = open("index.html")
		self.response.write(f.read())
		f.close()

#class FirstPage(webapp2.RequestHandler):
#	def get(self):
#		self.response.write ("""<html><script>
#			window.location="chooseEmployOrStudentPage/index.html";
#			</script></html>""")

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
		logging.info("id: " + str(user_id))
		student_query = Student.query(Student.user_id==user_id).get()
		if (student_query==None): 
			self.response.write(errorPage("גישה לא חוקית לדף"))
		else:
			course_query = Course.query()
			page = buildStudentEditPage(student_query, course_query)
			self.response.write(page)
			
class companyAdHandler(webapp2.RequestHandler):
	def get(self):
		id = self.request.cookies.get('id')
		logging.info(id)
		if (Company.query(id==Company.user_id).get()==None):
			self.response.write(errorPage("זמן החיבור פג"))
		else:
			course_query = Course.query()
			page = buildAdPage(course_query)
			self.response.write(page)

class companyAdRemover(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		if (Company.query(user_id==Company.user_id).get()==None):
			self.response.write(errorPage("זמן החיבור פג"))
		else:
			ad_id = self.request.get('ad_id')
			
			comp = Company.query(Company.user_id == user_id).get()
			email = comp.email
			ad_query = Ad.query(Ad.message.compMail == email).order(Ad.message.date).fetch()
			
			#ad_query = Ad.query(Ad.user_id ==user_id).fetch()
			
			if (int(ad_id)<0 or int(ad_id)>=len(ad_query)):
				self.redirect("/currentAds")
				return
				
			ad_query[int(ad_id)].key.delete()
			#ad_query.put()
			t.sleep(1)
			self.redirect("/currentAds")
			
			
class companyCurrAdHandler(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		if (Company.query(user_id==Company.user_id).get()==None):
			self.response.write(errorPage("זמן החיבור פג"))
		else:
			comp = Company.query(Company.user_id == user_id).get()
			email = comp.email
			
			#ad_query = Ad.query(Ad.user_id ==user_id )
			ad_query = Ad.query(Ad.message.compMail == email).order(Ad.message.date).fetch()
			page = buildCurrentAdsPage(ad_query)
			self.response.write(page)
		
class companyEditAdHandler(webapp2.RequestHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		if (Company.query(user_id==Company.user_id).get()==None):
			self.response.write(errorPage("זמן החיבור פג"))
		else:
			ad_id = self.request.get('ad_id')
			comp = Company.query(Company.user_id == user_id).get()
			email = comp.email
			ad_query = Ad.query(Ad.message.compMail == email).order(Ad.message.date).fetch()
			#ad_query = Ad.query(Ad.user_id ==user_id).fetch()
			logging.info("list len " + str(len(ad_query)) + " " + ad_id)
			
			if (int(ad_id)<0 or int(ad_id)>=len(ad_query)):
				self.redirect("/currentAds")
				return
				
			course_query = Course.query() 
			page = EditAdPage(course_query,ad_query[int(ad_id)],ad_id)
			self.response.write(page)

class companyAdResultsHandler(webapp2.RequestHandler):
	
	def fetchQuery(self,adv):
		course_query = Course.query()
		
		# making adjusments between the ad parameters and query parameters
		course_names = []
		course_grades = []	
		for crs in adv.aQuery.student_courses:
			course_names.append(crs.course.course_name)
			course_grades.append(str(crs.grade))
		ctypesBack = list(adv.aQuery.ctypes)
		
		#creating a mingrafequery object that is used by the getQuery function as 'self'
		minGradeQ = db.minGradeQuery()
		q = getQuery(minGradeQ,course_names,course_grades,str(adv.aQuery.avg)
			,adv.aQuery.ctypes,adv.aQuery.ctype_avgs,str(adv.aQuery.residence),str(adv.aQuery.year),str(adv.aQuery.availability),"False")	
		
		searchFlag = 0 
		searchTerm = ''
		srcWordList = adv.aQuery.srchWords
		# convers search terms to a string with AND between the terms
		for i in range(0,len(srcWordList)):
			searchTerm += srcWordList[i]
			if (i<len(srcWordList)-1):
				searchTerm += " AND "
		logging.info(searchTerm)
		# if a search term(s) exist call the getSearchQuery function to get results
		if (searchTerm != ''):
			searchFlag = 1
			s = getSearchQuery(searchTerm)
		
		#check the results of the search in cvs
		if (searchFlag==1):
			# if result is empty
			if(s==[]):
				logging.info("no search results for ad")
				return s
			# unifing the results of the two queries
			elif(s!=[] and (q!=None and q!=[])):
				logging.info("search res: " + str(s))
				qUnion = []
				for std in q:
					#logging.info("student id: " + str(std.google_id))
					if std.google_id in s:
						qUnion.append(std)
				q = qUnion
		
		if q==None: 
			return q
		adv.aQuery.ctypes = ctypesBack
		adv.put()
		return q
		
	def get(self):
		user_id = self.request.cookies.get('id')
		
		if (Company.query(user_id==Company.user_id).get()==None):
			self.response.write(errorPage("זמן החיבור פג"))
		else:
			ad_id = self.request.get('ad_id')
			
			comp = Company.query(Company.user_id == user_id).get()
			email = comp.email
			ad_query = Ad.query(Ad.message.compMail == email).order(Ad.message.date).fetch()
			#ad_query = Ad.query(Ad.user_id ==user_id).fetch()
			
			if (int(ad_id)<0 or int(ad_id)>=len(ad_query)):
				self.redirect("/currentAds")
				return
				
			ad = ad_query[int(ad_id)]
			
			q = companyAdResultsHandler.fetchQuery(self,ad)
			logging.info(ad)
			if q==None: 
				self.response.write(errorPage("קלט שגוי לאתר"))
				return
			if (q==[]):
				f = open("no_results_page.html")
				self.response.write(f.read())
				f.close()
			else: #build result page
				ad.studNum = str(len(q))
				ad.put()
				page = buildQueryResultsPage(q,ad_id,ad,comp)
				self.response.write(page)

class adSchedHandler(webapp2.RequestHandler):
	def get(self):
		logging.info("ad schedular started")
		user_id = self.request.cookies.get('id')
		
		ad_query = Ad.query()
		logging.info(ad_query.count())
		cmpAdHandler = companyAdResultsHandler()
		logging.info("ad schedular flag")
		i = 0 
		for ad in ad_query:
				
			if (ad.aQuery.scheduler == False):
				continue
				
			q = cmpAdHandler.fetchQuery(ad)
			logging.info(str(i) + " len q " + str(len(q)) + " studNum " + ad.studNum) 
			if (len(q) > int(ad.studNum)):
				for student in q:
					if(student.google_id not in ad.sentId):
						logging.info("student detected")
						#self.response.write(errorPage("new student detected"))
							
						sender_address = "TauHireTeam@gmail.com"
						subject = "TauHire team - new candidates are waiting for you"
						body = "Dear Sir/Madam,\n\n"+"Your Ad" + ad.message.jobName + " have a new candidates in TauHire website: \n \n"+\
						"Best regards"+"\n\n"+"TauHireTeam"
							
						logging.info(ad.message.compMail)
						mail.send_mail(sender_address, ad.message.compMail, subject, body)
						break
					#else:
						#self.response.write(errorPage("no new student detected"))
						#break
			i+=1
		self.response.write(errorPage("scheduler ran successfully"))	

class messageRemover(webapp2.RequestHandler):
					
	def get(self):
		i = 0
		mess_id = self.request.get('mess_id')
		user_id = self.request.cookies.get('id')
		st = Student.query(Student.user_id==user_id).get() 
		
		conv_query = Conversation.query().order(Conversation.message.date)
		mess_query = Message.query().order(Message.date)
		
		for conver in conv_query:
			for mess in conver.message:
				if(mess.receiver.identity == st.google_id):
					logging.info(str(i))
					i+=1
				if (i==int(mess_id)):
					logging.info("found")
					logging.info(conver.key)
					conver.key.delete()
					break
		i=0			
		for msg in mess_query:
			if(mess.receiver.identity == st.google_id):
				logging.info(str(i))
				i+=1
			if (i==int(mess_id)):
				logging.info("found")
				logging.info(msg.key)
				msg.key.delete()
				break
		t.sleep(1)
		self.redirect("/StudentOffersPage")
		
				

class compSignUpHandler(webapp2.RequestHandler):
	def get(self): 
		page = buildCompanySignUp()
		self.response.write(page)

class signUpHandler(webapp2.RequestHandler):
	def post(self): 
		role = self.request.get('role')
		company = self.request.get('compName')
		compMail = self.request.get('mailAdd')

		if (len(role)>70) or (len(company)>70) or (len(compMail)>70):
			self.response.write(errorPage("שגיאה במילוי הטופס"))
			return
		
		if (len(role)==0) or (len(company)==0) or (len(compMail)==0):
			self.response.write(errorPage("שגיאה במילוי הטופס"))
			return
		
		if ("@" not in compMail) or (" " in compMail):
			self.response.write(errorPage("שגיאה במילוי הטופס"))
			return
		
		tau_address = "tauhireteam@gmail.com"
		subject = "New Company Wants To Sign Up"
		body = role + " from " + company + " want to sign up for the site \n \n"+ "their mail address is: " + compMail

		mail.send_mail(tau_address, tau_address, subject, body)
		
		subjectComp = "TauHire team - thank you for signing up"
		bodyComp = """Dear Sir/Madam,\n\n We recieved your request and it is being
		processed at the moment. You will be notified upon completion. 
		Afterwards, you will be able to log in to the site using the
		Gmail address you've signed up with. \n \n 
		Best regards\n\nTauHireTeam"""    

		mail.send_mail(tau_address, compMail, subjectComp, bodyComp)
		self.response.write(errorPage("תודה רבה על פנייתכם. יישלח אליכם מייל מיד עם אישור חשבון המשתמש"))


				
class Logout(webapp2.RequestHandler):
	#class that handles logout and cookie removal
	def get(self):
		user_id = self.request.cookies.get('id')
		student_query = Student.query(Student.user_id==user_id).get()
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

#class doubleLogin(webapp2.RequestHandler):
#	def get(self):
#		logging.info('LogInForBarak START')
#		f = open("doublelogin.html")
#		self.response.write(f.read())
#		f.close()



app = webapp2.WSGIApplication([
	('/unauthorized', UnauthorizedPage),
	('/validateStudent', ValidateStudent),
	('/deleteStudent', deleteStudent),
	('/validateCompany', ValidateCompany),
	('/dbUserIdScramble', dbUserIdScramble),
	#('/dbDelete', dbDelete),
	('/dbBuild', dbBuild),
	('/adDbBuild', adDbBuild),
	('/studentInputPage', StudentInputHandler),
	('/gradeSheet', GradeSheetHandler),
	#('/StudentWelcomePage/index.html', WelcomeHandler),	
	('/studenthandler', StudentHandler),
	('/tokenSignIn', tokenSignIn),
	('/StudentLogout', Logout),
	('/dbHandler', dbHandler),
	('/companyQueryFormPage', CompanyHandler),
	('/companyQueryResultsPage' , minGradeQuery),
	('/StudentOffersPage', MessageHandler),
	('/messageSend', MessageSend),
	#('/messageReply', MessageReply),
	('/studentEditPage', StudentEditHandler),
	('/deleteMyCV', deleteMyCV),
	('/getMyCV', getMyCV),
	('/getCV', getCV),
	('/createAd', companyAdHandler),
	('/currentAds', companyCurrAdHandler),
	('/editAd', companyEditAdHandler),
	('/showAdResults', companyAdResultsHandler),
	('/deleteAd', companyAdRemover),
	('/processAd', adHandler),
	('/adScheduler', adSchedHandler),
	('/deleteMessage', messageRemover),
	('/HelpPage', HelpHandler),
	#('/doubleLogin', doubleLogin)
	('/companySignUp', compSignUpHandler),
	('/signUpHandler', signUpHandler),
	('/', LogInForBarak)
	
	], debug=True)


