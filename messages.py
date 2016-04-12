import cgi
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import logging

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
	compName = ndb.StringProperty(indexed=False)
	jobName = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class Conversation(ndb.Model):
	id = ndb.IntegerProperty(indexed = False)
	message = ndb.StructuredProperty(Message, repeated=True)	
	
class MessageHandler(webapp2.RequestHandler):
    def get(self):

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
	def post(self):
		#self.conNum = threadNum(num=0)
		#self.conNum.put()
		
	
		
		recList = self.request.get_all('studentselect') 
		destAdd = self.request.get('recv') + "@example.com"
		#destId = users.User(destAdd)
		logging.info(len(recList))
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
			self.message.date = datetime.datetime.now()
			userid = self.request.cookies.get('id')
			self.message.sender = Author(identity = userid)
			#if users.get_current_user():
				#self.message.sender = Author(identity=users.get_current_user().user_id())
			
			self.conversation.message = [self.message]
		
			#conNum = threadNum.query().get()
			#self.conversation.id = conNum.num
			#conNum.num +=1
			#conNum.put()
			self.conversation.put()
			self.message.put()

		

		self.response.write('<html><body>message entered<pre>')
		self.response.write('</pre></body></html>')

class MessageReply(webapp2.RequestHandler):
	def get(self):
		self.response.write(MESSAGE_PAGE_HTML)
		
	def post(self):
		self.message = Message(cont = self.request.get('mess'))

