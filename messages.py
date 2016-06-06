import cgi
import urllib
import datetime
import time as t

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail


import webapp2
import logging

import db 

from main import *
from db import *
from methods import *


MESSAGE_PAGE_HTML = """\
<html>
  <body>
    <form action="/messageSend" method="post">
	  send to:
	  <input type="text" name="recv" ><br>
      <div><textarea name="mess" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="send message"></div>
    </form>
	<br><br>
	</div><p>messages:</p><div>
	
  </body>
</html>
"""


# classes for the message system
class threadNum(ndb.Model):
	num = ndb.IntegerProperty(indexed = False)

class Author(ndb.Model):
	identity = ndb.StringProperty(indexed=False)

class Message(ndb.Model):
	#thread = ndb.IntegerProperty(indexed = False)
	sender = ndb.StructuredProperty(Author)
	receiver = ndb.StructuredProperty(Author)
	#receiver = ndb.StringProperty(indexed=False)
	cont = ndb.StringProperty(indexed=False)
	compMail = ndb.StringProperty(indexed=False)
	compName = ndb.StringProperty(indexed=False)
	jobName = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class Conversation(ndb.Model):
	id = ndb.StringProperty(indexed = False)
	message = ndb.StructuredProperty(Message, repeated=True)
	#parameters	

class Ad(ndb.Model):
	user_id = ndb.StringProperty(indexed=True, required=True)
	sentId = ndb.StringProperty(repeated=True)
	message = ndb.StructuredProperty(Message)
	aQuery = ndb.StructuredProperty(adQuery) 
	
class MessageHandler(webapp2.RequestHandler):
    def get(self):
		logging.info("message handler")
		conv_query = Conversation.query()	
		#mess_query = Message.query()
		#self.response.write(MESSAGE_PAGE_HTML)
		userid = self.request.cookies.get('id')
		page = buildStudentOffersPage(conv_query,userid)
		"""
		for conver in conv_query:
			for message in conver.message:
				if(message.receiver == users.get_current_user().nickname()):
					send = users.User(_user_id = message.sender.identity)
					self.response.write('<p>recieved: %s</p>' %message.date)
					self.response.write('<p>from: %s</p>' %send.nickname())
					self.response.write('<p>%s</p><br>' %message.cont)
					#self.response.write('<div><a href="/messageReply?%s">reply</a></div>' %conver.id)
	"""
		self.response.write(page)



class MessageSend(webapp2.RequestHandler):
	# def getEmail(self):
	# 	user_id = self.request.cookies.get('id')
	# 	student_query=Student.query(Student.user_id==user_id).get()
	# 	comapny_query=Company.query(Company.user_id==user_id).get()
	# 	if (student_query!=None):
	# 		email = student_query.email
	# 	elif (comapny_query!=None):
	# 		email = comapny_query.email
		
	# 	logging.info("getEmailResult:"+email)
	# 	self.response.write('getEmailResult is:' + email+'\n')
	# 	return email

	def post(self):
		#self.conNum = threadNum(num=0)
		#self.conNum.put()
		ad_id = self.request.get('ad_id')
		logging.info(ad_id)
		if (int(ad_id)!=-1):
			user_id = self.request.cookies.get('id')
			ad_query = Ad.query(Ad.user_id ==user_id).fetch()
			self.ad = ad_query[int(ad_id)]
			
		
		
		recList = self.request.get_all('studentselect') 
		destAdd = self.request.get('recv') + "@example.com"
		#destId = users.User(destAdd)
		#logging.info(len(recList))
		#destIdKey = destId.put()
		#destIdVal = destIdKey.get()
		#self.key = appUser(usr=destId).put()
		#self.rec = self.key.get()
		
		for rec in recList:
			self.conversation = Conversation()
			self.message = Message(cont = self.request.get('note'))
			self.message.receiver = Author(identity = rec)
			self.message.compName = self.request.get('companyName')
			self.message.jobName = self.request.get('jobId')
			self.message.compMail = self.request.get('companyMail')
			self.message.date = datetime.datetime.now()
			userid = self.request.cookies.get('id')
			self.message.sender = Author(identity = userid)
			
			if (int(ad_id)!=-1):
				self.ad.sentId.append(rec)
				self.ad.put()
				
			#if users.get_current_user():
				#self.message.sender = Author(identity=users.get_current_user().user_id())
			
			self.conversation.message = [self.message]
		
			#conNum = threadNum.query().get()
			#self.conversation.id = conNum.num
			#conNum.num +=1
			#conNum.put()
			self.conversation.put()
			self.message.put()

			student=Student.query(Student.user_id==rec).get()
			if student.allow_emails==True:
				user_address=student.email
				
				if not mail.is_email_valid(user_address):
					self.response.write("Error: student email address is not valid!")
				else:
					sender_address = "TauHireTeam@gmail.com"
					subject = "TauHire team - New Message Notification"
					# body = """ Dear Sir/Madam, \n \n 
					# You have a new Job Offer in TauHire website, \n \n 
					# Please visit our site to view your messages, \n \n 
					# Best regards, \n \n TauHire team"""
					body = "Dear Sir/Madam,\n\n"+"You have a new message in TauHire website: \n \n" + \
					"From: "+ self.message.compName + "\n\n"+"Company mail: "+ self.message.compMail+"\n\n"+\
					"Job name: "+ self.message.jobName+ "\n\n"+"Message content: "+ self.message.cont+"\n\n"+\
					"Best regards"+"\n\n"+"TauHireTeam"

					mail.send_mail(sender_address, user_address, subject, body)
					#self.response.write("mail was good")

		#self.response.write("""<html><body> <b> message send successfully! </b> </body></html>""")
		cours_query = Course.query()
		page = buildCompanyQuery(cours_query)
		self.response.write(page)
		#self.response.write('</pre></body></html>')

		self.response.write("""<html>
									<link rel="stylesheet" type="text/css" href="companyQueryFormPage/style.css">

									<body>
										
									</body>

	<script type="text/javascript" src="StudentWelcomePage/script.js"></script>
	<div class="popup" data-popup="popup-1">
    <div class="popup-inner">
        <h2 class="txt">message was sent successfully!</h2>
		
        <a class="popup-close" data-popup-close="popup-1" href="#">x</a>
    </div>
</div>

		<a class="btn" hidden data-popup-open="popup-1" href="#">Open Popup #1</a>
														

									</html>""")


