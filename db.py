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
	
	def hasGit(self):
		return self.git!=""
		
	google_id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True)
	student_courses=ndb.StructuredProperty(Student_Course,repeated=True)	
	avg= ndb.IntegerProperty(indexed=True, required=True)
	cv_blob_key = ndb.BlobKeyProperty()
	user_id= ndb.StringProperty(indexed=True, required=True)
	email=ndb.StringProperty(indexed=True, required=True)
	ctypes = ndb.ComputedProperty(lambda self: ",".join(self.getCTypes()))
	allow_emails= ndb.BooleanProperty(indexed=False, required=True)
	residence=ndb.IntegerProperty(indexed=True, required=True)
	availability=ndb.IntegerProperty(indexed=True, required=True)
	year=ndb.IntegerProperty(indexed=True, required=True)
	git=ndb.StringProperty(required=True)
	hasgit = ndb.ComputedProperty(lambda self: self.hasGit())
	
	
class allowedCompany(ndb.Model):
	email =ndb.StringProperty(indexed=True, required=True)
	
class Company(ndb.Model):
	google_id = ndb.StringProperty(indexed=True, required=True)
	user_id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=False)
	email = ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True, required=False)
	
	
class minGradeQuery(webapp2.RequestHandler):
	def errormsg(self):
		self.response.write("invalid input")
	
	#function that check whether student has courses in the relevant cluster
	def studentHasCType(self,student, ctype):
		if (ctype==''): return False
		for c in student.ctypes.split(","):
			if c=='': return False
			if int(c)==int(ctype): return True
		return False
	
	#a function that given a student and ctype calculates his/her avg 
	#in that ctype
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
		ctypes=self.request.get_all("ctype")
		ctype_avgs=self.request.get_all("ctype_avg")
		residence=self.request.get("residence")
		
		logging.info("grades " + str(len(grades)))
		logging.info("course " + str(len(course_names)))
		logging.info("average " + str(average))
		logging.info("ctypes " + str(len(ctypes)))
		logging.info("ctype_avgs " + str(len(ctype_avgs)))
		logging.info("residence " + str(residence))
		
		#server side input validation
		if len(grades)!=len(course_names): self.errormsg()
		for crs in course_names:
			if len(crs)>50: self.errormsg()
		for grade in grades:
			if grade!="" and grade.isdigit()==False: self.errormsg()
		if average!="" and average.isdigit()==False: self.errormsg()
		if (len(ctypes)!=len(ctype_avgs)): self.errormsg()
		if (len(ctypes) >0 and ctypes[0]!=""):
			for ctype in ctypes:
				if ctype.isdigit()==False: self.errormsg()
		if (len(ctype_avgs)>0 and ctypes[0]!=""):
			for ctype_avg in ctype_avgs:
				if ctype_avg!="" and ctype_avg.isdigit()==False: self.errormsg()
		if residence.isdigit()==False: self.errormsg()
		
		if year.isdigit()==False: self.errormsg()
		if availability.isdigit()==False: self.errormsg()
		if len(hasgit)>5: self.errormsg()

		q=Student.query()
		q.fetch(100)
		
		#filter by availability
		if (int(availability)>0 and int(availability)<6):
			p=Student.query(Student.availability==int(availability))
			p.fetch(100)
			q = [val for val in p if val in q]
		
		#filter by hasgit
		if (hasgit=="True"):
			p=Student.query(Student.hasgit==True)
			p.fetch(100)
			q = [val for val in p if val in q]
		
		#filter by year
		if (int(year)>0 and int(year)<6):
			p=Student.query(Student.year==int(year))
			p.fetch(100)
			q = [val for val in p if val in q]
		
		#filter by residence
		if (int(residence)>0 and int(residence)<6):
			p=Student.query(Student.residence==int(residence))
			p.fetch(100)
			q = [val for val in p if val in q]
			
		#filter out student by grades in specific courses
		for i in range (0,len(grades)):	
			if grades[i]=="" :
				break
			#logging.info(i)
			#logging.info (len(grades)-1)
			grade=int(grades[i])
			p=Student.query(Student.student_courses.grade>=grade, Student.student_courses.course.course_name==course_names[i])
			p.fetch(100)
			q = [val for val in p if val in q]
			
		#filter out by average
		if average!="":
			p=Student.query (Student.avg>=int(average))
			logging.info("MAIN AVERAGE QUERY")
			p.fetch(100)
			q = [val for val in q if val in p]

		for i in range(0,len(ctypes)):
			#logging.info(i)
			filteredRes=[]
			ctypes[i]=int(ctypes[i])
			if(ctypes[i]!=0):
				#logging.info("CTYPE QUERY")
				for student in q:
					if self.studentHasCType(student,ctypes[i]):
						sctavg=self.studentCTypeAvg(student,ctypes[i])
						logging.info("SCTAVG:" + str(sctavg))
						if (int(sctavg)>=int(ctype_avgs[i])):
							filteredRes.append(student)
			if (i>=1):
				q = [val for val in filteredRes if val in q]
				#logging.info(filteredRes)
			else:
				if (ctypes[0]!=0):
					q=filteredRes
		
		#logging.info(q)
		page = buildQueryResultsPage(q)
		self.response.write(page)

