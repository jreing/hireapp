import cgi
import urllib
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
  </body>
</html>
"""



class Author(ndb.Model):
	identity = ndb.StringProperty(indexed=False)



class Message(ndb.Model):
	sender = ndb.StructuredProperty(Author)
	#receiver = ndb.StructuredProperty(Author)
	receiver = ndb.StringProperty(indexed=False)
	cont = ndb.StringProperty(indexed=False)

class appUser(ndb.Model):
	usr = ndb.UserProperty(required=True)
	identity = ndb.StringProperty(indexed=False)

class MainPage(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
			self.response.write('Hello, ' + user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))
			
		mess_query = Message.query()
		
		for message in mess_query:
			if(message.receiver == users.get_current_user().nickname()):
				self.response.write('<p>%s</p>' %message.cont)
		self.response.write(MAIN_PAGE_HTML)
	
class Guestbook(webapp2.RequestHandler):
	def post(self):
	
		self.message = Message(cont = self.request.get('mess'))
		
		destAdd = self.request.get('recv') + "@example.com"
		#destId = users.User(destAdd)
		
		#destIdKey = destId.put()
		#destIdVal = destIdKey.get()
		#self.key = appUser(usr=destId).put()
		#self.rec = self.key.get()
		
		self.message.receiver = destAdd
		if users.get_current_user():
			self.message.sender = Author(identity=users.get_current_user().user_id())
		
		self.message.put()
		self.response.write('<html><body>message entered<pre>')
		self.response.write('</pre></body></html>')
		
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/sign', Guestbook),
	], debug=True)