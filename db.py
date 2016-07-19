# -*- coding: utf-8 -*-

import cgi
import urllib
import datetime
from methods import *

#for hashing
import hashlib
from time import time

import time as t

#for blobstore
from google.appengine.ext import blobstore
from google.appengine.ext.blobstore import BlobKey
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import search

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
import PyPDF2
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from StringIO import StringIO

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

#for debugging
import logging

INDEX_NAME = 'cv'


#DB class definitions:

class Course(ndb.Model):
	"""Sub model for representing a course."""
	course_id = ndb.StringProperty(indexed=True, required=True)
	course_name = ndb.StringProperty(indexed=True, required=True)
	course_type = ndb.IntegerProperty(indexed=True, required=True)
	course_weight = ndb.IntegerProperty(indexed=True, required=True)
	

class Student_Course(ndb.Model):
	grade = ndb.IntegerProperty(indexed=True, required=True)
	#weight = ndb.IntegerProperty(indexed=False, required=True)
	#semester = ndb.StringProperty(indexed=False, required=True)
	course = ndb.StructuredProperty (Course, required=True)
	course_id= ndb.ComputedProperty(lambda self:self.course.course_id)
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
	
	def getCGrades(self):
		cgrades=[]
		
		#logging.info ("GET C TYPES")
		for sc in self.student_courses:
			if (sc.course==None): 
				logging.info ("NONE")
				continue
			else:
				cgrades.append(str((sc.course_id,sc.grade)))
				
		#logging.info ("GET C TYPES FINISHED")
		return cgrades
	
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
	cgrades= ndb.ComputedProperty(lambda self: ",".join(self.getCGrades()))
	needs_job=ndb.BooleanProperty(indexed=True, required=True)
	cnt= ndb.IntegerProperty(indexed=False, required=True)
	
	cv_view_cnt=ndb.IntegerProperty(indexed=False, required=True)
	cv_viewed_by=ndb.StringProperty(indexed=True, repeated=True)
	gradesheet_view_cnt=ndb.IntegerProperty(indexed=False, required=True)
	gradesheet_viewed_by=ndb.StringProperty(indexed=True,repeated=True)
	
class allowedCompany(ndb.Model):
	email =ndb.StringProperty(indexed=True, required=True)
	
	
class Company(ndb.Model):
	google_id = ndb.StringProperty(indexed=True, required=True)
	user_id = ndb.StringProperty(indexed=True, required=True)
	name= ndb.StringProperty(indexed=True, required=False)
	email = ndb.StringProperty(indexed=True, required=True)
	city =ndb.StringProperty(indexed=True, required=False)
	cnt= ndb.IntegerProperty(indexed=False, required=True)

class adQuery(ndb.Model):
	student_courses=ndb.StructuredProperty(Student_Course,repeated=True)
	cgrades= ndb.StringProperty(indexed=True,repeated = True)
	avg= ndb.IntegerProperty(indexed=True, required=True)
	ctypes = ndb.StringProperty(indexed=True,repeated = True)
	ctype_avgs=ndb.StringProperty(indexed=True,repeated = True)
	residence=ndb.IntegerProperty(indexed=True, required=True)
	availability=ndb.IntegerProperty(indexed=True, required=True)
	year=ndb.IntegerProperty(indexed=True, required=True)
	hasgit = ndb.BooleanProperty(indexed=False, required=True, default=False)
	scheduler = ndb.BooleanProperty(indexed=False, required=True, default=False)
	srchWords = ndb.StringProperty(indexed=True,repeated = True)

#end of DB class definitions

	
#function that checks student login
def checkStudentLoginExists(user_id):
	if (Student.query(user_id==Student.user_id).get()!=None):
		return True
	else:
		return False
		
#function that checks login
def checkCompanyLoginExists(user_id):
	if (Company.query(user_id==Company.user_id).get()!=None):
		return True
	else:
		return False
	
