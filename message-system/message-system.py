import cgi
import urllib
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

MAIN_PAGE_HTML = """\
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


#class Thread(ndb.Model):
#	owner = ndb.

#class appUser(ndb.Model):
	#usr = ndb.UserProperty(required=True)
	#identity = ndb.StringProperty(indexed=False)

class MainPage(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
			self.response.write('Hello, ' + user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))
		conv_query = Conversation.query()	
		#mess_query = Message.query()
		self.response.write(MAIN_PAGE_HTML)
		for conver in conv_query:
			for message in conver.message:
				if(message.receiver == users.get_current_user().nickname()):
					send = users.User(_user_id = message.sender.identity)
					self.response.write('<p>recieved: %s</p>' %message.date)
					self.response.write('<p>from: %s</p>' %send.nickname())
					self.response.write('<p>%s</p><br>' %message.cont)
					self.response.write('<div><a href="/replay?%s">replay</a></div>' %conver.id)
		
	
class Guestbook(webapp2.RequestHandler):
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

class Replay(webapp2.RequestHandler):
	def get(self):
		self.response.write(MAIN_PAGE_HTML)
		
	def post(self):
		self.message = Message(cont = self.request.get('mess'))
		
		
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', Guestbook),
	('/replay', Replay),
	], debug=True)