class MessageReply(webapp2.RequestHandler):
	def get(self):
		self.response.write(MESSAGE_PAGE_HTML)
		
	def post(self):
		self.message = Message(cont = self.request.get('mess'))

class adHandler(webapp2.RequestHandler):
	
	def post(self):
		ad_id = self.request.get('ad_id')
		user_id = self.request.cookies.get('id')
		comp_query = Company.query(Company.user_id ==user_id).get()
		
		course_names=self.request.get_all('name')
		grade = self.request.get_all('grade')
		average=self.request.get('avg')
		if(average==""):
			average = 0
		crstypes=self.request.get_all("ctype")
		crstype_avgs=self.request.get_all("ctype_avg")
		residence=self.request.get("residence")
		year=self.request.get("year")
		availability=self.request.get("availability")
		adCont = self.request.get("note")
		adName = self.request.get("jobId")
		 
		if (int(ad_id)==-1):
			logging.info("ad id = -1")
			self.ad = Ad()
			self.ad.sentId = []
		else:
			adqy = Ad.query(Ad.user_id ==user_id ).fetch()
			self.ad = adqy[int(ad_id)]
		
		dbHandler = db.dbHandler()
		stdCrs= dbHandler.createStudentCourse(course_names, grade)
		
		self.qry = adQuery()
		self.qry.student_courses=stdCrs
		self.qry.cgrades = grade
		self.qry.avg= int(average)
		self.qry.ctypes = crstypes 
		self.qry.ctype_avgs=crstype_avgs
		self.qry.residence= int(residence)
		self.qry.availability= int(availability)
		self.qry.year= int(year)
		self.qry.hasGit= "False"

		#student_courses=ndb.StructuredProperty(Student_Course,repeated=True)
		#cgrades= ndb.ComputedProperty(lambda self: ",".join(Student.getCGrades()))
		#avg= ndb.IntegerProperty(indexed=True, required=True)
		#ctypes = ndb.ComputedProperty(lambda self: ",".join(Student.getCTypes()))
		#ctype_avgs=ndb.StringProperty(indexed=True,repeated = True)
		#residence=ndb.IntegerProperty(indexed=True, required=True)
		#availability=ndb.IntegerProperty(indexed=True, required=True)
		#year=ndb.IntegerProperty(indexed=True, required=True)
		#hasgit = ndb.ComputedProperty(lambda self: self.hasGit())
		
		self.message = Message(cont = adCont)
		self.message.jobName = adName
		self.message.compMail = comp_query.email
		self.message.compName = comp_query.name
		
		self.ad.user_id = user_id
		self.ad.message = self.message
		self.ad.aQuery = self.qry 
		self.ad.put()
		
		self.response.write ("""<html><script>
				window.location="/currentAds";
				</script></html>""")

# class ConfirmUserSignup(webapp2.RequestHandler):
#     def post(self):
#     	user_address = self.request.get('companyMail')
#     	#self.response.write('mail is:' + user_address)
#     	logging.info(user_address)
#         if not mail.is_email_valid(user_address):
#             self.response.write("please enter valid email address, please please please!!!")
#         else:
#         #sender_address = "Example.com Support <support@example.com>"
#         	sender_address = "support@example.com"
#         	subject = "Confirm your registration"
#         	body = """ I'm in! Yalla Macabi!!!!!!!!!!!!!!!!!!!!!!!!! """
#         	mail.send_mail(sender_address, user_address, subject, body)
#         	self.response.write("mail was good")