def getQuery(self,course_names,grades,average,ctypes,ctype_avgs,residence,year,availability,hasgit):
	logging.info ("GET QUERY")
	
	#server side input validation
	logging.info(str(len(grades)) + " " + str(len(course_names)) )
	if len(grades)!=len(course_names): return None
	logging.info("look here")
	for crs in course_names:
		if len(crs)>50: return None
	for grade in grades:
		if grade!="" and grade.isdigit()==False: return None
	if average!="" and average.isdigit()==False: return None
	if (len(ctypes)!=len(ctype_avgs)): return None
	if (len(ctypes) >0 and ctypes[0]!=""):
		for ctype in ctypes:
			if ctype.isdigit()==False:return None
	if (len(ctype_avgs)>0 and ctypes[0]!=""):
		for ctype_avg in ctype_avgs:
			if ctype_avg!="" and ctype_avg.isdigit()==False: return None
	if residence.isdigit()==False:return None
	
	if year.isdigit()==False: return None
	if availability.isdigit()==False: return None
	if len(hasgit)>5: return None

	#get only students who want to be found
	q=Student.query(Student.needs_job==True)
	q=q.fetch(100)
	
	#filter out unfinished signups
	p=Student.query(Student.avg>0)
	q = [val for val in p if val in q]
					
	#logging.info(q)
	
	#filter by availability
	if (int(availability)>0 and int(availability)<6):
		p=Student.query(Student.availability==int(availability))
		p=p.fetch(100)
		q = [val for val in p if val in q]
	
	#logging.info(q)
	
	#filter by hasgit
	if (hasgit=="True"):
		p=Student.query(Student.hasgit==True)
		p=pp.fetch(100)
		q = [val for val in p if val in q]
	
	#logging.info(q)
	
	#filter by year
	if (int(year)>0 and int(year)<6):
		p=Student.query(Student.year==int(year))
		p=p.fetch(100)
		q = [val for val in p if val in q]
	
	#logging.info(q)
	
	#filter by residence
	if (int(residence)>0 and int(residence)<17):
		p=Student.query(Student.residence==int(residence))
		p=p.fetch(100)
		q = [val for val in p if val in q]
		
	#logging.info(q)	
	
	#filter out student by grades in specific courses
	for i in range (0,len(grades)):	
		if grades[i]=="" :
			break
		#logging.info(i)
		#logging.info (len(grades)-1)
		grade=int(grades[i])
		course=Course.query(Course.course_name==course_names[i]).get()
		course_id=course.course_id
		logging.info(course_id)
		
		#p1=Student.query(Student.student_courses.course_id==course_id)
		p=Student.query(Student.student_courses.grade>=grade)
		p=p.fetch(100)
		p=[[val.google_id] +  val.cgrades.split("),(") for val in p]
		logging.info(p)
		p=[[p[i][0],p[i][j]] for i in range(len(p)) for j in range(1, len(p[i]))]
		logging.info(p)
		
		#filter students that have both course and grade
		p=[v[0] for v in p if \
		(''.join(c for c in v[1].split("',")[0] if c.isdigit())== \
		''.join(c for c in course_id if c.isdigit())) and\
		((int(''.join(c for c in v[1].split("',")[1] if c.isdigit()))) \
		>=grade)]
		logging.info(p)
		p1=[]
		#build list of those students
		for google_id in p:
			p1.append(Student.query(Student.google_id==google_id).get())
		
		#intersect
		q = [val for val in q if val in p1]
		logging.info(p)
		logging.info(q)
		
	#filter out by average
	if average!="":
		p=Student.query (Student.avg>=int(average))
		logging.info("MAIN AVERAGE QUERY")
		p=p.fetch(100)
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
	return q
			
def getSearchQuery(searchTerm):
	srcRes = []
	try:
		index = search.Index(INDEX_NAME)
		search_results = index.search(searchTerm)
		logging.info("completed search: " + str(search_results.number_found))
		if (search_results.number_found>0):
			for res in search_results:
				#logging.info("result: ")
				#logging.info(res.doc_id)
				srcRes.append(res.doc_id)
	except search.Error:
		logging.info("search error")
	return srcRes
	
