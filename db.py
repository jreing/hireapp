import cgi
import urllib
import datetime
from methods import *

#for hashing
import hashlib
from time import time

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

#for debugging
import logging

#DB class definitions:

class Course(ndb.Model):
	"""Sub model for representing a course."""
	course_id = ndb.StringProperty(indexed=True, required=True)
	course_name = ndb.StringProperty(indexed=True, required=True)
	course_type = ndb.IntegerProperty(indexed=False, required=True)
	course_weight = ndb.IntegerProperty(indexed=False, required=True)
	

class Student_Course(ndb.Model):
	grade = ndb.IntegerProperty(indexed=True, required=True)
	#weight = ndb.IntegerProperty(indexed=False, required=True)
	#semester = ndb.StringProperty(indexed=False, required=True)
	course= ndb.StructuredProperty (Course, required=True)
	#course_type=ndb.ComputedProperty(lambda self: self.course.course_type)
	#hashed_id = ndb.IntegerProperty(indexed=False)
	
class Student(ndb.Model):
	#function for computed property that gets types of courses student has
	def getCTypes(self):
		ctypes=[]
		#logging.info ("GET C TYPES")
		for sc in self.student_courses:
			if (sc.course==None): 
				logging.info ("NONE")
				continue
			if str(sc.course.course_type) not in ctypes:
				ctypes.append(str(sc.course.course_type))
		#logging.info (ctypes)
		#logging.info ("GET C TYPES FINISHED")
		return ctypes
	google_id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True, required=True)
	student_courses=ndb.StructuredProperty(Student_Course,repeated=True)	
	avg= ndb.IntegerProperty(indexed=True, required=True)
	cv_blob_key = ndb.BlobKeyProperty()
	user_id= ndb.StringProperty(indexed=True, required=True)
	email=ndb.StringProperty(indexed=True, required=True)
	ctypes = ndb.ComputedProperty(lambda self: ",".join(self.getCTypes()))
	
	
class Company(ndb.Model):
	google_id = ndb.StringProperty(indexed=True, required=True)
	user_id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=False)
	email = ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True, required=False)
	
	
class minGradeQuery(webapp2.RequestHandler):

	#function that check whether student has courses in the relevant cluster
	def studentHasCType(self,student, ctype):
		
		for c in student.ctypes.split(","):
			if c==ctype: return True
		return False

	def studentCTypeAvg(self,student,ctype):
		weighted_sum=0
		num_points=0
		#logging.info("STARTED AVG" +str(ctype))
		
		for sc in student.student_courses:
			#logging.info(sc.course.course_type)
			#logging.info(ctype)
			if (str(sc.course.course_type)==str(ctype)):
				
				weighted_sum+=sc.grade*sc.course.course_weight
				num_points+=sc.course.course_weight
				#logging.info(str(weighted_sum)+ "/"+str(num_points))
				
		if (num_points==0): return 0
		else: return weighted_sum/num_points
		
	def post(self):	 
		course_names=self.request.get_all('name')
		grades= self.request.get_all('grade')
		average=self.request.get('avg')	
		ctype=self.request.get("ctype")
		ctype_avg=self.request.get("ctype_avg")
		
		q=Student.query()
		

		logging.info(ctype)
		
		
		#filter out student by grades in specific courses
		for i in range (0,len(grades)-1):	
			if grades[i]=="" :
				break
			#logging.info(i)
			#logging.info (len(grades)-1)
			grade=int(grades[i])
			q=q.filter (Student.student_courses.grade>=grade, Student.student_courses.course.course_name==course_names[i])
		#filter out by average
		if average!="":
			average=int(average);
			q=q.filter (Student.avg>=average)	

		#self.response.write(q)
		## TODO: write the response in a nicer way
		q.fetch(100)
		
		if(ctype!=0):
			filteredRes=[]
			for student in q:
				if self.studentHasCType(student,ctype):
					sctavg=self.studentCTypeAvg(student,ctype)
					#logging.info("SCTAVG:" + str(sctavg))
					if (int(sctavg)>=int(ctype_avg)):
						filteredRes.append(student)
			q=filteredRes
			#logging.info(q)
			
		page = buildQueryResultsPage(q)
		self.response.write(page)

