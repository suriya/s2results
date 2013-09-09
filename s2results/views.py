
from .models import ResultClass, Result
from django.views.generic import DetailView, FormView, ListView
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.http import Http404

class ResultDetail(DetailView):
    model = Result
    context_object_name = 'result'

class ResultClassList(ListView):
    model = ResultClass
    context_object_name = 'resultclass_list'

class ResultClassDetail(DetailView):
    model = ResultClass
    context_object_name = 'resultclass'

class ResultClassSearch(FormView):
    template_name = 's2results/resultclass_search.html'

    def get_result(self, result_class, cleaned_data):
        primary_field_value = cleaned_data.get('primary_field_value')
        secret_field_value = cleaned_data.get('secret_field_value')
        if primary_field_value and secret_field_value:
            return result_class.result_set.get(primary_field_value=primary_field_value, secret_field_value=secret_field_value)
        return None

    def get_result_class_form_class(self, result_class):
        class ResultQueryForm(forms.Form):
            primary_field_value = forms.CharField(label=result_class.primary_field)
            secret_field_value = forms.CharField(label=result_class.secret_field, widget=forms.PasswordInput)
            secret_field_value = forms.CharField(label=result_class.secret_field)
            def clean(iself):
                cleaned_data = super(ResultQueryForm, iself).clean()
                try:
                    result = self.get_result(result_class, cleaned_data)
                except Result.DoesNotExist:
                    message = u"Could not locate result. '{}' and '{}' do not match".format(
                            result_class.primary_field, result_class.secret_field)
                    raise forms.ValidationError(message)
                return cleaned_data
        return ResultQueryForm

    def get_result_class_object(self):
        slug = self.kwargs.get('slug', None)
        result_class = get_object_or_404(ResultClass, slug=slug)
        return result_class

    def get_form_class(self):
        result_class = self.get_result_class_object()
        return self.get_result_class_form_class(result_class)

    def get_context_data(self, **kwargs):
        context = super(ResultClassSearch, self).get_context_data(**kwargs)
        context.update({
            'result_class': self.get_result_class_object(),
        })
        return context

    def form_valid(self, form):
        result_class = self.get_result_class_object()
        result = self.get_result(result_class, form.cleaned_data)
        if result.results_file:
            return redirect(result.results_file.url)
        else:
            raise Http404
