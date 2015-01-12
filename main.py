# install new lib : pip install httplib2 -t /home/qgthurier/eclipse/export_bq_psa

#!/usr/bin/env python
# coding: utf8 

import metadata
import codecs
import httplib2
import logging
import os
import urllib
import webapp2
import cgi 
import csv
import json
import time

import cloudstorage 
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.appengine import AppAssertionCredentials
from oauth2client.client import OAuth2Credentials
from google.appengine.api import mail
from datetime import date, timedelta, datetime

BUCKET = "/ds-exports"
JOB_METADATA = BUCKET + "/current_job.csv"
LEFT_JOIN_REF = BUCKET + "/left_join.csv"
INFORMED = BUCKET + "/informed.csv"

BILLING_PROJECT_ID = "1011003757378" # DnaProjet2 aka singular-silo-638
BQ_PROJECT_ID = "1011003757378"

PREFIX = "ds_report_"
FINAL_TAB = "left_join_report_"
DATASET = "elce_ds_reports"

SECRET = "swhyrMAUgFX_ZzEga9qrETZe"
ID = "1011003757378-r7rurifg7jf6f6occko1ff37sbrbp57d.apps.googleusercontent.com"
TOKEN = "1/GRT4uXq-c3vAM8HDBkf4JLFt0S-JDaBNrJD22OLsJ-k"


def create_credentials(client_id, client_secret, refresh_token):
    return OAuth2Credentials(access_token=None,
                             client_id=client_id,
                             client_secret=client_secret,
                             refresh_token=refresh_token,
                             token_expiry=None,
                             token_uri='https://accounts.google.com/o/oauth2/token',
                             user_agent=None)

def upload_file_to_gcs(service, report_id, report_fragment, date):
    f = cloudstorage.open(BUCKET + "/" + report_id + "-" + date + '-report-' + report_fragment + '.csv', 'w', content_type='text/csv')
    request = service.reports().getFile(reportId=report_id, reportFragment=report_fragment)
    f.write(request.execute())
    f.close()
  
def poll_daily_report_to_gcs(service, report_id, date):
    request = service.reports().get(reportId=report_id)
    json_data = request.execute()
    while True:
        if json_data['isReportReady']:
            for i in range(len(json_data['files'])):
                upload_file_to_gcs(service, report_id, str(i), date) 
                return
        else:
            time.sleep(10)
    
def read_current_job_metadata():
    f = cloudstorage.open(JOB_METADATA, 'r')
    csv_reader = csv.reader(iter(f.readline, ''), delimiter=',', quotechar='"')
    next(csv_reader)  # skip the headers
    return next(csv_reader)
     
                
class LaunchDsJob(webapp2.RequestHandler):
  
    def initialization(self):
        generic_user_creds = create_credentials(ID, SECRET, TOKEN)
        http = generic_user_creds.authorize(http = httplib2.Http())
        self.ds_service = build('doubleclicksearch', 'v2', http=http)
        self.args = self.parse_get_parameters()    
    
    def parse_get_parameters(self):
        get = cgi.FieldStorage()
        try:
            date = get['date'].value
        except:
            yesterday =  datetime.today() - timedelta(1)
            date = yesterday.strftime('%Y-%m-%d')
        try:
            request = get['request'].value
            if request == '1':
                request = metadata.request1
                rid = '1'
            else:
                request = metadata.request2
                rid = '2'
        except:
            request = metadata.request1
            rid = '1'
        return {'date': date, 'request': request, 'rid': rid}           
    
    def get(self):         
        self.initialization()
        self.args['request']["timeRange"]["startDate"] = self.args['date']
        self.args['request']["timeRange"]["endDate"] = self.args['date']
        qry = self.ds_service.reports().request(body = self.args['request'])
        json_data = qry.execute()
        jid = json_data['id']
        f = cloudstorage.open(JOB_METADATA, 'w', content_type='text/csv')
        f.write("request,date,ds_job_id\n")
        f.write(self.args['rid'].encode('utf-8') + "," + self.args['date'].encode('utf-8') + "," + jid.encode('utf-8'))
        f.close()