class minGradeQuery(webapp2.RequestHandler):
	def errormsg(self):
		self.response.write (errorPage("קלט שגוי לאתר"))
	
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

		user_id = self.request.cookies.get('id')
		comp_query = Company.query(Company.user_id ==user_id).get()		
	 
		#get fields from request
		course_names=self.request.get_all('name')
		grades= self.request.get_all('grade')
		average=self.request.get('avg')	
		ctypes=self.request.get_all("ctype")
		ctype_avgs=self.request.get_all("ctype_avg")
		residence=self.request.get("residence")
		year=self.request.get("year")
		availability=self.request.get("availability")
		hasgit=self.request.get("hasgit")
		
		logging.info("grades " + str(len(grades)))
		logging.info("course " + str(len(course_names)))
		logging.info("average " + str(average))
		logging.info("ctypes " + str(len(ctypes)))
		logging.info("ctype_avgs " + str(len(ctype_avgs)))
		logging.info("residence " + str(residence))
		
		q = getQuery(self, course_names,grades,average,ctypes
		,ctype_avgs,residence,year,availability,hasgit)
		#logging.info(q)
		
		## initial code for searching module
		logging.info("trying to search")
		searchFlag = 0
		searchTerm = ''
		searchTermTry = self.request.get('searchBar')
		#logging.info(searchTermTry)
		
		# input validation and seperate words by ' '
		srcWordList = re.sub("[^\w]", " ",  searchTermTry).split()
		
		#logging.info(srcWordList)
		
		# if more than one term in search query put 'AND' between terms
		for i in range(0,len(srcWordList)):
			searchTerm += srcWordList[i]
			if (i<len(srcWordList)-1):
				searchTerm += " AND "
				
		#logging.info(searchTerm)
		
		#srcRes = []
		if (searchTerm !=''):
			searchFlag = 1
			logging.info(searchTerm)
			srcRes = getSearchQuery(searchTerm)
		
		if (searchFlag==1):
			if(srcRes==[]):
				logging.info("no search results")
				f = open("no_results_page.html")
				self.response.write(f.read())
				f.close()
				return
			elif(srcRes!=[] and (q!=None and q!=[])):
				logging.info("search res: " + str(srcRes))
				qUnion = []
				for std in q:
					#logging.info("student id: " + str(std.google_id))
					if std.google_id in srcRes:
						qUnion.append(std)
				q = qUnion
		
		#/no results
		if (q==None):
			self.errormsg()
		
		if (q==[]):
			f = open("no_results_page.html")
			self.response.write(f.read())
			f.close()
		else: #build result page
			page = buildQueryResultsPage(q,None,None,comp_query)
			self.response.write(page)
			

#adds all courses to DB from the parsed courses files
class dbBuild(webapp2.RequestHandler):
	
	def get(self):
		#add a mail to allowedCompany so it can be seen in console
		
		#ac = allowedCompany(email="tauhireteam@gmail.com")
		#ac.put()
			
		q=Student.query()
		q=q.fetch(1000)
		for st in q:
			if st.year==None: st.year=0
			if st.availability==None: st.availability=0
			if st.needs_job==None: st.needs_job=True
			if st.cnt==None: st.cnt=0
			if st.cv_view_cnt==None : st.cv_view_cnt=0
			if st.gradesheet_view_cnt==None: st.gradesheet_view_cnt=0
			
			#index CVs:
			if (st.cv_blob_key!=None):
				blob_reader = blobstore.BlobReader(st.cv_blob_key)
				#get the file text
				text = blob_reader.read()
				dbHndlr = dbHandler()
				cvPdf= StringIO(text)
				cvContent = dbHandler.convert_pdf_to_txt(dbHndlr, cvPdf)
				cvContentRev = dbHandler.reverseString(dbHndlr,cvContent)
				self.response.write(cvContentRev)
			
				srcFields = [search.TextField(name='cvContent', value=cvContentRev)]
			
				doc = search.Document(doc_id = st.google_id,fields=srcFields)
				try:
					add_result = search.Index(name=INDEX_NAME).put(doc)
				except search.Error:
					logging.info("indexing result for search has failed")
		#import csv
		
		#upload courses to db

		#with open('courses3.csv', 'rb') as csvfile:
			#spamreader = csv.reader(csvfile, delimiter=',')
			#for row in spamreader:
		 		#c=Course(course_name=row[0],course_id=row[1], course_type=int(row[2]), course_weight=int(row[3]))
		 		#c.put()

		#upload allowed companies file to db 
		
		#with open('allowedCompanies.csv', 'rb') as csvfile:
			#spamreader = csv.reader(csvfile, delimiter='\n')
			#for row in spamreader:
				#s=(str(row)[2:len(str(row))-2]).strip()
				#logging.info(s.strip())
				#a=allowedCompany(email=s)
				#a.put()
		
		#self.response.write(errorPage('Database built'))

#deletes all courses from DB	
class dbDelete(webapp2.RequestHandler):
	def get(self):
		passw=self.request.get("passw")
		if (passw=="weLoveYouGoogle2016"):
			ndb.delete_multi(Course.query().fetch(keys_only=True))
			self.response.write(errorPage('Database deleted'))
		else:
			self.response.write(errorPage('Wrong password'))
			
