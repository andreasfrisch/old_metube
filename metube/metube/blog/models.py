from django.db import models
from django import forms
from django.template.defaultfilters import slugify
from datetime import datetime

#
# Models
#
class Tag(models.Model):
	title = models.CharField(max_length=50)

	def __unicode__(self):
		return self.title


class Blog(models.Model):
	# author
	date = models.DateTimeField(default=datetime.now())
	title = models.CharField(max_length=200)
	slug = models.SlugField()
	content = models.TextField()
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id:
			# If new object
			# create slug, test for availability, cope with existing slugs
			new_slug = slugify(self.title)
			temp_slug = new_slug
			done_testing = False
			counter = 1 # we want the first increase to go to '2'
			while not done_testing:
				try:
					# If slug is already used
					_ = Blog.objects.get(slug=temp_slug)
					counter += 1
					temp_slug = "%s-%d" % (new_slug, counter)
				except:
					done_testing = True
			self.slug = temp_slug
		super(Blog, self).save(*args, **kwargs)
	
	class Meta:
		ordering = ("date",)


#
# Forms 
#
class BlogForm(forms.ModelForm):
	error_css_class = "form_error"
	required_css_class = "form_required"

	tags = forms.ModelMultipleChoiceField(
			queryset=Tag.objects.all(),
			widget=forms.CheckboxSelectMultiple(),
			required=True
	)

	class Meta:
		model = Blog
		fields = [
			"title",
			"tags",
			"content",
		]
