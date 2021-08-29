from django.db.models import query
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

def index(request):
    users = ["A", "B", "D", "E", "F"]
    return render(request, "firstapp/base.html", {"data": users})



class Index(TemplateView):
    template_name = "firstapp/index.html"
    # extra_context = {"data": "hi"}

    # def get_context_data(self, **kwargs):
    #     old_context = super().get_context_data(**kwargs)
    #     context_data = {"hi": "hello", "old_context": old_context}
    #     return context_data


from django.core.exceptions import ValidationError

# def contact_us(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         if len(phone) > 10:
#             raise ValidationError("Phone number must be 10 digits")
#         query = request.POST.get('query')
#     return render(request, 'firstapp/contactus.html')

from django.http import HttpResponse
from firstapp.forms import ContactUsForm

def contact_us(request):
    if request.method == 'POST':
        print(request.POST)
        form = ContactUsForm(request.POST)
        if form.is_valid():
            if len(form.cleaned_data.get('query')) > 50:
                form.add_error('query', "Query shud not be more than 50 characters.")
                return render(request, 'firstapp/contactus_new.html', {"form": form})
            form.save()
            return HttpResponse("Thank you for contacting us")
        else:
            if len(form.cleaned_data.get('query')) > 50:
                form.add_error(None, "Query shud not be more than 50 characters.")

            return render(request, 'firstapp/contactus_new.html', {"form": form})
    form = ContactUsForm()
    return render(request, 'firstapp/contactus_new.html', {"form": form})
