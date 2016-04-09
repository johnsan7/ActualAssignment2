from google.appengine.ext import ndb

class Contact(ndb.Model):
	first_name = ndb.StringProperty(required=True)
	last_name = ndb.StringProperty(required=True)
	email_address = ndb.StringProperty(required=True)
	marriage_status = ndb.StringProperty()
	number_children = ndb.IntegerProperty(required=True)
	my_friend = ndb.StringProperty()
	age = ndb.IntegerProperty()
	