class UploadToGcs(webapp2.RequestHandler):
    
    def initialization(self):
        generic_user_creds = create_credentials(ID, SECRET, TOKEN)
        http_generic_user = generic_user_creds.authorize(http = httplib2.Http())
        self.ds_service = build('doubleclicksearch', 'v2', http=http_generic_user)  
        self.job_metadata = read_current_job_metadata()   
         
    def get(self):         
        self.initialization()
        poll_daily_report_to_gcs(self.ds_service, self.job_metadata[2], self.job_metadata[1])   
      
      
class InsertIntoBq(webapp2.RequestHandler):
    
    def initialization(self):
        http_app = AppAssertionCredentials(scope='https://www.googleapis.com/auth/bigquery').authorize(httplib2.Http())
        self.bq_service = build('bigquery', 'v2', http=http_app)
        self.job_metadata = read_current_job_metadata()  
        
    def make_request_config(self, date):
        files = cloudstorage.listbucket(BUCKET + '/' + date)
        file_names = ["gs:/" + fstat.filename for fstat in files]
        logging.debug(file_names)
        logging.debug(self.job_metadata[0])
        logging.debug('gs:/' + BUCKET + '/' + self.job_metadata[2] + "-" + date )
        if self.job_metadata[0] == '1':
            schema = metadata.schema1
            logging.debug('choose schema 1')
        else:
            schema = metadata.schema2
            logging.debug('choose schema 2')
        return {
              'configuration': {
                  'load': {
                    'sourceUris': ['gs:/' + BUCKET + '/' + self.job_metadata[2] + "-" + date + '*'],
                    'schema': schema,
                    'skipLeadingRows': 1,
                    #'ignoreUnknownValues': True,
                    'destinationTable': {
                      'projectId': BQ_PROJECT_ID,
                      'datasetId': DATASET,
                      'tableId': PREFIX + self.job_metadata[0] + "_" + date.replace("-", "")
                    },
                  }
                }}
      
    def get(self):         
        self.initialization()
        job = self.bq_service.jobs().insert(projectId=BILLING_PROJECT_ID, body=self.make_request_config(self.job_metadata[1])).execute()
        f = cloudstorage.open(JOB_METADATA, 'w', content_type='text/csv')
        f.write("request,date,ds_job_id,bq_job_id\n")
        self.job_metadata.append(job['jobReference']['jobId'].encode('utf-8'))
        f.write(",".join(self.job_metadata))
        f.close()
      

class CheckBqJob(webapp2.RequestHandler):
    
    def initialization(self):
        http_app = AppAssertionCredentials(scope='https://www.googleapis.com/auth/bigquery').authorize(httplib2.Http())
        self.bq_service = build('bigquery', 'v2', http=http_app)
        self.job_metadata = read_current_job_metadata()  
        
      
    def get(self):         
        self.initialization()
        res = self.bq_service.jobs().get(projectId=BILLING_PROJECT_ID, jobId=self.job_metadata[3]).execute()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(res)
                 

