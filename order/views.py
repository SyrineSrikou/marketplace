from django.shortcuts import render, redirect, get_object_or_404    
from django.http import HttpResponse, HttpResponseRedirect

# Creafrom django.shortcuts import render, redirect, get_object_or_404    

from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.template.loader import get_template
#from xhtml2pdf import pisa



""" 
  
def order_render_pdf_view(request,*args, **kwargs):
    pk = kwargs.get('pk')
    order = get_object_or_404(Order, pk=pk)

    template_path = 'order_pdf.html'
    context = {'order': order}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="order_detail.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_view(request):
    template_path = 'order_pdf.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="order_detail.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

 """