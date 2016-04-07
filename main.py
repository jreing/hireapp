#!/usr/bin/env python
import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

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

class minGradeQuery(webapp2.RequestHandler):
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
	def get(self):
		inputfile=open("courses.csv")
		text = inputfile.readlines()
		for i in range(0,len(text)-2,2):
			c=Course(course_name=text[i],course_id=text[i+1], course_type="class")
			c.put()
			
		inputfile.close()
		self.response.write('Database built')
	
class dbDelete(webapp2.RequestHandler):
	def get(self):
		ndb.delete_multi(
			Course.query().fetch(keys_only=True)
		)
		self.response.write('Database deleted')
	
		
		
class dbHandler(webapp2.RequestHandler):
    def post(self):	 
		course_name=self.request.get('name')
		grade= int(self.request.get('grade'))
		c=Course(course_id='1', course_name=course_name, course_type="class")
		s=Student_Course(grade=grade, course=c) 
		s.put()
		## TODO: write the response in a nicer way
		self.response.write('<html><body>Test Entry added</body></html>')


class CompanyHandler(webapp2.RequestHandler):
    def get(self):
        f = open("companyQueryFormPage\index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close()        
		
class MainHandler(webapp2.RequestHandler):
    def get(self):
        f = open("studentinputpage\index.html") 
	#self.response.charset="unicode"
	self.response.write(f.read())
	f.close()        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/dbHandler', dbHandler),
	('/dbDelete', dbDelete),
	('/dbBuild', dbBuild),
	('/studentinputpage/index.html', MainHandler),
	('/companyQueryFormPage/index.html', CompanyHandler),
	('/companyQueryFormPage/minGradeQuery' , minGradeQuery)
	
], debug=True)
