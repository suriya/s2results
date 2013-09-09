from django.db import models
from storages.backends.s3boto import S3BotoStorage
from django.utils.text import slugify
from django.core.urlresolvers import reverse
import django.utils.timezone
import django.utils.dateformat
import json_field

protected_storage = S3BotoStorage(
  acl='private',
  querystring_auth=True,
  querystring_expire=600, # expires in 10 minutes
)

def resultclass_csv_upload_to(instance, filename):
    now = django.utils.timezone.now()
    timestamp = django.utils.dateformat.format(now, 'U')
    return 'resultclass_csv/%s-%s.csv' % (timestamp, slugify(instance.title))

class ResultClass(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    data_csv = models.FileField(upload_to=resultclass_csv_upload_to, storage=protected_storage)
    fields = json_field.JSONField()
    primary_field = models.CharField(max_length=255)
    secret_field = models.CharField(max_length=255)
    enabled = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ResultClass, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('result-class-detail', kwargs={ 'slug': self.slug })

class Result(models.Model):
    result_class = models.ForeignKey(ResultClass)
    primary_field_value = models.CharField(max_length=255)
    secret_field_value = models.CharField(max_length=255)
    data = json_field.JSONField()
    results_file = models.FileField(blank=True, upload_to='results/', storage=protected_storage)

    def __unicode__(self):
        return '%s (id : %s)' % (self.result_class, self.primary_field_value)