#deletes user	
class deleteStudent(webapp2.RequestHandler):
	def get(self):
		#validate student
		id = self.request.cookies.get('id')
		logging.info(id)
		st=Student.query(id==Student.user_id).get()
		if (st!=None):
			#remove student
			index = search.Index(name=INDEX_NAME)
			index.delete(st.google_id)
			st.key.delete()
				
		self.response.write(\
		errorPage("שם המשתמש שלך נמחק, בהצלחה בהמשך הדרך"))


class dbUserIdScramble(webapp2.RequestHandler):
	#changes all hash id's in the DB
	#the function is called using cron.yaml once a day for security reasons
	def get(self):
		passw=self.request.get("passw")
		if (passw=="weLoveYouGoogle2016"):
			#change student ids
			q=Student.query()
			for s in q:
				s.user_id=str(hashlib.sha512(s.google_id + str(time())).hexdigest())
				s.put()
			#change company ids
			q=Company.query()
			for c in q:
				c.user_id=str(hashlib.sha512(c.google_id + str(time())).hexdigest())
				c.put()
			self.response.write(errorPage('Database scrambled'))
		else:
			self.response.write(errorPage('Wrong password'))
		
#adds Student to DB
class dbHandler(webapp2.RequestHandler):

	def createStudentCourse(self, course_names, grade):
		if (len(course_names)!=len(grade)):
			self.response.write (errorPage("קלט שגוי לאתר"))
			return
		s=[]
		for i in range(0,len(course_names)):
			if (grade[i].isdigit()==False): continue
			if (int(grade[i])>100 or int(grade[i])<60) : continue
			if (len(course_names[i])>50):
				self.response.write (errorPage("קלט שגוי לאתר"))
				return
			course_query=Course.query (Course.course_name==course_names[i]).get()
			
			if course_query==None : continue
			
			#logging.info (course_query)
			s.append(Student_Course(grade=int(grade[i]), course=course_query))
		return s
	
	def convert_pdf_to_txt(self, StIO):
		rsrcmgr = PDFResourceManager()
		retstr = StringIO()
		codec = 'utf-8'
		laparams = LAParams()
		device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
		#fp = file(path, 'rb')
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		password = ""
		maxpages = 0
		caching = True
		pagenos=set()

		for page in PDFPage.get_pages(StIO, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
			interpreter.process_page(page)

		text = retstr.getvalue()

		#fp.close()
		device.close()
		retstr.close()
		return text

	def reverseString(self,str):
		rev = ''
		temp = ''
		for i in range(0,len(str)):
			if (ord(str[i])>=128):
				temp+=str[i]
			else:
				temp = temp.decode('utf-8')
				temp = temp[::-1]
				temp = temp.encode('utf-8')
					
				rev+= temp
				rev+= str[i]
				temp=''
		return rev
	
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
			if (self.checkPdfFile(cv)==False or len(cv)>3000000):
				self.response.write(errorPage("קובץ לא חוקי להעלאה"))
				return
			
			#write user's CV File into blobstore
			cv_blob_key=self.CreateFile(st.google_id,cv)
			
			
			##cvContent = ''
			##cvStr = cv.decode('utf-8', errors='ignore').encode('utf-8')
			
			cvPdf= StringIO(cv)
			cvContent = dbHandler.convert_pdf_to_txt(self, cvPdf)
			cvContentRev = dbHandler.reverseString(self,cvContent)
		
			##logging.info("whole cv: ")
			##logging.info(cvContent)
			##self.response.write (errorPage(cvContentd))
			
			srcFields = [search.TextField(name='cvContent', value=cvContentRev)]
			
			doc = search.Document(doc_id = st.google_id,fields=srcFields)
			try:
				add_result = search.Index(name=INDEX_NAME).put(doc)
			except search.Error:
				logging.info("indexing result for search has failed")
			##logging.info("indexed cv")
		elif(st.cv_blob_key!=None):
			cvKey = True
		
		
		#add courses and grades
		course_names=self.request.get_all('name')
		grade= self.request.get_all('grade')
		
		st.student_courses= dbHandler.createStudentCourse(self, course_names, grade)
		
		st.name = "demo"
		#logging.info(self.request.get('getEmailNotification'))
		
		#handle allow-emails
		if (self.request.get('getEmailNotification')=="True"):
			st.allow_emails=True
		else:
			st.allow_emails=False
		
		#handle needs_job
		logging.info("needs_job")
		logging.info(self.request.get('receiveOffers'))
		if (self.request.get('receiveOffers')=="True"):
			#invert values of checkbox
			st.needs_job=False
		else:
			st.needs_job=True
		logging.info(st.needs_job)
		
		logging.info("residence added")
		#residence validation and handling
		residence = self.request.get('residence')
		if (residence.isdigit()==False or int(residence)>16 or int(residence)<0):
			self.response.write (errorPage("קלט שגוי לאתר"))
			return
		st.residence = int(residence)
		
		logging.info("year added")
		#year validation and handling
		year = self.request.get('year')
		if (year.isdigit()==False or int(year)>4 or int(year)<0):
			self.response.write (errorPage("קלט שגוי לאתר"))
			return
		logging.info(year)
		st.year = int(year)
		
		logging.info("avail added")
		#availability validation and handling
		availability = self.request.get('availability')
		if (availability.isdigit()==False or int(availability)>2 or int(availability)<0):
			self.errormsg()
			return
		logging.info(availability)
		st.availability = int(availability)
		
		logging.info("git added")
		
		#git validation and handling
		git = self.request.get('git')
		logging.info(git)
		if (git!="" and (len(git)>60 or git.find("git")==-1)):
			self.response.write (errorPage("קלט שגוי לאתר"))
			return
		st.git = git
		
		curr_average = st.avg
		
		#average validation
		new_avg= self.request.get('average')
		if (new_avg.isdigit()==False or int(new_avg)>100 or int(new_avg)<60):
			self.response.write (errorPage("קלט שגוי לאתר"))
			return
		st.avg = int(new_avg)
		
		if (cv!=""):
			st.cv_blob_key=BlobKey(cv_blob_key)
		elif(cvKey!= True):
			st.cv_blob_key=None
		
		#logging.info(st)
		st.put()
		
		if (curr_average == -1):
			self.response.write ("""<html><script>
				window.location="StudentWelcomePage/index.html";
				</script></html>""")
		else:
			self.response.write ("""<html><script>
				window.location="/StudentOffersPage";
				</script></html>""")
	
	#server side validation that uploaded file is a pdf with text in it
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
		#saving the file in the blob store using the user's google id
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
		
#use this function for student to get his/her own CV
class deleteMyCV(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		if (checkStudentLoginExists(user_id)!=True):
			self.response.write(errorPage("גישה לא חוקית לדף"))
		else:
			st = Student.query(Student.user_id==user_id).get()
			index = search.Index(name=INDEX_NAME)
			index.delete(st.google_id)
			if (st.cv_blob_key!=None):
				blobstore.delete(st.cv_blob_key)
				st.cv_blob_key=None
				st.put()
				t.sleep(2)
			self.response.write ("""<html><script>
				window.location="studentEditPage";
				</script></html>""")

#use this function for student to get his/her own CV
class getMyCV(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		user_id = self.request.cookies.get('id')
		if (checkStudentLoginExists(user_id)!=True):
			self.response.write(errorPage("גישה לא חוקית לדף"))
		else:
			st = Student.query(Student.user_id==user_id).get()
			self.send_blob(st.cv_blob_key)

#use this function for companies to see student CVs
#get the user_id using the hashed version
class getCV(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		cv_id = self.request.get('user_id')
		user_id = self.request.cookies.get('id')
		
		#check that session is valid
		if (checkCompanyLoginExists(user_id)!=True):
			self.response.write(errorPage("גישה לא חוקית לדף"))
		else:
			company=Company.query(Company.user_id==user_id).get()
			st = Student.query(Student.user_id==cv_id).get()
			#check student id is valid
			if (st!=None):
				#if a new company is watching this cv- add it and inc counter
				if (company.email not in st.cv_viewed_by):
					st.cv_view_cnt+=1
					st.cv_viewed_by.append(company.email)
					st.put()
				self.send_blob(st.cv_blob_key)

class GradeSheetHandler(webapp2.RequestHandler):
	def get(self):
		s_id = self.request.get('user_id')
		user_id = self.request.cookies.get('id')
		if (checkCompanyLoginExists(user_id)!=True):
			self.response.write(errorPage("גישה לא חוקית לדף"))
		else:
			company=Company.query(Company.user_id==user_id).get()
			st=Student.query(Student.user_id==s_id).get()
			if (st!=None):
				logging.info("VIEWING")
				logging.info(st.gradesheet_viewed_by)
				logging.info(company.email not in st.gradesheet_viewed_by)
				if (company.email not in st.gradesheet_viewed_by):
					st.gradesheet_view_cnt+=1
					st.gradesheet_viewed_by.append(company.email)
					st.put()
					
				page = buildGradeSheetPage(st)
				self.response.write(page)
			else:
				self.response.write(errorPage("גישה לא חוקית לדף"))
