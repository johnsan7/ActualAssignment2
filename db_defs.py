from google.appengine.ext import ndb

class Message(ndb.Model):
	channel = ndb.StringProperty(required=True)
	date_time = ndb.DateTimeProperty(required=True)
	count = ndb.IntegerProperty(required=True)
	
class Channel(ndb.Model):
	name = ndb.StringProperty(required=True)
	classes = ndb.StringProperty(repeated=True)
	active = ndb.BooleanProperty(required=True)
	
	