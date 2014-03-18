from django.db import models
from django import forms
from django.template.defaultfilters import slugify
from datetime import datetime

class Blog(models.Model):
	# author
	date = models.DateTimeField(default=datetime.now())
	title = models.CharField(max_length=200)
	slug = models.SlugField(editable=False)
	content = models.TextField()

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id:
			# If new object, create slug
			self.slug = slugify(self.title)
		super(Blog, self).save(*args, **kwargs)

class BlogForm(forms.ModelForm):
	error_css_class = "form_error"
	required_css_class = "form_required"

	class Meta:
		model = Blog
		fields = [
			"title",
			"content",
		]
