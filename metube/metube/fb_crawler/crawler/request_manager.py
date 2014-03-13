import threading
import httplib2
import codecs
import time
from time import sleep
from metube.fb_crawler.models import CrawlRequest
from metube.fb_crawler.crawler.fb import handle_facebook_id
from metube.settings import MEDIA_ROOT
from settings import APP_ID, APP_SECRET
from dateutil import parser
#from csv2pdf import csv2pdf

def manage_requests():
	# If we are working, do nothing
	if CrawlRequest.objects.filter(status="INP"):
		return	
	else:
		requests = CrawlRequest.objects.filter(status="SCH")
		if len(requests) > 0:
			request_thread = RequestHandler(requests[0].pk)
			request_thread.start()
		return

class RequestHandler(threading.Thread):
	def __init__(self, request_identifier):
		super(RequestHandler, self).__init__()
		self.request_id = request_identifier
		
	def run(self):
		# Mark request as in progress
		request = CrawlRequest.objects.get(id=self.request_id)
		
		request.status = "INP"
		request.save()

		# Perform!
		print "handling request (%s): %s" % (request.id, request.tag)
		# Get Access token
		h = httplib2.Http()
		url = 'https://graph.facebook.com/oauth/access_token?client_id='+APP_ID+'&client_secret='+APP_SECRET+'&grant_type=client_credentials'
		response, content = h.request(url)
		
		access_token = str(content).split('=')[-1]

		# Get facebook data
		options = {}
		options["access_token"] = access_token
		options["from_date"] = request.start_date
		options["to_date"] = request.end_date
		options["include_comments"] = request.include_comments
		
		result = handle_facebook_id(request.fb_id, options)

		# Write to CSV file
		filename = os.path.join(MEDIA_ROOT, "fb_crawler/[%s__%s]_%s" % (
			request.created_date.strftime("%Y_%m_%d"),
			request.created_date.strftime("%h:%M"),
			request.facebook_id,
		))
		request.filename = filename
		f = codecs.open(csv_filepath+".csv", "w", encoding="utf-8")
		f.write(result)
		f.close()

		## Generate pdf
		#pdf_name = csv2pdf(csv_filepath)
		#if pdf_name == '':
		#	print('error generating pdf')
		#else:
		#	print(pdf_name+' generated successfully')

		#request.pdf_filename = pdf_name

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
		
		print "...done!"

		# Update request status
		request.status = "COM"
		request.save()
		
		# manage more
		manage_requests()
