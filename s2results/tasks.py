
import csv
import requests
import itertools
from StringIO import StringIO
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from .models import ResultClass, Result

TEMPLATE_FILE = 's2results/result_detail.html'

def create_result(resultclass, csvrow):
    data = [ (key, value) for (key, value) in zip(resultclass.fields, csvrow) ]
    datadict = dict(data)
    result = Result(result_class=resultclass, data=data)
    result.primary_field_value = datadict.get(resultclass.primary_field, '')
    result.secret_field_value = datadict.get(resultclass.secret_field, '')
    result.save()
    filename = 'result-{}.html'.format(result.pk)
    content = render_to_string(TEMPLATE_FILE, { 'result' : result })
    result.results_file.save(filename, ContentFile(content))

def create_individual_results(resultclass):
    content = requests.get(resultclass.data_csv.url).content
    reader = csv.reader(StringIO(content))
    for row in itertools.islice(reader, 1, None):
        create_result(resultclass, row)

for rc in ResultClass.objects.all():
    create_individual_results(rc)
