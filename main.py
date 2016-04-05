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
	
class Student_Course(ndb.Model):
	grade = ndb.IntegerProperty(indexed=False, required=True)
	weight = ndb.IntegerProperty(indexed=False, required=True)
	semester = ndb.StringProperty(indexed=False, required=True)
	course= ndb.StructuredProperty (Course, required=True)
	student_id= ndb.IntegerProperty	(indexed=True, required=True)
	hashed_id = ndb.IntegerProperty(indexed=False)

class dbHandler(webapp2.RequestHandler):
    def post(self):	 
        
	c=Course(course_id='1', course_name=self.request.get('name'), course_type="class")
	
	c.put()
	self.response.write('<html><body>')
	self.response.write('Test Entry added')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        f = open("index.html") 
	self.response.charset="unicode"
	self.response.write(f.read())
	f.close()        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/dbHandler', dbHandler)
], debug=True)