class LeftJoin(webapp2.RequestHandler):
    
    def initialization(self):
        http_app = AppAssertionCredentials(scope='https://www.googleapis.com/auth/bigquery').authorize(httplib2.Http())
        self.bq_service = build('bigquery', 'v2', http=http_app)
        self.args = self.parse_get_parameters()    
    
    def parse_get_parameters(self):
        get = cgi.FieldStorage()
        try:
            date = get['date'].value
        except:
            yesterday =  datetime.today() - timedelta(1)
            date = yesterday.strftime('%Y-%m-%d')
        return {'date': date}
        
    def make_query_config(self, query):
        return {"configuration": {
                  "query": {
                    "query": query,
                    "destinationTable": {
                      "projectId": BQ_PROJECT_ID,
                      "datasetId": DATASET,
                      "tableId":  FINAL_TAB + self.args['date'].replace("-", "")
                    },
                    "useQueryCache": False,
                    "allowLargeResults": True,
                    "createDisposition": "CREATE_IF_NEEDED",
                    "writeDisposition": "WRITE_EMPTY",
                    #"priority": "BATCH"
                  }
                }}
                
    def get(self):         
        self.initialization()
        date = self.args['date'].replace("-", "")
        query = metadata.left_join_qry % (date, date)
        job = self.bq_service.jobs().insert(projectId=BILLING_PROJECT_ID, body=self.make_query_config(query)).execute()
        table = DATASET + "." + FINAL_TAB + date
        jid = job['jobReference']['jobId']
        f = cloudstorage.open(LEFT_JOIN_REF, 'w', content_type='text/csv')
        f.write("table,bq_job_id\n")
        f.write(table.encode('utf-8') + "," + jid.encode('utf-8'))
        f.close()
        self.response.out.write("join query has been launched")


class Check(webapp2.RequestHandler):
    
    def initialization(self):
        http_app = AppAssertionCredentials(scope='https://www.googleapis.com/auth/bigquery').authorize(httplib2.Http())
        self.bq_service = build('bigquery', 'v2', http=http_app)    
        self.left_join = self.read_left_join_file()
        self.emails = self.read_informed_file()
    
    def read_left_join_file(self):
        f = cloudstorage.open(LEFT_JOIN_REF, 'r')
        csv_reader = csv.reader(iter(f.readline, ''), delimiter=',', quotechar='"')
        next(csv_reader)  # skip the headers
        return next(csv_reader)
    
    def read_informed_file(self):
        f = cloudstorage.open(INFORMED, 'r')
        csv_reader = csv.reader(iter(f.readline, ''), delimiter=',', quotechar='"')
        next(csv_reader)  # skip the headers
        emails = []
        for row in csv_reader:
            emails.append(row[0])
        return emails
    
    def get(self):         
        self.initialization()
        message = mail.EmailMessage(sender="<qgthurier@netbooster.com>", subject="Status for DS daily report")
        message.to = "<" + ">,<".join(self.emails) + ">"
        message.html = "<html><head></head><body><b>DS Report Status:</b>\n"
        message.body = "DS Report Status:\n"
        res = self.bq_service.jobs().get(projectId=BILLING_PROJECT_ID, jobId=self.left_join[1]).execute()
        if "errors" in res['status'].keys():
            message.html += "Job " + self.left_join[1] + " for table " + self.left_join[0] + " has failed"
            message.body += "Job " + self.left_join[1] + " for table " + self.left_join[0] + " has failed"
        else:
            try:
                ds_id = self.left_join[0].split(".")[0]
                table_id = self.left_join[0].split(".")[1]
                table = self.bq_service.tables().get(projectId=BQ_PROJECT_ID, datasetId=ds_id, tableId=table_id).execute()
            except HttpError:
                table = None
            if not table:
                message.html += "Job " + self.left_join[1] + " for table " + self.left_join[0] + " is " + res['status']['state'] + " & report is unavailable"
                message.body += "Job " + self.left_join[1] + " for table " + self.left_join[0] + " is " + res['status']['state'] + " & report is unavailable"
            else:
                message.html += "Job " + self.left_join[1] + " for table " + self.left_join[0] + " is " + res['status']['state'] + " & report is available"
                message.body += "Job " + self.left_join[1] + " for table " + self.left_join[0] + " is " + res['status']['state'] + " & report is available"
        message.html += "\n</body></html>"
        message.send()
        self.response.out.write("email has been sent")


app = webapp2.WSGIApplication(
    [
     ('/launch_ds_job', LaunchDsJob),
     ('/upload_to_gcs', UploadToGcs),
     ('/import_into_bq', InsertIntoBq),
     ('/left_join', LeftJoin),
     ('/check', Check)
    ],
    debug=True)