import webapp2

config = {'default-group' : 'base-data'}

application = webapp2.WSGIApplication([
	('/add', 'add.AddContact'),
], debug=True, config=config)