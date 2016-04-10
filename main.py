#!/usr/bin/env python
import cgi
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

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
#DB class definitions:

class Course(ndb.Model):
	"""Sub model for representing a course."""
	course_id = ndb.StringProperty(indexed=True, required=True)
	course_name = ndb.StringProperty(indexed=True, required=True)
	course_type = ndb.StringProperty(indexed=False, required=True)
	
class Student(ndb.Model):
	id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True, required=True)
	
class Student_Course(ndb.Model):
	grade = ndb.IntegerProperty(indexed=True, required=True)
	#weight = ndb.IntegerProperty(indexed=False, required=True)
	#semester = ndb.StringProperty(indexed=False, required=True)
	course= ndb.StructuredProperty (Course, required=True)
	student= ndb.StructuredProperty (Student, required=True)
	#hashed_id = ndb.IntegerProperty(indexed=False)

# classes for the message system
class threadNum(ndb.Model):
	num = ndb.IntegerProperty(indexed = False)

class Author(ndb.Model):
	identity = ndb.StringProperty(indexed=False)

class Message(ndb.Model):
	#thread = ndb.IntegerProperty(indexed = False)
	sender = ndb.StructuredProperty(Author)
	#receiver = ndb.StructuredProperty(Author)
	receiver = ndb.StringProperty(indexed=False)
	cont = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class Conversation(ndb.Model):
	id = ndb.IntegerProperty(indexed = False)
	message = ndb.StructuredProperty(Message, repeated=True)	
	
#end of DB class definitions
#

#classes for actions:

class minGradeQuery(webapp2.RequestHandler):
	def post(self):	 
		course_name=self.request.get('name' )
		grade= int(self.request.get('grade'))
		c=Course(course_name=course_name, course_id="1", course_type="class")		
		self.response.write('<html><body>')
		#debug prints
		self.response.write(c)
		self.response.write(grade )
		self.response.write("<br>End of Debug prints<br><br>")
		q=Student_Course.query(Student_Course.grade>=grade, Student_Course.course.course_name==course_name)
		self.response.write(q)
		## TODO: write the response in a nicer way
		q.fetch(100)
		for student in q:
			self.response.write("Student %s <br>" %student)
		self.response.write('End of Results</html></body>')
		


#adds all courses to DB from the parsed courses files
class dbBuild(webapp2.RequestHandler):
	
	def get(self):
		inputfile=open("courses.csv")
		text = inputfile.readlines()
		for i in range(0,len(text)-2,2):
			c=Course(course_name=text[i],course_id=text[i+1], course_type="class")
			c.put()
			
		inputfile.close()
		self.response.write('Database built')

#deletes all courses from DB	
class dbDelete(webapp2.RequestHandler):

	def get(self):
		ndb.delete_multi(Course.query().fetch(keys_only=True))
		self.response.write('Database deleted')

#adds Student_Course to DB
class dbHandler(webapp2.RequestHandler):
    def post(self):	 
		self.response.write('<html><body>Test Entry ')
		self.response.write(self.request)
		course_names=self.request.get('name', allow_multiple=True)
		
		self.response.write("<br><br>")
		
		
		grade= self.request.get('grade', allow_multiple=True)
		if (len(course_names)!=len(grade)):
			self.response.write ("Error")
		for i in range(0,len(course_names)):
			st=Student(id="demo", name="demo", city="demo")
			c=Course(course_id='1', course_name=course_names[i], course_type="class")
			s=Student_Course(student= st, grade=int(grade[i]), course=c) 
			s.put()
		## TODO: write the response in a nicer way
		self.response.write('<html><body>Test Entry added</body></html>')

#classes that send pages to user, should check if the duplicates can be reduced

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
			self.response.write('<br><br><div><a href="/studentinputpage/index.html">input page</a></div>')	
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
        f = open("studentinputpage\index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close()        

class MessageHandler(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
			self.response.write('Hello, ' + user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))
		conv_query = Conversation.query()	
		#mess_query = Message.query()
		self.response.write(MESSAGE_PAGE_HTML)
		for conver in conv_query:
			for message in conver.message:
				if(message.receiver == users.get_current_user().nickname()):
					send = users.User(_user_id = message.sender.identity)
					self.response.write('<p>recieved: %s</p>' %message.date)
					self.response.write('<p>from: %s</p>' %send.nickname())
					self.response.write('<p>%s</p><br>' %message.cont)
					self.response.write('<div><a href="/messageReply?%s">reply</a></div>' %conver.id)



class MessageSend(webapp2.RequestHandler):
	def post(self):
		#self.conNum = threadNum(num=0)
		#self.conNum.put()
		self.conversation = Conversation()
	
		self.message = Message(cont = self.request.get('mess'))
		
		destAdd = self.request.get('recv') + "@example.com"
		#destId = users.User(destAdd)
		
		#destIdKey = destId.put()
		#destIdVal = destIdKey.get()
		#self.key = appUser(usr=destId).put()
		#self.rec = self.key.get()
		
		self.message.receiver = destAdd
		self.message.date = datetime.datetime.now()
		if users.get_current_user():
			self.message.sender = Author(identity=users.get_current_user().user_id())
		
		self.conversation.message = [self.message]
		
		conNum = threadNum.query().get()
		self.conversation.id = conNum.num
		conNum.num +=1
		conNum.put()
		self.conversation.put()
		self.message.put()
		self.response.write('<html><body>message entered<pre>')
		self.response.write('</pre></body></html>')

class MessageReply(webapp2.RequestHandler):
	def get(self):
		self.response.write(MESSAGE_PAGE_HTML)
		
	def post(self):
		self.message = Message(cont = self.request.get('mess'))


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
	('/studentinputpage/index.html', MainHandler),
	('/chooseEmployOrStudentPage/index.html', LoginHandler),
	('/dbHandler', dbHandler),
	('/companyQueryFormPage/index.html', CompanyHandler),
	('/minGradeQuery' , minGradeQuery),
	('/message', MessageHandler),
	('/messageSend', MessageSend),
	('/messageReply', MessageReply)	
	], debug=True)

