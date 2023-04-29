from django.db import models
from django.utils.text import slugify


class CategoryNews(models.Model):
    title = models.JSONField()


class News(models.Model):
    title = models.JSONField()
    body = models.JSONField()
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to='image/')
    category = models.ForeignKey('CategoryNews', on_delete=models.PROTECT, related_name='news')
    author = models.CharField(max_length=127, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)
