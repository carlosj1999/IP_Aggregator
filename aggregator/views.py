# aggregator/views.py

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import IPAggregatorForm
from .utils import aggregate_ip_addresses

def index(request):
    form = IPAggregatorForm()
    result = None

    if request.method == 'POST':
        form = IPAggregatorForm(request.POST)
        if form.is_valid():
            ip_addresses = form.cleaned_data['ip_addresses']
            output_format = form.cleaned_data['output_format']
            why_blocked = form.cleaned_data['why_blocked']
            asn_code = form.cleaned_data['asn_code']
            
            result = aggregate_ip_addresses(ip_addresses, output_format, why_blocked, asn_code)
            
    
    else:
        form = IPAggregatorForm()

    return render(request, 'aggregator/index.html', {'form': form, 'result': result})