#Methods to build the companyQueryResultsPage and StudentOffersPage

def buildQueryResultsPage():
	i=0
	htmlstart= """<!DOCTYPE html>
	<html>
	<link rel="stylesheet" type="text/css" href="style.css">
	<body>
	
  <div align="right">
    <p class="titletext">:שליחת משרה</p>
  </div>

  <div id="form-div">
    <div align="right"> <p class="medtitletext">:הזן משרה</p>  </div>
    <form class="form" id="form1" action="advanced.py" method="post">
      <div align="right">
        <p class="text1">:שם החברה</p>
        <input name="name" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="שם" id="name" />
      </div>

      <div align="right">
        <p class="text1">:מייל החברה</p>
        <input name="name" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="מייל" id="name" />
      </div>

      <div align="right">
        <p class="text1">:שם המשרה</p>
        <input name="name" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="משרה" id="name" />
      </div>

      <div align="right">
        <p class="text1">:תיאור המשרה</p>
        <textarea class="scrollabletextbox" name="note" dir="rtl" placeholder="פרטים על המשרה.."></textarea>
        
           
      </div>
	<div align="right" > <p class="medtitletextpadded">:בחר מועמדים</p> </div>

      <div id="scroll" style="overflow-y: scroll; height:450px;">"""
	  
	htmlbody=''
	for obj in database:
		i=i+1
		htmlbody+="""

        <div class="form-element" ; align="right">

          <label for="studentselect"""+i+""" class="textsmallpad">בחר</label>
          <input type="checkbox" id="studentselect"""+i+""" class="texthugepad" value="select">
          <p class="text">לא צורף</p>
          <p class="textbigpad">:קורות חיים</p>
          <p class="text">"""+obj.city+"""</p>
          <p class="text">:עיר</p>

        </div>"""
	
	htmlend="""
      </div>

      <label for="select-all" class="textsmallpad">בחר הכל</label>
      <input type="checkbox" name="select-all" id="select-all" />
      <div class="submit">
        <input type="submit" value="שלח משרה" id="button-blue" />

      </div>
    </form>
	
	<script type="text/javascript" src="jquery-2.2.3.js"></script>
	<script type="text/javascript" src="script.js"></script>
  </div>
  <body>
	<html>"""

	html=htmlstart+htmlbody+htmlend
	return html
	
	
def buildStudentOffersPage():
	i=0
	htmlstart= """<!DOCTYPE html>
<html>
	<link rel="stylesheet" type="text/css" href="style.css">
<body>

  <div >
    <p class="titletext"  >:הפרופיל שלי</p>
  </div>

  <div id="form-div">
    <div align="right"> <p class="medtitletext">:הצעות שקיבלת</p>  </div>
  


      <div id="scroll">"""
	  
	htmlbody=''
	for obj in database:
		i=i+1
		htmlbody+="""

                <div class="form-element" ; align="right">
		
				<div align="right">
					<button type="button" id="button"""+i+"""" class="button">הצג פרטים</button>
					<p class="text">"""+obj.mail+"""</p>
					<p class="text">:מייל</p>
					<p class="text">"""+obj.companyName+"""</p>
					<p class="text">:שם חברה</p>
					<p class="text">"""+obj.jobName+"""</p>
					<p class="text">:שם משרה</p>
				</div>
				
				<div class="form-extra" id="extra"""+i+"""""; align="right">

				<p class="text" id="extra1" >"""+obj.description+"""</p>


				</div>
        </div>"""
	
	htmlend="""
            </div>

    <div align="right"> <p class="medtitletext" id="empty">...טרם קיבלת הצעות</p>  </div>

  </div>


  <body>
			<script type="text/javascript" src="jquery-2.2.3.js"></script>
	<script type="text/javascript" src="script.js"></script>

<html>"""

	html=htmlstart+htmlbody+htmlend
	return html
	
	



