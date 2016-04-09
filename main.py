import webapp2

config = {'default-group' : 'base-data'}

application = webapp2.WSGIApplication([
	('/', 'add.AddContact'),
	('/view.*', 'add.ViewContact'),
	('/edit.*', 'add.EditContact'),
], debug=True, config=config)