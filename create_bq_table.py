#!/usr/bin/env python

import webapp2
from bqloader import BQLoader


class MainHandler(webapp2.RequestHandler):
    def get(self):
        bq_loader = BQLoader()
        bq_loader.create_table()

        self.response.write('ok')




app = webapp2.WSGIApplication([
    ('/tasks/create_bq_table', MainHandler)
], debug=True)