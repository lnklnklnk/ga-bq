from oauth2client.appengine import AppAssertionCredentials
import httplib2
from apiclient import discovery
import logging

class BQLoader():
    project_id = ''
    dataset_id = 'test'
    table_id = 'gadatapy4'

    table_schema= [
        {
            "name": "clientId",
            "type": "STRING"
        },
        {
            "name": "type",
            "type": "STRING"
        },
        {
            "name": "version",
            "type": "STRING"
        },
        {
            "name": "tid",
            "type": "STRING"
        },
        {
            "name": "userId",
            "type": "STRING"
        },
        {
            "name": "referer",
            "type": "STRING"
        },
        {
            "name": "ip",
            "type": "STRING"
        },
        {
            "name": "timestamp",
            "type": "INTEGER"
        },
        {
            "name": "device",
            "type": "RECORD",
            "fields": [
                {
                    "name": "screenResolution",
                    "type": "STRING"
                },
                {
                    "name": "viewPort",
                    "type": "STRING"
                },
                {
                    "name": "encoding",
                    "type": "STRING"
                },
                {
                    "name": "screenColors",
                    "type": "STRING"
                },
                {
                    "name": "language",
                    "type": "STRING"
                },
                {
                    "name": "javaEnabled",
                    "type": "BOOLEAN"
                },
                {
                    "name": "flashVersion",
                    "type": "STRING"
                },
                {
                    "name": "userAgent",
                    "type": "STRING"
                }
            ]
        },
        {
            "name": "page",
            "type": "RECORD",
            "fields": [
                {
                    "name": "location",
                    "type": "STRING"
                },
                {
                    "name": "title",
                    "type": "STRING"
                },
                {
                    "name": "pagePath",
                    "type": "STRING"
                },
                {
                    "name": "hostname",
                    "type": "STRING"
                }
            ]
        },
        {
            "name": "trafficSource",
            "type": "RECORD",
            "fields": [
                {
                    "name": "referralPath",
                    "type": "STRING"
                },
                {
                    "name": "campaign",
                    "type": "STRING"
                },
                {
                    "name": "source",
                    "type": "STRING"
                },
                {
                    "name": "medium",
                    "type": "STRING"
                }
            ]
        },
        {
            "name": "eventInfo",
            "type": "RECORD",
            "fields": [
                {
                    "name": "eventCategory",
                    "type": "STRING"
                },
                {
                    "name": "eventAction",
                    "type": "STRING"
                },
                {
                    "name": "eventLabel",
                    "type": "STRING"
                },
                {
                    "name": "eventValue",
                    "type": "INTEGER"
                }
            ]
        },
        {
            "name": "customDimensions",
            "type": "RECORD",
            "mode": "REPEATED",
            "fields": [
                {
                    "name": "index",
                    "type": "INTEGER"
                },
                {
                    "name": "value",
                    "type": "STRING"
                }
            ]
        },
        {
            "name": "customMetrics",
            "type": "RECORD",
            "mode": "REPEATED",
            "fields": [
                {
                    "name": "index",
                    "type": "INTEGER"
                },
                {
                    "name": "value",
                    "type": "STRING"
                }
            ]
        }
    ]

    def __init__(self):
        credentials = AppAssertionCredentials(
            'https://www.googleapis.com/auth/bigquery'
        )
        self.http = credentials.authorize(httplib2.Http())
        self.bigquery = discovery.build('bigquery', 'v2', http=self.http)
    def insert_rows(self,rows,stop_recursion = False):

        body = {"rows":rows}

        response = self.bigquery.tabledata().insertAll(
            projectId=self.project_id,
            datasetId=self.dataset_id,
            tableId=self.table_id,
            body=body).execute()

        # TODO add response check

    def create_table(self):
        table_ref = {'tableId': self.table_id,
                     'datasetId': self.dataset_id,
                     'projectId': self.project_id}
        table = {'tableReference': table_ref, 'schema':{'fields':self.table_schema}}

        table = self.bigquery.tables().insert(
            body=table, datasetId=self.dataset_id, projectId=self.project_id).execute()
        logging.info(table)