from django.db import models
from storages.backends.s3boto import S3BotoStorage
from django.utils.text import slugify
import json_field

protected_storage = S3BotoStorage(
  acl='private',
  querystring_auth=True,
  querystring_expire=600, # expires in 10 minutes
)

def result_csv_upload_to(instance, filename):
    return 'results_csv/%s.csv' % slugify(instance.title)

class ResultClass(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    data_csv = models.FileField(upload_to=result_csv_upload_to, storage=protected_storage)
    fields = json_field.JSONField()
    primary_field = models.CharField(max_length=255)
    secret_field = models.CharField(max_length=255)
    enabled = models.BooleanField()

class Result(models.Model):
    result_class = models.ForeignKey(ResultClass)
    primary_field_value = models.CharField(max_length=255)
    secret_field_value = models.CharField(max_length=255)
    data = json_field.JSONField()
    results_file = models.FileField(blank=True, upload_to='results/', storage=protected_storage)
