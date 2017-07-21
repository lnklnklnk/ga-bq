#!/usr/bin/env python
import webapp2
import json
import logging
from google.appengine.api import taskqueue


from bqloader import BQLoader



class MainHandler(webapp2.RequestHandler):

    def get(self):

        q = taskqueue.Queue('pull-queue')
        tasks = q.lease_tasks(30, 1000)
        logging.info(len(tasks))
        if len(tasks)>0:

            bq_loader = BQLoader()
            rows=[]

            for task in tasks:
                rows.append({'insertId': task.payload, 'json':json.loads(task.payload)})

            logging.info(rows)

            bq_loader.insert_rows(rows)
            q.delete_tasks(tasks)

        self.response.write('ok')




app = webapp2.WSGIApplication([
    ('/tasks/process_queue', MainHandler)
], debug=True)
