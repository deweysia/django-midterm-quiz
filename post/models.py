from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):

	title = models.CharField(max_length=250)
	date_created = models.DateTimeField(default=timezone.now)
	date_updated = models.DateTimeField(null=True, auto_now=True)
	content = models.TextField()
	is_active = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Post"
		verbose_name_plural = "Posts"

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})


	# override save() 

class Comment(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	content = models.TextField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Comment"
		verbose_name_plural = "Comments"
		ordering = ["-date_created"]

	def __str__(self):
		return f'{self.post.title}: {self.content}'
    