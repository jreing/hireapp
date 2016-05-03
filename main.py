#!/usr/bin/env python
import cgi
import urllib
import datetime
import logging


from google.appengine.api import users
from google.appengine.ext import ndb
#from oauth2client.client import flow_from_clientsecrets
#from oauth2client import client, crypt
from google.appengine.api import oauth

import webapp2
logging.getLogger().setLevel(logging.INFO)
logging.warning("CHECK")
from db import *
from messages import *


#end of DB class definitions
#
#
#classes for actions:


class CompanyHandler(webapp2.RequestHandler):
	def get(self):
		cours_query = Course.query()
		page = buildCompanyQuery(cours_query)
		self.response.write(page)
		#f = open("companyQueryFormPage\index.html") 
		#self.response.charset="unicode"
		#self.response.write(f.read())
		#f.close()               

class tokenSignIn(webapp2.RequestHandler):
	def post(self):
		logging.info("enter token sign in")
		userid=self.request.get('user_id')
		email=self.request.get('email')
		isStudent = self.request.get('isStudent')
		
		if (isStudent == 'true'):
			user_query = Student.query(Student.id==userid).get()
			if (user_query == None):
				s = []
				st= Student(student_courses=s,id=userid, name="", city="",avg=-1)
				st.put()
				self.response.write('<html><br><br>userId: ' + userid)
		elif(isStudent == 'false'):
			user_query = Company.query(Company.id==userid).get()
			logging.info(user_query)
			if (user_query == None):
				cmp= Company(id=userid, name="", city="")
				cmp.put()
		
		self.response.set_cookie("id", userid)
		

	
class LoginHandler(webapp2.RequestHandler):
	def get(self):
		f = open("chooseEmployOrStudentPage/index.html") 
		logging.info("LOGIN HANDLER")
		self.response.write(f.read())
		f.close() 

class MainHandler(webapp2.RequestHandler):
	def get(self):
		cours_query = Course.query()
		page = buildStudentInputPage(cours_query)
		self.response.write(page)
		#f = open("studentInputPage/index.html") 
	#self.response.charset="unicode"
	#self.response.write(f.read())
	#f.close()        

class ResultsPage(webapp2.RequestHandler):
	def get(self):
		f = open("companyQueryResultsPage/index.html")
		self.response.write(f.read())
		f.close()
		
class LogInForBarak(webapp2.RequestHandler):
	def get(self):
		logging.info('LogInForBarak START')
		f = open("index.html")
		self.response.write(f.read())
		f.close()

class FirstPage(webapp2.RequestHandler):
	def get(self):
		self.response.write ("""<html><script>
			window.location="chooseEmployOrStudentPage/index.html";
			</script></html>""")

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		f = open("StudentWelcomePage/index.html") 
		self.response.write(f.read())
		f.close()

class StudentHandler(webapp2.RequestHandler):
	def get(self):
		userid = self.request.cookies.get('id')
		#logging.info(userid)
		st = Student.query(Student.id==userid).get()
		if (st.avg == -1):
			self.response.write ("""<html><script>
				window.location="/studentInputPage";
				</script></html>""")
		else:
			self.response.write ("""<html><script>
				window.location="/StudentOffersPage";
				</script></html>""")



class fileTest(webapp2.RequestHandler):
	def get(self):
		bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Demo GCS Application running from Version: '+ os.environ['CURRENT_VERSION_ID'] + '\n')
		self.response.write('Using bucket name: ' + bucket_name + '\n\n')
		bucket = '/' + bucket_name
		filename = bucket + '/demo-testfile'

		self.tmp_filenames_to_clean_up = []

		try:
			self.create_file(filename)
			self.response.write('\n\n')

			self.read_file(filename)
			self.response.write('\n\n')

			self.stat_file(filename)
			self.response.write('\n\n')

			self.create_files_for_list_bucket(bucket)
			self.response.write('\n\n')

			self.list_bucket(bucket)
			self.response.write('\n\n')

			self.list_bucket_directory_mode(bucket)
			self.response.write('\n\n')

		except Exception, e:
			logging.exception(e)
			self.delete_files()
			self.response.write('\n\nThere was an error running the demo! ','Please check the logs for more details.\n')

		else:
			self.delete_files()
			self.response.write('\n\nThe demo ran successfully!\n')
	  
	def create_file(self, filename):
		"""Create a file.

		The retry_params specified in the open call will override the default
		retry params for this particular file handle.

		Args:
		  filename: filename.
		"""
		self.response.write('Creating file %s\n' % filename)

		write_retry_params = gcs.RetryParams(backoff_factor=1.1)
		gcs_file = gcs.open(filename,'w',content_type='text/plain',options={'x-goog-meta-foo': 'foo','x-goog-meta-bar': 'bar'},retry_params=write_retry_params)
		gcs_file.write('abcde\n')
		gcs_file.write('f'*1024*4 + '\n')
		gcs_file.close()
		self.tmp_filenames_to_clean_up.append(filename)

	def read_file(self, filename):
		self.response.write('Abbreviated file content (first line and last 1K):\n')

		gcs_file = gcs.open(filename)
		self.response.write(gcs_file.readline())
		gcs_file.seek(-1024, os.SEEK_END)
		self.response.write(gcs_file.read())
		gcs_file.close()

	def stat_file(self, filename):
		self.response.write('File stat:\n')

		stat = gcs.stat(filename)
		self.response.write(repr(stat))

	def create_files_for_list_bucket(self, bucket):
		self.response.write('Creating more files for listbucket...\n')
		filenames = [bucket + n for n in ['/foo1', '/foo2', '/bar', '/bar/1','/bar/2', '/boo/']]
		for f in filenames:
			self.create_file(f)

	def delete_files(self):
		self.response.write('Deleting files...\n')
		for filename in self.tmp_filenames_to_clean_up:
			self.response.write('Deleting file %s\n' % filename)
			try:
				gcs.delete(filename)
			except gcs.NotFoundError:
				pass

app = webapp2.WSGIApplication([
	('/dbDelete', dbDelete),
	('/dbBuild', dbBuild),
	('/studentInputPage', MainHandler),
	('/StudentWelcomePage/index.html', WelcomeHandler),	
	('/studenthandler', StudentHandler),
	('/tokenSignIn', tokenSignIn),
	('/chooseEmployOrStudentPage/index.html', LoginHandler),
	('/dbHandler', dbHandler),
	('/companyQueryFormPage', CompanyHandler),
	('/companyQueryResultsPage' , minGradeQuery),
	('/StudentOffersPage', MessageHandler),
	('/messageSend', MessageSend),
	('/messageReply', MessageReply),
	('/fileTest', fileTest),
	('/getMyCV', getMyCV),
	('/getCV', getCV),
	('/', LogInForBarak)
	], debug=True)


