import cgi
import urllib
import datetime
from methods import *

#for blobstore
from google.appengine.ext import blobstore
from google.appengine.ext.blobstore import BlobKey
from google.appengine.ext.webapp import blobstore_handlers

#required for Google Cloud Storage
import os
import cloudstorage as gcs
from google.appengine.api import app_identity

my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
###

##to validate pdf files
import pyPdf
from StringIO import StringIO

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import logging

#DB class definitions:

class Course(ndb.Model):
	"""Sub model for representing a course."""
	course_id = ndb.StringProperty(indexed=True, required=True)
	course_name = ndb.StringProperty(indexed=True, required=True)
	course_type = ndb.StringProperty(indexed=False, required=True)

class Student_Course(ndb.Model):
	grade = ndb.IntegerProperty(indexed=True, required=True)
	#weight = ndb.IntegerProperty(indexed=False, required=True)
	#semester = ndb.StringProperty(indexed=False, required=True)
	course= ndb.StructuredProperty (Course, required=True)
	#hashed_id = ndb.IntegerProperty(indexed=False)
	
	
class Student(ndb.Model):
	id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=True)
	#email = ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True, required=True)
	student_courses=ndb.StructuredProperty(Student_Course,repeated=True)	
	avg= ndb.IntegerProperty(indexed=True, required=True)
	cv_blob_key = ndb.BlobKeyProperty()



class Company(ndb.Model):
	id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=False)
	#email = ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True, required=False)
	
	
	
class minGradeQuery(webapp2.RequestHandler):
	def post(self):	 
		course_names=self.request.get_all('name')
		grades= self.request.get_all('grade')
		average=self.request.get('avg')	
				
		#self.response.write('<html><body>')
		#debug prints
		
		#self.response.write(int(grades[0]))
		#self.response.write(int(grades[1]))
		#self.response.write("<br>End of Debug prints<br><br>")
		q=Student.query()
		#filter out student by grades in specific courses
		for i in range (0,len(grades)-1):	
			if grades[i]=="" :
				break
			logging.info(i)
			logging.info (len(grades)-1)
			grade=int(grades[i])
			q=q.filter (Student.student_courses.grade>=grade, Student.student_courses.course.course_name==course_names[i])
		#filter out by average
		if average!="":
			average=int(average);
			q=q.filter (Student.avg>=average)	

		#self.response.write(q)
		## TODO: write the response in a nicer way
		q.fetch(100)
		#for student in q:
		#	self.response.write("""<br> <h1 style="color:red">Student %s <br>""" %student)
		#self.response.write('End of Results</html></body>')
		page = buildQueryResultsPage(q)
		self.response.write(page)

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

#adds Student to DB
class dbHandler(webapp2.RequestHandler):
	def post(self):	
		#get userid from cookie
		userid = self.request.cookies.get('id')
		
		#get student's cv file
		cv=self.request.get('cv')
		if (cv!=""):
			#validate the user's file is a REAL PDF.
			if (self.checkPdfFile(cv)==False):
				#TODO - more elegent error message
				self.response.write("erroneos file")
				return
			
			#write user's CV File into blobstore
			cv_blob_key=self.CreateFile(userid,cv)
		
		course_names=self.request.get('name', allow_multiple=True)
		grade= self.request.get('grade', allow_multiple=True)
		if (len(course_names)!=len(grade)):
			self.response.write ("Error")
		s=[]
		for i in range(0,len(course_names)):
			c=Course(course_id='1', course_name=course_names[i], course_type="class")
			s.append(Student_Course(grade=int(grade[i]), course=c))
		
		
		#people_resource = service.people()
		#people_document = people_resource.get(userId='me').execute(
		st = Student.query(Student.id==userid).get()
		st.student_courses=s
		st.name = "demo"
		st.city = self.request.get('city')
		st.avg = 40
		if (cv!=""):
			st.cv_blob_key=BlobKey(cv_blob_key)
		else:
			st.cv_blob_key=None
		#st= Student(student_courses=s,id="2", name="demo", city="demo",avg=40)
		st.put()
		## TODO: write the response in a nicer way
		#self.response.write('<html><body>Test Entry added</body></html>')
		self.response.write ("""<html><script>
			window.location="StudentWelcomePage/index.html";
			</script></html>""")
	
	def checkPdfFile (self,file):
		cvFile= StringIO(file)
		try:
			doc = pyPdf.PdfFileReader(cvFile)
			return True
		except: 
			return False
	
	def CreateFile(self,userid, cv):
		"""Create a GCS file with GCS client lib.
		Args:
			filename: GCS filename.
		Returns:
			The corresponding string blobkey for this GCS file.
		"""
		# Create a GCS file with GCS client.
		#write user's CV File into blobstore
		write_retry_params = gcs.RetryParams(backoff_factor=1.1)
		bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())
		bucket = '/' + bucket_name
		filename = bucket + '/'+userid + '.cv'
		gcs_file = gcs.open(filename=filename,content_type="application/pdf", mode='w',retry_params=write_retry_params)
		gcs_file.write(cv)
		gcs_file.close()
		# Blobstore API requires extra /gs to distinguish against blobstore files.
		blobstore_filename = '/gs' + filename
		# This blob_key works with blobstore APIs that do not expect a
		# corresponding BlobInfo in datastore.
		return blobstore.create_gs_key(blobstore_filename)
		

class getMyCV(blobstore_handlers.BlobstoreDownloadHandler):

	def get(self):
		userid = self.request.cookies.get('id')
		st = Student.query(Student.id==userid).get()
		self.send_blob(st.cv_blob_key)

class getCV(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		
		userid = self.request.get('user_id')
		self.response.write("<html>"+ userid+ "</html>")
		st = Student.query(Student.id==userid).get()
		self.response.write (userid)
		if (st!=None):
			self.send_blob(st.cv_blob_key)

#classes that send pages to user, should check if the duplicates can be reduced
