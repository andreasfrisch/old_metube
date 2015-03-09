from django.db import models
from django.forms import ModelForm
from datetime import datetime

class CrawlRequest(models.Model):
	# request meta options
	SCHEDULED = "SCH"
	IN_PROGRESS = "INP"
	COMPLETED = "COM"
	ERROR = "ERR"
	STATUS_CHOICES = (
			(SCHEDULED, "Scheduled"),
			(IN_PROGRESS, "In progress"),
			(COMPLETED, "Completed"),
			(ERROR, "Error")
	)
	created_date = models.DateTimeField(default=datetime.now())
	status = models.CharField(
			max_length=3,
			choices=STATUS_CHOICES,
			default=SCHEDULED
	)
	filename = models.CharField(max_length=200, null=True, blank=True)

	# request options
	tag = models.CharField(max_length=50, null=True, blank=True)
	facebook_id = models.CharField(max_length=50)
	from_date = models.DateField()
	to_date = models.DateField()

	include_comments = models.BooleanField(default=True)
	#todo: further inclusion options

	generate_pdf = models.BooleanField(default=True)
	
	def __unicode__(self):
		return "%s [%s - %s]" % (self.tag, self.created_date, self.facebook_id)

class CrawlRequestForm(ModelForm):
	error_css_class = "form_error"
	required_css_class = "form_required"

	class Meta:
		model = CrawlRequest
		fields = [
			"created_date",
			"tag",
			"facebook_id",
			"from_date",
			"to_date",
			"include_comments",
			"generate_pdf",
		]
