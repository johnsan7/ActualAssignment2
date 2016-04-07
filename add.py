import webapp2
import os
import jinja2

from google.appengine.ext import ndb
import db_defs




JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True		
	)
	
class AddContact(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.response.write(template.render())
		