#adds all courses to DB from the parsed courses files
class dbBuild(webapp2.RequestHandler):
	
	def get(self):
		import csv
		with open('courses2.csv', 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')
			for row in spamreader:
				c=Course(course_name=row[0],course_id=row[1], course_type=int(row[2]), course_weight=int(row[3]))
				c.put()
		
		self.response.write('Database built')

#deletes all courses from DB	
class dbDelete(webapp2.RequestHandler):
	def get(self):
		passw=self.request.get("passw")
		if (passw=="weLoveYouGoogle2016"):
			ndb.delete_multi(Course.query().fetch(keys_only=True))
			self.response.write('Database deleted')
		else:
			self.response.write('Wrong password')

#changes all hash id's in the DB
class dbUserIdScramble(webapp2.RequestHandler):
	def get(self):
		passw=self.request.get("passw")
		if (passw=="weLoveYouGoogle2016"):
			q=Student.query()
			for s in q:
				s.user_id=str(hashlib.sha512(s.google_id + str(time())).hexdigest())
				s.put()
			q=Company.query()
			for c in q:
				c.user_id=str(hashlib.sha512(c.google_id + str(time())).hexdigest())
				c.put()
			self.response.write('Database scrambled')
		else:
			self.response.write('Wrong password')


#adds Student to DB
class dbHandler(webapp2.RequestHandler):
	def post(self):	
		#get userid from cookie
		user_id = self.request.cookies.get('id')
		
		st = Student.query(Student.user_id==user_id).get()
		
		#get student's cv file
		cv=self.request.get('cv')
		if (cv!=""):
			#validate the user's file is a REAL PDF.
			if (self.checkPdfFile(cv)==False):
				#TODO - more elegent error message
				self.response.write("erroneos file")
				return
			
			#write user's CV File into blobstore
			cv_blob_key=self.CreateFile(st.google_id,cv)
		
		course_names=self.request.get('name', allow_multiple=True)
				
		grade= self.request.get('grade', allow_multiple=True)
		if (len(course_names)!=len(grade)):
			self.response.write ("Error")
		s=[]
		for i in range(0,len(course_names)):
			course_query=Course.query (Course.course_name==course_names[i]).get()
			#logging.info (course_query)
			s.append(Student_Course(grade=int(grade[i]), course=course_query))
		
		
		#people_resource = service.people()
		#people_document = people_resource.get(userId='me').execute(
		city = self.request.get('city')
		st.student_courses=s
		#logging.info(s)
		st.name = "demo"
		st.city = self.request.get('city')
		st.avg = 1000
		if (cv!=""):
			st.cv_blob_key=BlobKey(cv_blob_key)
		else:
			st.cv_blob_key=None
		st.put()
		
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
	
	def CreateFile(self,user_id, cv):
		"""Create a GCS file with GCS client lib.
		Args:
			filename: GCS filename.
		Returns:
			The corresponding string blobkey for this GCS file.
		"""
		#saving the file in the blob store using the users google id
		#then a blobstore key is generated from that (not visible to user)
		# Create a GCS file with GCS client.
		#write user's CV File into blobstore
		write_retry_params = gcs.RetryParams(backoff_factor=1.1)
		bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())
		bucket = '/' + bucket_name
		filename = bucket + '/'+user_id + '.cv'
		gcs_file = gcs.open(filename=filename,content_type="application/pdf", mode='w',retry_params=write_retry_params)
		gcs_file.write(cv)
		gcs_file.close()
		blobstore_filename = '/gs' + filename
		return blobstore.create_gs_key(blobstore_filename)
		

#use this function to get user's own CV
class getMyCV(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		st = Student.query(Student.user_id==user_id).get()
		self.send_blob(st.cv_blob_key)

#use this function for companies to see student CVs
#get the user_id using the hashed version
class getCV(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		user_id = self.request.get('user_id')
		st = Student.query(Student.user_id==user_id).get()
		
		if (st!=None):
			self.send_blob(st.cv_blob_key)

#classes that send pages to user, should check if the duplicates can be reduced
