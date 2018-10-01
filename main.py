#!/usr/bin/env python

import webapp2
import json
import string
import base64
from google.appengine.api import taskqueue
from urllib import urlencode
from urlparse import urlparse
from urlparse import parse_qs
import logging
import time
import re


class MainHandler(webapp2.RequestHandler):
    params_mapping = {
        'cid': 'clientId',
        't': 'type',
        'v': 'version',
        'tid': 'tid',
        'uid': 'userId',
        'dr': 'trafficSource.referralPath',
        'sr': 'device.screenResolution',
        'vp': 'device.viewPort',
        'de': 'device.encoding',
        'sd': 'device.screenColors',
        'ul': 'device.language',
        'je': 'device.javaEnabled',
        'fl': 'device.flashVersion',
        'dl': 'page.location',
        'dt': 'page.title',
        'dh': 'page.hostname',
        'dp': 'page.pagePath',
        'ec': 'eventInfo.eventCategory',
        'ea': 'eventInfo.eventAction',
        'el': 'eventInfo.eventLabel',
        'ev': 'eventInfo.eventValue',
    }

    def process_ga_params(self, params):
        data = {}

        if 'je' in params and params['je'] == '1':
            params['je'] = True
        else:
            params['je'] = False

        parsed_url = urlparse(params['dl'])

        if 'dh' not in params or not params['dh']:
            params['dh'] = parsed_url.hostname

        if 'dp' not in params or not params['dp']:
            params['dp'] = parsed_url.path
            if parsed_url.query:
                parsed_query_string = parse_qs(parsed_url.query)

                if 'utm_source' in parsed_query_string:
                    if 'trafficSource' not in data:
                        data['trafficSource'] = {}
                    data['trafficSource']['source'] = parsed_query_string['utm_source'][0]
                    parsed_query_string.pop('utm_source', None)

                if 'utm_medium' in parsed_query_string:
                    if 'trafficSource' not in data:
                        data['trafficSource'] = {}
                    data['trafficSource']['medium'] = parsed_query_string['utm_medium'][0]
                    parsed_query_string.pop('utm_medium', None)

                if 'utm_campaign' in parsed_query_string:
                    if 'trafficSource' not in data:
                        data['trafficSource'] = {}
                    data['trafficSource']['campaign'] = parsed_query_string['utm_campaign'][0]
                    parsed_query_string.pop('utm_campaign', None)

                if 'utm_term' in parsed_query_string:
                    if 'trafficSource' not in data:
                        data['trafficSource'] = {}
                    data['trafficSource']['term'] = parsed_query_string['utm_term'][0]
                    parsed_query_string.pop('utm_term', None)

                if 'utm_content' in parsed_query_string:
                    if 'trafficSource' not in data:
                        data['trafficSource'] = {}
                    data['trafficSource']['content'] = parsed_query_string['utm_content'][0]
                    parsed_query_string.pop('utm_content', None)

                if parsed_query_string:
                    params['dp'] += '?' + urlencode(parsed_query_string)


        for key, value in self.params_mapping.iteritems():
            if key in self.request.GET:
                data = self.map_params(data, value, params[key])

        a = re.compile("^cm([1-9][0-9]*)")
        for key, value in self.request.GET.iteritems():
            res = a.match(key)
            if res:
                if 'customMetrics' not in data:
                    data['customMetrics'] = []
                data['customMetrics'].append({'index':res.group(1),'value':value})

        a = re.compile("^cd([1-9][0-9]*)")
        for key, value in self.request.GET.iteritems():
            res = a.match(key)
            if res:
                if 'customDimensions' not in data:
                    data['customDimensions'] = []
                data['customDimensions'].append({'index':res.group(1),'value':value})

        data['device']['userAgent'] = self.request.headers.get('User-Agent')
        data['timestamp'] = int(time.time())
        data['ip']=self.request.remote_addr

        return data

    def get(self):


        data = self.process_ga_params(self.request.GET)

        q = taskqueue.Queue('pull-queue')

        tasks = [taskqueue.Task(payload=json.dumps(data), method='PULL')]
        logging.info(data)
        q.add(tasks)

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'image/gif'
        self.response.write(base64.b64decode('R0lGODlhAQABAJAAAP8AAAAAACH5BAUQAAAALAAAAAABAAEAAAICBAEAOw=='))

    def map_params(self, data, key, value):
        str_arr = string.split(key, '.')

        if len(str_arr) == 2:
            if not (str_arr[0] in data):
                data[str_arr[0]] = {}
            data[str_arr[0]][str_arr[1]] = value
        else:
            data[str_arr[0]] = value

        return data


app = webapp2.WSGIApplication([
    ('/collect', MainHandler)
], debug=True)
