#-*- coding: utf8 -*-
import httplib2
import json
from dateutil import parser

def handle_comments(post_identifier, options):
	done = False
	page = 0
	pageLimit = 200
	
	comments = [] #storing comments for sorting

	while not done:
		h = httplib2.Http()
		url = "https://graph.facebook.com/{facebook_identifier}/comments?access_token={access_token}&limit={limit}&offset={offset}&filter=toplevel&fields=from,message,comments.limit(0),like_count,created_time".format(
					facebook_identifier = post_identifier,
					access_token = options["access_token"],
					limit = pageLimit,
					offset = page*pageLimit,
				)
		response, content = h.request(url)
		post_page = json.loads(content, "utf-8")
			#	.replace("false", "False")
			#	.replace("true", "True")
			#)
		if not "data" in post_page:
			done = True
			break
		if post_page["data"] == []:
			done = True
			break
		for comment in post_page['data']:
			if "created_time" in comment:
				comments.append((comment['created_time'],comment))	
		page += 1

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
			print ">>> Error in post:"
			print post
			print "<<<"
		return_text += '%s\n' % comment_string #reverses comment order

	return len(comments), return_text

def get_likes(post_identifier, options):
	h = httplib2.Http()
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
	post_datetime = parser.parse(post["created_time"])
	comment_amount, comment_string = u"n/a", ""
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
		elif "story" in post:
			post_string += u"\"%s\"" % post["story"].replace('"',"'").replace("\n"," ") # text
	except:
		print ">>> Error in post:"
		print post
		print "<<<"
	post_string += u"\n"
	post_string += comment_string
	return post_string


def handle_facebook_id(facebook_id, options):
	result_string = ""
	if facebook_id is not "":
		h = httplib2.Http()
		done = False
		page = 0
		pageLimit = 200
		#url = 'https://graph.facebook.com/' + str(facebook_id) + \
		#		'/posts?access_token=' + opt_dict['access_token']
				#+ '&filter=toplevel&fields=from,message,comments.limit(0),like_count,created_time'
		while not done:
			url = "https://graph.facebook.com/" + str(facebook_id) + "/posts" \
					+ "?access_token=" + options["access_token"] \
					+ "&limit=" + str(pageLimit)\
					+ "&offset=" + str(page*pageLimit)
			response, content = h.request(url)
			#post_page = content.decode(encoding="utf-8")
			post_page = json.loads(content, "utf-8")
				#	.replace("false", "False")
				#	.replace("true", "True")
				#)
			if "data" in post_page:
				for post in post_page["data"]:
					post_created_time = parser.parse(post["created_time"]).date()
					if post_created_time < options["from_date"]:
						done = True
						continue
					if post_created_time > options["from_date"] \
							and post_created_time < options["to_date"]:
						result_string += handle_facebook_post(post, options)
				page += 1
			else:
				done = True
				continue
	return result_string
