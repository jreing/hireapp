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
    <form action="/sign" method="post">
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
	course_name = ndb.StringProperty(indexed=False, required=True)
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
	#STILL DOESNT WORK - returns results of students that satisfy some requirement	
	def post(self):	 
		course_name=self.request.get('name')
		grade= int(self.request.get('grade'))
		self.response.write('<html><body>')
		self.response.write(grade)
		#Student_Course.grade>=grade
		query=Student_Course.query()
		self.response.write(query)
		## TODO: write the response in a nicer way
		query.fetch(100)
		for student in query:
			self.response.write("Student %s\n" %student)
		self.response.write('End of Results</html></body>')
		


	
class dbBuild(webapp2.RequestHandler):
	#adds all courses to DB from the parsed courses files
	def get(self):
		inputfile=open("courses.csv")
		text = inputfile.readlines()
		for i in range(0,len(text)-2,2):
			c=Course(course_name=text[i],course_id=text[i+1], course_type="class")
			c.put()
			
		inputfile.close()
		self.response.write('Database built')
	
class dbDelete(webapp2.RequestHandler):
	#deletes all courses from DB	
	def get(self):
		ndb.delete_multi(
			Course.query().fetch(keys_only=True)
		)
		self.response.write('Database deleted')
	
		
		
class dbHandler(webapp2.RequestHandler):
	#adds Student_Course to DB
    def post(self):	 
		course_name=self.request.get('name')
		grade= int(self.request.get('grade'))
		st=Student(id="demo", name="demo", city="demo")
		c=Course(course_id='1', course_name=course_name, course_type="class")
		s=Student_Course(student= st, grade=grade, course=c) 
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
		
class MainHandler(webapp2.RequestHandler):
    def get(self):
        f = open("studentinputpage/index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close()        

class Message(webapp2.RequestHandler):
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
					self.response.write('<div><a href="/replay?%s">replay</a></div>' %conver.id)
		
	
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

class MessageReplay(webapp2.RequestHandler):
	def get(self):
		self.response.write(MESSAGE_PAGE_HTML)
		
	def post(self):
		self.message = Message(cont = self.request.get('mess'))
			
	
#list of urls the user enters and functions that handle them
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/dbHandler', dbHandler),
	('/dbDelete', dbDelete),
	('/dbBuild', dbBuild),
	('/studentinputpage/index.html', MainHandler),
	('/companyQueryFormPage/index.html', CompanyHandler),
	('/companyQueryFormPage/minGradeQuery' , minGradeQuery),
	('/message', Message),
	('/messageSend', MessageSend),
	('/messageReplay', MessageReplay),
	
], debug=True)