#adds all courses to DB from the parsed courses files
class dbBuild(webapp2.RequestHandler):
	
	def get(self):
		#add a mail to allowedCompany so it can be seen in console
		ac = allowedCompany(email="tauhireteam@gmail.com")
		ac.put()
		
		import csv
		with open('courses3.csv', 'rb') as csvfile:
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
	def errormsg(self):
		#TODO: write prettier error message display
		self.response.write("invalid request to server")
		return 

	def post(self):
		cvKey = False
		#get userid from cookie
		user_id = self.request.cookies.get('id')
		
		st = Student.query(Student.user_id==user_id).get()
		
		#get student's cv file
		cv=self.request.get('cv')
		if (cv!=""):
			#logging.info ("cv detected " + cv)
			
			#validate the user's file is a REAL PDF.
			if (self.checkPdfFile(cv)==False):
				#TODO - more elegent error message
				self.response.write("erroneos file")
				return
			
			#write user's CV File into blobstore
			cv_blob_key=self.CreateFile(st.google_id,cv)
		elif(st.cv_blob_key!=None):
			cvKey = True
		
		if (cv!=""):
			st.cv_blob_key=BlobKey(cv_blob_key)
		elif(cvKey!= True):
			st.cv_blob_key=None
		
		#add courses and grades
		course_names=self.request.get('name', allow_multiple=True)
		grade= self.request.get('grade', allow_multiple=True)
		if (len(course_names)!=len(grade)):
			#self.response.write ("Error")
			self.errormsg()

		
				
		s=[]
		for i in range(0,len(course_names)):
			if (grade[i].isdigit()==False): continue
			if (int(grade[i])>100 or int(grade[i])<60) : continue
			if (len(course_names[i])>50):
				self.errormsg()
				return
			course_query=Course.query (Course.course_name==course_names[i]).get()
			
			if course_query==None : continue
			
			#logging.info (course_query)
			s.append(Student_Course(grade=int(grade[i]), course=course_query))
		
		st.student_courses=s
		
		st.name = "demo"
		#logging.info(self.request.get('getEmailNotification'))
		
		#handle allow-emails
		if (self.request.get('getEmailNotification')=="True"):
			st.allow_emails=True
		else:
			st.allow_emails=False
			
		
		#residence validation and handling
		residence = self.request.get('residence')
		if (residence.isdigit()==False or int(residence)>5 or int(residence)<0):
			self.errormsg()
			return
		st.residence = int(residence)
		
		#year validation and handling
		year = self.request.get('year')
		if (year.isdigit()==False or int(year)>4 or int(year)<0):
			self.errormsg()
			return
		st.year = int(year)
		
		#availablity validation and handling
		availablity = self.request.get('availablity')
		if (availablity.isdigit()==False or int(availablity)>2 or int(availablity)<0):
			self.errormsg()
			return
		st.availablity = int(availablity)
		
		#git validation and handling
		git = self.request.get('git')
		
		if (git!="" and (len(git)>60 or git.find("git")==-1)):
			self.errormsg()
			return
		st.git = git
		
		curr_average = st.avg
		
		#average validation
		new_avg= self.request.get('average')
		if (new_avg.isdigit()==False or int(new_avg)>100 or int(new_avg)<60):
			self.errormsg()
			return
		st.avg = int(new_avg)
		
		
		
		st.put()
		
		if (curr_average == -1):
			self.response.write ("""<html><script>
				window.location="StudentWelcomePage/index.html";
				</script></html>""")
		else:
			self.response.write ("""<html><script>
				window.location="/StudentOffersPage";
				</script></html>""")
	
	def checkPdfFile (self,file):
		logging.info ("check cv")
		cvFile= StringIO(file)
		
		try:
			doc = pyPdf.PdfFileReader(cvFile)
			logging.info ("cv check passed")
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
