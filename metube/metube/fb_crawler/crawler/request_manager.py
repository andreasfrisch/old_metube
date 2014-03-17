import threading
import httplib2
import codecs
import time
import logging
import os
import gobject
from time import sleep
from metube.fb_crawler.models import CrawlRequest
from metube.fb_crawler.crawler.fb import handle_facebook_id
from metube.settings import MEDIA_ROOT, CRAWLER_RESULTS
from settings import APP_ID, APP_SECRET
from dateutil import parser
#from csv2pdf import csv2pdf

gobject.threads_init()
logger = logging.getLogger("metube")

def manage_requests():
	# If we are working, do nothing
	if CrawlRequest.objects.filter(status="INP"):
		return	
	else:
		requests = CrawlRequest.objects.filter(status="SCH")
		if len(requests) > 0:
			request_thread = RequestHandler(requests[0].pk)
			request_thread.start()
			request_thread.join()
		return

class RequestHandler(threading.Thread):
	def __init__(self, request_identifier):
		super(RequestHandler, self).__init__()
		self.request_id = request_identifier
		
	def run(self):
		logger.debug("> Handling request id %s [start]" % self.request_id)
		print("1")

		# Mark request as in progress
		try:
			request = CrawlRequest.objects.get(pk=self.request_id)
		except:
			logger.error("No CrawlRequest with ID:%s found" % self.request_id)
			print("no crawl request found")
			return
		
		logger.debug(">> Found object [%s]" % request)
		print("2")
		
		request.status = "INP"
		request.save()
		
		logger.debug(">> request status INP")
		print("3")

		# Perform!
		# Get Access token
		response, content = httplib2.Http(".cache").request(
				"https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials" % (APP_ID, APP_SECRET),
				"GET"
		)
		access_token = str(content).split('=')[-1]
		logger.debug(">> got access_token: %s" % access_token)
		print("4")

		# Get facebook data
		options = {}
		options["access_token"] = access_token
		options["from_date"] = request.from_date
		options["to_date"] = request.to_date
		options["include_comments"] = request.include_comments
		
		logger.debug(">> handle facebook id [start]")
		print("5")
		
		result = handle_facebook_id(request.facebook_id, options)
		
		logger.debug(">> handle facebook id [end]")
		print("6")

		# Write to CSV file
		filename = "[%s__%s]_%s" % (
				request.created_date.strftime("%Y_%m_%d"),
				request.created_date.strftime("%H:%M"),
				request.facebook_id,
		)
		
		logger.debug(">> created filename: %s" % filename)
		print("7")
		
		request.filename = filename
		f = codecs.open(os.path.join(MEDIA_ROOT, "%s/%s.%s" % (CRAWLER_RESULTS, filename, "csv")), "w", encoding="utf-8")
		f.write(result)
		f.close()
		
		logger.debug(">> wrote to file: %s" % filename+".csv")
		print("8")

		# Generate pdf
		if request.generate_pdf:
			try:
				csv2pdf(csv_filepath)
			except:
				print('error generating pdf')
				logger.error("Could not generate PDF")

		## Mail:
		##if user requested mail
		#if (options['send_mail']):
		#	#available_files = []
		#	available_files = ["tmp/"+options['filename'],pdf_name]
		#	print('>>Sending mail to: '+options['user_mail']+'...')
		#	mail(options['user_mail'],
		#		"PolSoc: requested data response",
		#		self.generate_mail(options, available_files),
		#		[]#["tmp/"+options['filename']]#,pdf_name]
		#	)
		#	print('>>...done!')

		# Update request status
		request.status = "COM"
		request.save()
		
		logger.debug(">> request status COM")
		logger.debug("> request handler [done]")
		print("9")
		
		# manage more
		manage_requests()
