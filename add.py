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
	template_variables = {}
	
	def get(self):
		self.template_variables = {}
		template = JINJA_ENVIRONMENT.get_template('add.html')

		if self.request.get('error'):
			ecode = self.request.get('error')
			if ecode=='fname':
				self.template_variables['error_code'] = [{'error':'You did not enter a first name, no changes made'}]
			elif ecode=='lname':
				self.template_variables['error_code'] = [{'error':'You did not enter a last name, no changes made'}]
			elif ecode=='email':
				self.template_variables['error_code'] = [{'error':'You did not enter an email, no changes made'}]
			elif ecode=='numchild':
				self.template_variables['error_code'] = [{'error':'You did not enter a number of children, no changes made'}]
				
				

		self.template_variables['current_contacts'] = [{'firstname':m.first_name, 'lastname':m.last_name,'key':m.key.urlsafe()} for m in db_defs.Contact.query(ancestor=ndb.Key(db_defs.Contact, self.app.config.get('default-group'))).fetch()]
		self.response.write(template.render(self.template_variables))
		
	def post(self):
		self.template_variables = {}
		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.template_variables

		if self.request.get('fname')=="":
			self.redirect('/?error=fname')
		elif self.request.get('lname')=="":
			self.redirect('/?error=lname')
		elif self.request.get('email')=="":
			self.redirect('/?error=email')			
		elif self.request.get('numchild')=="":
			self.redirect('/?error=numchild')
		else:		
			newKey = ndb.Key(db_defs.Contact, self.app.config.get('default-group'))
			
			nCon = db_defs.Contact(parent=newKey)
			nCon.first_name = self.request.get('fname')
			nCon.last_name = self.request.get('lname')
			nCon.email_address = self.request.get('email')
			nCon.marriage_status = str(self.request.get('married'))
			nCon.my_friend = self.request.get('whofriend')
			nCon.number_children = int(self.request.get('numchild'))
			nCon.age = int(self.request.get('age'))
			nCon.put()
			
			self.redirect('/')
		
#We have the id in the url with the get request. So now we just
#extract it, and change it back to a key, then get the item with that key
#and render our template. 		

class ViewContact(webapp2.RequestHandler):
	
	template_variables = {}
	
	def get(self):				
		template = JINJA_ENVIRONMENT.get_template('view.html')
		unSafeKey = ndb.Key(urlsafe=self.request.get('key'))
		tempCont = unSafeKey.get()
		
		if self.request.get('error'):
			ecode = self.request.get('error')
			if ecode=='fname':
				self.template_variables['error_code'] = [{'error':'You did not enter a first name, no changes made'}]
			elif ecode=='lname':
				self.template_variables['error_code'] = [{'error':'You did not enter a last name, no changes made'}]
			elif ecode=='email':
				self.template_variables['error_code'] = [{'error':'You did not enter an email, no changes made'}]
			elif ecode=='numchild':
				self.template_variables['error_code'] = [{'error':'You did not enter a number of children, no changes made'}]
			elif ecode=='changesmade':
				self.template_variables['error_code'] = [{'error':'Your changes were applied to this contact'}]
			elif ecode=='nochangesmade':
				self.template_variables['error_code'] = [{'error':'You did not enter any changes, so the contact was not updated'}]				

		self.template_variables['cur_con_data'] = [{'unsafekey':unSafeKey.id(), 'firstname':tempCont.first_name, 'lastname':tempCont.last_name, 'email':tempCont.email_address, 
		'marriagestatus':tempCont.marriage_status, 'numberchildren':tempCont.number_children, 'myfriend':tempCont.my_friend, 'age':tempCont.age}]	
		self.response.write(template.render(self.template_variables))
		
class EditContact(webapp2.RequestHandler):
	
	template_variables = {}

	
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		unSafeKey = ndb.Key(urlsafe=self.request.get('key'))
		tempCont = unSafeKey.get()
				
		self.template_variables['cur_con_data'] = [{'unsafekey':unSafeKey.id(), 'firstname':tempCont.first_name, 'lastname':tempCont.last_name, 'email':tempCont.email_address, 
		'marriagestatus':tempCont.marriage_status, 'numberchildren':tempCont.number_children, 'myfriend':tempCont.my_friend, 'age':tempCont.age, 'key':self.request.get('key')}]	
		self.response.write(template.render(self.template_variables))
		
	def post(self):
		self.template_variables = {}
		template = JINJA_ENVIRONMENT.get_template('add.html')
		changeMade = 0					#bool to store if any changes were made
		#urlSafeKey = ndb.Key(urlsafe=self.request.get('editkey'))
		
		if self.request.get('fname')=="":
			self.redirect('/?error=fname&key=' + self.request.get('editkey')) #This should feed back the key sent with the form as a hidden field
		elif self.request.get('lname')=="":
			self.redirect('/?error=lname&key=' + self.request.get('editkey'))
		elif self.request.get('email')=="":
			self.redirect('/?error=email&key=' + self.request.get('editkey'))			
		elif self.request.get('numchild')=="":
			self.redirect('/?error=numchild&key=' + self.request.get('editkey'))
		else:		
			unSafeKey = ndb.Key(urlsafe=self.request.get('editkey'))
			tempCont = unSafeKey.get()								#Gets our entity to edit, all forms are confirmed to have data that need to so we can just make the change

		
			if self.request.get('fname') and tempCont.first_name != self.request.get('fname'):
				tempCont.first_name = self.request.get('fname')
				changeMade = 1
			if self.request.get('lname') and tempCont.last_name != self.request.get('lname'):
				tempCont.last_name = self.request.get('lname')
				changeMade = 1
			if self.request.get('email') and tempCont.email_address != self.request.get('email'):
				tempCont.email_address = self.request.get('email')
				changeMade = 1
			if self.request.get('married') and tempCont.marriage_status != self.request.get('married'):
				tempCont.marriage_status = self.request.get('married')
				changeMade = 1
			if self.request.get('numchild') and tempCont.number_children != int(self.request.get('numchild')):
				tempCont.number_children = int(self.request.get('numchild'))
				changeMade = 1
			if self.request.get('myfriend') and tempCont.my_friend != self.request.get('myfriend'):
				tempCont.my_friend = self.request.get('myfriend')
				changeMade = 1
			if self.request.get('age') and tempCont.age != int(self.request.get('age')):
				tempCont.age = int(self.request.get('age'))
				changeMade = 1				
			tempCont.put()
			if changeMade:
				self.redirect('/edit?error=changesmade&key=' + self.request.get('editkey'))
			else:
				self.redirect('/edit?error=nochangesmade&key=' + self.request.get('editkey'))
			

	

	