#-*- coding: utf8 -*-
import httplib2
import json
from dateutil import parser
import logging

logger = logging.getLogger("metube")

def handle_comments(post_identifier, options):
	logger.debug("Getting comments for post: %s" % post_identifier)
	done = False
	pageLimit = 200
	
	comments = [] #storing comments for sorting
	url = "https://graph.facebook.com/{facebook_identifier}/comments?access_token={access_token}&limit={limit}&filter=toplevel&fields=from,message,comments.limit(0),like_count,created_time".format(
				facebook_identifier = post_identifier,
				access_token = options["access_token"],
				limit = pageLimit
	)
	response, content = httplib2.Http(".cache", disable_ssl_certificate_validation=True).request(url)
	post_page = json.loads(content, "utf-8")

	while not done:
		if not "data" in post_page:
			done = True
			break
		if post_page["data"] == []:
			done = True
			break
		for comment in post_page['data']:
			if "created_time" in comment:
				comments.append((comment['created_time'],comment))	
		if "paging" in post_page:
			url = post_page["paging"]["next"]
			response, content = httplib2.Http(".cache", disable_ssl_certificate_validation=True).request(url)
			post_page = json.loads(content, "utf-8")
		else:
			done = True
			break

	##sorting comments by timestamp
	#comments.sort(key=lambda tup: tup[0])

	return_text = ""
	for timestamp, comment_object in comments:
		comment_string = "comment,"
		
		comment_string += "%s," % comment_object["from"]["name"]
		comment_string += "%s," % comment_object["from"]["id"]
		comment_datetime = parser.parse(comment_object["created_time"])
		comment_string += u"%s," % comment_datetime.time() # time (hour)
		comment_string += u"%s," % comment_datetime.date() # time (date)
		comment_string += "%s," % comment_object["like_count"]
		comment_string += "," #todo: comments_count?
		try:
			comment_string += "\"%s\"," % comment_object["message"] \
					.replace('"',"'") \
					.replace("\n"," ") \
					.replace("\r"," ")
		except:
			comment_string += ","
			print ">>> Error in comment"
			#print post
			#print "<<<"
		return_text += '%s\n' % comment_string #reverses comment order

	return len(comments), return_text

def get_likes(post_identifier, options):
	logger.debug("Getting likes for post: %s" % post_identifier)
	h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
	url = "https://graph.facebook.com/" + post_identifier + "/likes" \
		+ "?access_token=" + options["access_token"] \
		+ "&summary=1"
	response, content = h.request(url)
	post_page = eval(
			content
			.replace("false", "False")
			.replace("true", "True")
		)
	if "summary" in post_page:
		return "%s" % post_page["summary"]["total_count"]
	else:
		return "n/a"

def handle_facebook_post(post, options):
	logger.debug("Handle post: %s" % post)
	post_datetime = parser.parse(post["created_time"])
	comment_amount, comment_string = u"n/a", u""
	if options["include_comments"]:
		comment_amount, comment_string = handle_comments(post['id'], options)
	else:
		comment_amount, comment_string = u"n/a", u""
	post_string = u""
	post_string += u"Facebook," # type
	post_string += u"%s," % post['from']['name']# name
	post_string += u"," # allow for id on comments
	post_string += u"%s," % post_datetime.time() # time (hour)
	post_string += u"%s," % post_datetime.date() # time (date)
	post_string += u"%s," % get_likes(post["id"], options) # likes
	post_string += u"%s," % comment_amount # comments
	try:
		if "message" in post:
			post_string += u"\"%s\"" % post["message"].replace('"',"'").replace("\n"," ") # text
			#print(post["message"])
		elif "story" in post:
			post_string += u"\"%s\"" % post["story"].replace('"',"'").replace("\n"," ") # text
	except:
		print ">>> Error in post"
	post_string += u"\n"
	post_string += comment_string
	return post_string


def handle_facebook_id(facebook_id, options):
	result_string = ""
	if facebook_id is not "":
		done = False
		pageLimit = 200
		url = "https://graph.facebook.com/%s/posts?access_token=%s&limit=%s" % (
				str(facebook_id),
				options["access_token"],
				str(pageLimit),
		)
		post_page = json.loads(content, "utf-8")
			.replace("false", "False")
			.replace("true", "True")
		)
		while not done:
			print(">>> not done yet")
			if "data" in post_page:
				print(">>>>\t post has data")
				if post_page["data"] == []:
					print("ERROR >>>>\tERROR: data is empty <<< ERROR")
					done = True
					continue
				for post in post_page["data"]:
					post_created_time = parser.parse(post["created_time"]).date()
					if post_created_time < options["from_date"]:
						done = True
						continue
					if post_created_time > options["from_date"] \
							and post_created_time < options["to_date"]:
						result_string += handle_facebook_post(post, options)
				if "paging" in post_page:
					url = post_page["paging"]["next"]
					response, content = httplib2.Http(
							".cache",
							disable_ssl_certificate_validation = True
					).request(url, "GET")
					post_page = json.loads(content, "utf-8")
				else:
					print("ERROR >>>>\tERROR: no paging <<< ERROR")
					done = True
					continue
			else:
				done = True
				continue
		print(">>> done!")
	return result_string
